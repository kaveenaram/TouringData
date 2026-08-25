from tables.artist_audience import Artist_Audience
from datetime import datetime, timezone, timedelta
from backend import db
from artist_service import getArtistByUUID
from location_service import Location_Service
from soundcharts_service import getCityKey
from sqlalchemy import Integer, cast
from tables.location import City

# artist_audience_service acts as a way to interact with the database's artist_audience table.

AUDIENCE_CACHE_TTL = timedelta(days=7)

# SETTERS

def setArtistAudience(artist_uuid: str, payload: dict):
    platform = payload["related"].get("platform", "spotify")
    fetched_at = datetime.now(timezone.utc)

    latest_item = max(
        payload.get("items", []),
        key=lambda item: item.get("date", ""),
        default=None,
    )

    if latest_item is None:
        return []

    existing_snapshot = getFreshSnapshots(artist_uuid, platform)

    if existing_snapshot:
        return existing_snapshot

    # there does not exist a snapshot within the last 24 hours, so we will create new snapshots for each city in the latest_item

    saved_snapshots = []

    for city_plot in latest_item.get("cityPlots", []):
        observed_at = datetime.fromisoformat(
            city_plot["date"].replace("Z", "+00:00")
        )
         
        city_name = city_plot.get("cityName")
        country_code = city_plot.get("countryCode")
        country_name = city_plot.get("countryName")

        # set country and city in the database
        country = Location_Service.setCountry(country_code, country_name)
        cityKey = getCityKey(city_name, country_code)
        city = Location_Service.setCity(cityKey, city_name, country_code)

        snapshot = Artist_Audience(
            artist_uuid=artist_uuid,
            city_key=cityKey,
            local_monthly_listeners=str(city_plot.get("value", 0)),
            platform=platform,
            observed_at=observed_at,
            fetched_at=fetched_at,
        )

        db.session.add(snapshot)
        saved_snapshots.append(snapshot)

    db.session.commit()

    return saved_snapshots

# GETTERS

def getCachedAudience(artist_uuid: str, cityKey: int, platform="spotify"):
    # check if artist audience is in database by artist_uuid, city_id, and platform
    # if artist audience is not in database return None
    cutoff_date = datetime.now(timezone.utc) - AUDIENCE_CACHE_TTL  # 24 hours cutoff for audience data

    cached_audience = (Artist_Audience.query
            .filter_by(
                artist_uuid=artist_uuid,
                cityKey=cityKey,
                platform=platform,
            )
            .filter(Artist_Audience.fetched_at >= cutoff_date)
            .order_by(Artist_Audience.fetched_at.desc())
            .first()
        )

    return cached_audience

def getLocalMonthlyListeners(artist_uuid: str, cityKey: str, platform="spotify"):
    # check if artist audience is in database by artist_uuid, city_id, and platform
    # if artist audience is not in database return None
    cached_audience = getCachedAudience(artist_uuid, cityKey, platform)

    if cached_audience is not None:
        return cached_audience.local_monthly_listeners
    else:
        return None

# get artist top 50 cities by uuid
def getArtistTop50Cities(artist_uuid: str, platform="spotify"):
    artist = getArtistByUUID(artist_uuid)

    if artist is None:
        return None

    latest_observed_at = (
        db.session.query(db.func.max(Artist_Audience.observed_at))
        .filter_by(
            artist_uuid=artist_uuid,
            platform=platform,
        )
        .scalar()
    )

    if latest_observed_at is None:
        return []

    top_snapshots = (
        Artist_Audience.query
        .join(City, City.cityKey == Artist_Audience.cityKey)
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

    return [snapshot.cityKey for snapshot in top_snapshots]

def getFreshSnapshots(artist_uuid: str, platform="spotify"):
    # check if artist audience is in database by artist_uuid, and platform
    # if artist audience is not in database return None
    cutoff_date = datetime.now(timezone.utc) - AUDIENCE_CACHE_TTL  # 24 hours cutoff for audience data

    fresh_snapshots = (Artist_Audience.query
            .filter_by(
                artist_uuid=artist_uuid,
                platform=platform,
            )
            .filter(Artist_Audience.fetched_at >= cutoff_date)
            .order_by(Artist_Audience.local_monthly_listeners.desc())
            .all()
        )

    return fresh_snapshots



