

# IMPORTS

from backend.tables.artist_audience import Artist_Audience
from datetime import datetime, timezone, timedelta
from backend import db
from backend.services import artist_service
from backend.services import location_service
from sqlalchemy import Integer, cast
from backend.tables.location import City

# artist_audience_service acts as a way to interact with the database's artist_audience table.

# GLOBAL VARIABLES


AUDIENCE_CACHE_TTL = timedelta(days=7)

# SETTERS



def setArtistAudience(artist_uuid: str, payload: dict, platform="spotify"):
    print(f"[setArtistAudience] Starting for artist_uuid: {artist_uuid}")
    
    # extract lastCrawlDate from payload's 'related' section
    # this is when soundcharts last collected the data
    # extract lastCrawlDate from payload's 'related' section
    # this is when soundcharts last collected the data
    related = payload.get("related", {})
    last_crawl_date_str = related.get("lastCrawlDate")
    print(f"[setArtistAudience] Raw lastCrawlDate from payload: {last_crawl_date_str}")
        
    # observed_at will be set to lastCrawlDate (when Soundcharts observed)
    observed_at_value = None
    if last_crawl_date_str:
        observed_at_value = datetime.fromisoformat(
            last_crawl_date_str.replace("Z", "+00:00")
        ).replace(tzinfo=None)
    
    print(f"[setArtistAudience] Parsed observed_at (lastCrawlDate): {observed_at_value}")
    
    # fetched_at is when WE fetched it from Soundcharts
    fetched_at = datetime.now()
    print(f"[setArtistAudience] fetched_at (when we called API): {fetched_at}")
    
    items = payload.get("items", [])
    print(f"[setArtistAudience] Payload items: {len(items) if items else 0}")

    latest_item = max(
        items or [],
        key=lambda item: item.get("date", ""),
        default=None,
    )

    if latest_item is None:
        print(f"[setArtistAudience] No latest_item found in payload")
        return []

    # there does not exist a snapshot within the last crawl cycle, so we will create new snapshots for each city in the latest_item

    saved_snapshots = []
    city_plots = latest_item.get("cityPlots", [])
    print(f"[setArtistAudience] Found {len(city_plots)} city plots")

    for idx, city_plot in enumerate(city_plots):
        print(f"[setArtistAudience] Processing city {idx + 1}/{len(city_plots)}")
        # Use lastCrawlDate as observed_at (when Soundcharts observed the data)
        observed_at = observed_at_value
        print(f"[setArtistAudience] Using lastCrawlDate as observed_at: {observed_at}")
         
        city_name = city_plot.get("cityName")
        country_code = city_plot.get("countryCode")
        country_name = city_plot.get("countryName")

        # set country and city in the database
        location_service.setCountry(country_code, country_name)
        city = location_service.getCityByNameAndCountryCode(
            city_name,
            country_code,
        )

        if city is None:
            city = location_service.setCity(city_name, country_code)
            db.session.flush()

        if city.id is None:
            db.session.flush()

        snapshot = Artist_Audience.query.filter_by(
            artist_uuid=artist_uuid,
            city_id=city.id,
            platform=platform,
            observed_at=observed_at,
        ).first()
        print(f"[setArtistAudience] Found existing snapshot: {snapshot is not None}")

        if snapshot is None:
            print(f"[setArtistAudience] Creating new snapshot for city_id: {city.id}")
            snapshot = Artist_Audience(
                artist_uuid=artist_uuid,
                city_id=city.id,
                local_monthly_listeners=str(city_plot.get("value", 0)),
                platform=platform,
                observed_at=observed_at,
                fetched_at=fetched_at,
            )
            db.session.add(snapshot)
        else:
            print(f"[setArtistAudience] Updating existing snapshot")
            snapshot.local_monthly_listeners = str(city_plot.get("value", 0))
            snapshot.fetched_at = fetched_at

        saved_snapshots.append(snapshot)

    print(f"[setArtistAudience] Committing {len(saved_snapshots)} snapshots to database")
    db.session.commit()
    print(f"[setArtistAudience] Commit successful")

    return saved_snapshots

