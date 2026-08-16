# should have all methods for getting artist data from soundcharts api
# minimize API calls


from api import sc
from datetime import date, timedelta

def searchArtist(input: str):
# input will always be a string because we are getting it from the front end
    artist = sc.search.search_artist_by_name(input, 0, 1)
    if artist is None:
        return 0
    return artist

# monthly listeners by city

def artistListenersByCity(artist, city: str, country: str):
    today = date.today()
    listenerData = sc.artist.get_local_streaming_audience(artist_uuid=artist["uuid"], str="spotify", end_date=today)

    if not listenerData or "items" not in listenerData:
        return "No data available"

    latest_item = listenerData["items"][-1]

    for city_data in latest_item.get("cityPlots", []):
        city_match = city_data.get("cityName", "").lower() == city.lower()

        if country:
            country_match = city_data.get("countryName", "").lower() == country.lower()
        else:
            country_match = True

        if city_match and country_match:
            return city_data.get("value", 0)

    return "City Not In Top 50"


FIGURE OUT HOW TO GET ONLY USA AND CA DATA
