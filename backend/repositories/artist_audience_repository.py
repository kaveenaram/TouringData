# communications between artist_audience_service and soundcharts_service
# to make sure that the database is checked for cache before calling the api for info

from backend.services import artist_audience_service
from backend.services import location_service
from backend.services import soundcharts_service


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

    # triple check that this logic works, is this the correct snapshot?
    return localListeners

def getArtistCityAudience(artist_uuid: str, cityId: int, platform="spotify"):
    cached = artist_audience_service.getCachedAudience(
        artist_uuid,
        cityId,
        platform,
    )

    if cached is not None:
        city_record = location_service.Location_Service.getCityById(cityId)
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

    city_record = location_service.Location_Service.getCityById(cityId)
    return {
        "cityId": cached.city_id,
        "cityKey": city_record.cityKey if city_record else None,
        "cityName": city_record.city_name if city_record else None,
        "countryCode": city_record.country_code if city_record else None,
        "localMonthlyListeners": cached.local_monthly_listeners,
        "observedAt": cached.observed_at,
    }

def selectCity(artist_uuid: str, cityId: int, platform="spotify"):
    city_record = location_service.Location_Service.getCityById(cityId)

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

    location_service.Location_Service.setCityKey(
        city_record.city_name,
        city_record.country_code,
        cityKey,
    )
    return getArtistCityAudience(artist_uuid, cityId, platform)


# get city key method needs country code, you can get country code from location... you would have the country code with the country name
# because we are getting the venue needed data from the artist audience, which comes with country code.


# method that stores citykey in the database

def getAllArtistCities(uuid: str):
    # return the artist's top 50 fresh cities in a format that is easy for the front end to display
    return artist_audience_service.getArtistTop50Cities(uuid, "spotify")



# for example:
    # front end calls dashboard
    # from the dashboard: artist audience monthly listeners
    # call comes to artist_aud_repo
    # repo calls artist_audience_service getLocalMonthlyListeners()
    # artist_audience_service returns None, meaning now let's call the api
    # repo calls soundcharts getlocalstreamingaudience
    # repo calls artist_audience_service setArtistAudience()
    # repo returns data to dashboard
    # dashboard formats this data to be pushed to the front end
    # front end receives, front end happy



#request artist audience
 #   -> get fresh snapshots from database
  #  -> if snapshots exist, return them
   # -> otherwise call Soundcharts once
   # -> pass complete payload to setArtistAudience()
   # -> return saved snapshots

#The repository should not call Soundcharts if getFreshSnapshots() returns a non-empty list.