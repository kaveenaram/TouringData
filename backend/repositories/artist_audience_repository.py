"""
ARTIST_AUDIENCE_REPOSITORY

Coordinates communication between artist_audience_service, location_service, and soundcharts_service,
to make sure that the database is checked for cache before calling the api for information specifically
regarding the artist audience and local monthly listeners.

"""

# IMPORTS

from backend.services import artist_audience_service
from backend.services import location_service
from backend.services import soundcharts_service

"""
-----------------------------
getLocalMonthlyListeners
-----------------------------
Checks cache for an artist's local monthly listeners.
If not found, it calls Soundcharts and sends info to cache.
-----------------------------
parameters: uuid: str, cityId: int, platform="spotify"
returns: localListeners
-----------------------------
"""

def getLocalMonthlyListeners(uuid: str, cityId: int, platform="spotify"):
    localListeners = artist_audience_service.getLocalMonthlyListeners(
        uuid,
        cityId,
        platform,
    )
    if localListeners is None:
        if not artist_audience_service.getFreshSnapshots(uuid, platform):
            try:
                payload = soundcharts_service.getLocalStreamingAudience(uuid)
            except soundcharts_service.SoundchartsError as error:
                return {
                    "statusCode": error.status_code,
                    "error": error.message,
                }
            artist_audience_service.setArtistAudience(uuid, payload, platform)
        localListeners = artist_audience_service.getLocalMonthlyListeners(
            uuid,
            cityId,
            platform,
        )

    return localListeners

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

def getArtistCityAudience(artist_uuid: str, cityId: int, platform="spotify"):

    cached = artist_audience_service.getCachedAudience(
        artist_uuid,
        cityId,
        platform,
    )

    if cached is not None:
        city_record = location_service.getCityById(cityId)
        return {
            "cityId": cached.city_id,
            "cityKey": city_record.cityKey if city_record else None,
            "cityName": city_record.city_name if city_record else None,
            "countryCode": city_record.country_code if city_record else None,
            "localMonthlyListeners": cached.local_monthly_listeners,
            "observedAt": cached.observed_at,
        }

    if not artist_audience_service.getFreshSnapshots(artist_uuid, platform):
        try:
            payload = soundcharts_service.getLocalStreamingAudience(artist_uuid)
        except soundcharts_service.SoundchartsError as error:
            return {
                "statusCode": error.status_code,
                "error": error.message,
            }
        artist_audience_service.setArtistAudience(artist_uuid, payload, platform)

    cached = artist_audience_service.getCachedAudience(
        artist_uuid,
        cityId,
        platform,
    )

    if cached is None:
        return None

    city_record = location_service.getCityById(cityId)
    return {
        "cityId": cached.city_id,
        "cityKey": city_record.cityKey if city_record else None,
        "cityName": city_record.city_name if city_record else None,
        "countryCode": city_record.country_code if city_record else None,
        "localMonthlyListeners": cached.local_monthly_listeners,
        "observedAt": cached.observed_at,
    }

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

def selectCity(artist_uuid: str, cityId: int, platform="spotify"):
    # ensure cities are cached before trying to select one
    cities = getAllArtistCities(artist_uuid)
    if isinstance(cities, dict) and "error" in cities:
        return cities

    city_record = location_service.getCityById(cityId)

    if city_record is None:
        return None

    if city_record.cityKey is not None:
        return getArtistCityAudience(artist_uuid, cityId, platform)

    try:
        city_matches = soundcharts_service.getCityKey(
            city_record.city_name,
            city_record.country_code,
        )
    except soundcharts_service.SoundchartsError as error:
        return {
            "statusCode": error.status_code,
            "error": error.message,
        }
    cityKey = next(
        (
            city_match.get("cityKey") or city_match.get("city_key")
            for city_match in city_matches
            if city_match.get("cityName", city_record.city_name).lower()
            == city_record.city_name.lower()
        ),
        None,
    )

    if cityKey is None and len(city_matches) == 1:
        cityKey = city_matches[0].get("cityKey") or city_matches[0].get("city_key")

    if cityKey is None:
        return None

    location_service.setCityKey(
        city_record.city_name,
        city_record.country_code,
        cityKey,
    )
    return getArtistCityAudience(artist_uuid, cityId, platform)


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

def getAllArtistCities(uuid: str):
    # return the artist's top 50 fresh cities in a format that is easy for the front end to display

    # checking the cache first
    cities = artist_audience_service.getArtistTop50Cities(uuid, "spotify")

    # calling for soundcharts if not found in cache
    if not cities:
        try:
            payload = soundcharts_service.getLocalStreamingAudience(uuid)
        except soundcharts_service.SoundchartsError as error:
            return {
                "statusCode": error.status_code,
                "error": error.message,
            }
        
        # Cache immediately
        artist_audience_service.setArtistAudience(uuid, payload, "spotify")
        cities = artist_audience_service.getArtistTop50Cities(uuid, "spotify")

    return cities