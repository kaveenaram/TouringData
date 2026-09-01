

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

"""
-----------------------------
Name
-----------------------------
Description
Use
-----------------------------
Parameters
Returns
-----------------------------
"""

def setArtistAudience(artist_uuid: str, payload: list, platform="spotify"):
    fetched_at = datetime.now(timezone.utc).replace(tzinfo=None)

    latest_item = max(
        payload or [],
        key=lambda item: item.get("date", ""),
        default=None,
    )

    if latest_item is None:
        return []

    # there does not exist a snapshot within the last 7 days, so we will create new snapshots for each city in the latest_item

    saved_snapshots = []

    for city_plot in latest_item.get("cityPlots", []):
        observed_at = datetime.fromisoformat(
            city_plot["date"].replace("Z", "+00:00")
        ).replace(tzinfo=None)
         
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

        snapshot = Artist_Audience.query.filter_by(
            artist_uuid=artist_uuid,
            city_id=city.id,
            platform=platform,
            observed_at=observed_at,
        ).first()

        if snapshot is None:
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
            snapshot.local_monthly_listeners = str(city_plot.get("value", 0))
            snapshot.fetched_at = fetched_at

        saved_snapshots.append(snapshot)

    db.session.commit()

    return saved_snapshots

# GETTERS

"""
-----------------------------
Name
-----------------------------
Description
Use
-----------------------------
Parameters
Returns
-----------------------------
"""

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

"""
-----------------------------
Name
-----------------------------
Description
Use
-----------------------------
Parameters
Returns
-----------------------------
"""

def getLocalMonthlyListeners(artist_uuid: str, cityId: int, platform="spotify"):
    # check if artist audience is in database by artist_uuid, cityId, and platform
    # if artist audience is not in database return None
    cached_audience = getCachedAudience(artist_uuid, cityId, platform)

    if cached_audience is not None:
        return cached_audience.local_monthly_listeners
    else:
        return None

"""
-----------------------------
Name
-----------------------------
Description
Use
-----------------------------
Parameters
Returns
-----------------------------
"""

# get artist top 50 cities by uuid

# makes no sense.. please review
def getArtistTop50Cities(artist_uuid: str, platform="spotify"):
    artist = artist_service.getArtistByUUID(artist_uuid)

    if artist is None:
        return None

    cutoff_date = datetime.now() - AUDIENCE_CACHE_TTL

    latest_observed_at = (
        db.session.query(db.func.max(Artist_Audience.observed_at))
        .filter_by(
            artist_uuid=artist_uuid,
            platform=platform,
        )
        .filter(Artist_Audience.observed_at >= cutoff_date)
        .scalar()
    )

    if latest_observed_at is None:
        return []

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

    return [
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

"""
-----------------------------
Name
-----------------------------
Description
Use
-----------------------------
Parameters
Returns
-----------------------------
"""

def getArtistTop50CityKeys(artist_uuid: str, platform="spotify"):
    return [
        city["cityKey"]
        for city in getArtistTop50Cities(artist_uuid, platform)
        if city["cityKey"] is not None
    ]

"""
-----------------------------
Name
-----------------------------
Description
Use
-----------------------------
Parameters
Returns
-----------------------------
"""

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



