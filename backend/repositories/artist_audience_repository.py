"""
ARTIST_AUDIENCE_REPOSITORY

Coordinates communication between artist_audience_service, location_service, and soundcharts_service,
to make sure that the database is checked for cache before calling the api for information specifically
regarding the artist audience and local monthly listeners.

"""

# IMPORTS

from backend.services import artist_audience_service, artist_service, location_service, soundcharts_service

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

def getArtistCityAudience(artist_uuid: str, cityId: int, platform="spotify"):

    cached = artist_audience_service.getCachedAudience(
        artist_uuid,
        cityId,
        platform
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

def selectCity(artist_uuid: str, cityId: int, platform="spotify"):
    # ensure cities are cached before trying to select one
    cities = getAllArtistCities(artist_uuid)
    if isinstance(cities, dict) and "error" in cities:
        return cities

    cached_listeners = artist_audience_service.getLocalMonthlyListeners(
        artist_uuid,
        cityId,
        platform,
    )
    
    if cached_listeners is None:
        # no fresh cached data for this city
        return None

    
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

def getAllArtistCities(uuid: str):
    # return the artist's top 50 fresh cities in a format that is easy for the front end to display
    print(f"[getAllArtistCities] Starting for artist_uuid: {uuid}")

    # make sure the artist is in the database
    artist = artist_service.getArtistByUUID(uuid)
    print(f"[getAllArtistCities] Artist in database: {artist is not None}")
    if artist is None:
        print(f"[getAllArtistCities] WARNING: Artist {uuid} not in database")
    
    # checking the cache first
    print(f"[getAllArtistCities] Checking cache for artist_uuid: {uuid}")
    cities = artist_audience_service.getArtistTop50Cities(uuid, "spotify")
    print(f"[getAllArtistCities] Cache result: {cities is not None}, Count: {len(cities) if cities else 0}")

    if cities:
        print(f"[getAllArtistCities] Found {len(cities)} cached cities, returning")
        return cities

    # calling for soundcharts if not found in cache
    print(f"[getAllArtistCities] No cached cities, calling Soundcharts API")
    if not cities:
        try:
            print(f"[getAllArtistCities] Fetching local streaming audience from Soundcharts")
            payload = soundcharts_service.getLocalStreamingAudience(uuid)
            print(f"[getAllArtistCities] Soundcharts payload received, items: {len(payload) if payload else 0}")
        except soundcharts_service.SoundchartsError as error:
            print(f"[getAllArtistCities] Soundcharts error: {error.status_code} - {error.message}")
            return {
                "statusCode": error.status_code,
                "error": error.message,
            }
        
        # Cache immediately
        print(f"[getAllArtistCities] Saving artist audience to database")
        saved_snapshots = artist_audience_service.setArtistAudience(uuid, payload, "spotify")
        print(f"[getAllArtistCities] Saved {len(saved_snapshots)} city snapshots")

        if not saved_snapshots:
            print(f"[getAllArtistCities] No snapshots were saved")
            return []
        
        print(f"[getAllArtistCities] Retrieving cities from cache after save")
        cities = artist_audience_service.getArtistTop50Cities(uuid, "spotify")
        print(f"[getAllArtistCities] Retrieved {len(cities) if cities else 0} cities after save")

    result = cities if cities else []
    print(f"[getAllArtistCities] Returning {len(result)} cities")
    return result