# GETTERS



def getCachedAudience(artist_uuid: str, cityId: int, platform="spotify"):
    # check if artist audience is in database by artist_uuid, cityId, and platform
    # if artist audience is not in database return None
    cutoff_date = datetime.now() - AUDIENCE_CACHE_TTL  # 7 day cutoff based on Soundcharts observation date

    cached_audience = (Artist_Audience.query
            .filter_by(
                artist_uuid=artist_uuid,
                city_id=cityId,
                platform=platform,
            )
            .filter(Artist_Audience.observed_at >= cutoff_date)
            .order_by(Artist_Audience.observed_at.desc())
            .first()
        )

    return cached_audience



def getLocalMonthlyListeners(artist_uuid: str, cityId: int, platform="spotify"):
    # check if artist audience is in database by artist_uuid, cityId, and platform
    # if artist audience is not in database return None
    cached_audience = getCachedAudience(artist_uuid, cityId, platform)

    if cached_audience is not None:
        return cached_audience.local_monthly_listeners
    else:
        return None



# get artist top 50 cities by uuid

# makes no sense.. please review
def getArtistTop50Cities(artist_uuid: str, platform="spotify"):
    print(f"[getArtistTop50Cities] Querying for artist_uuid: {artist_uuid}")
    artist = artist_service.getArtistByUUID(artist_uuid)
    print(f"[getArtistTop50Cities] Artist found: {artist is not None}")

    if artist is None:
        print(f"[getArtistTop50Cities] Artist not in database, returning None")
        return None

    cutoff_date = datetime.now() - AUDIENCE_CACHE_TTL
    print(f"[getArtistTop50Cities] Cutoff date: {cutoff_date}")
    
    print(f"[getArtistTop50Cities] Querying latest observed_at for artist_uuid: {artist_uuid}")
    latest_observed_at = (
        db.session.query(db.func.max(Artist_Audience.observed_at))
        .filter_by(
            artist_uuid=artist_uuid,
            platform=platform,
        )
        .filter(Artist_Audience.observed_at >= cutoff_date)
        .scalar()
    )
    print(f"[getArtistTop50Cities] Latest observed_at: {latest_observed_at}")
    
    if latest_observed_at is None:
        print(f"[getArtistTop50Cities] No fresh snapshots found (data not observed within {AUDIENCE_CACHE_TTL.days} days)")
        return []
    
    print(f"[getArtistTop50Cities] Querying top 50 cities for observed_at: {latest_observed_at}")
    top_snapshots = (
        db.session.query(Artist_Audience, City)
        .join(City, City.id == Artist_Audience.city_id)
        .filter(
            Artist_Audience.artist_uuid == artist_uuid,
            Artist_Audience.platform == platform,
            Artist_Audience.observed_at == latest_observed_at,
        )
        .order_by(
            cast(
                Artist_Audience.local_monthly_listeners,
                Integer,
            ).desc(),
            City.city_name.asc(),
        )
        .limit(50)
        .all()
    )
    print(f"[getArtistTop50Cities] Found {len(top_snapshots)} cities")

    result = [
        {
            "cityId": snapshot.city_id,
            "cityKey": city.cityKey,
            "cityName": city.city_name,
            "countryCode": city.country_code,
            "localMonthlyListeners": snapshot.local_monthly_listeners,
            "observedAt": snapshot.observed_at,
        }
        for snapshot, city in top_snapshots
    ]
    print(f"[getArtistTop50Cities] Returning {len(result)} cities")
    return result


def getFreshSnapshots(artist_uuid: str, platform="spotify"):
    # check if artist audience is in database by artist_uuid, and platform
    # if artist audience is not in database return None
    cutoff_date = datetime.now() - AUDIENCE_CACHE_TTL  # 7 day cutoff based on Soundcharts observation date

    fresh_snapshots = (Artist_Audience.query
            .filter_by(
                artist_uuid=artist_uuid,
                platform=platform,
            )
            .filter(Artist_Audience.observed_at >= cutoff_date)
            .order_by(Artist_Audience.observed_at.desc())
            .all()
        )

    return fresh_snapshots



