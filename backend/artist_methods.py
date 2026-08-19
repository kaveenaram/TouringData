# should have all methods for getting artist data from soundcharts api
# minimize API calls

from api import sc
from database import db
from datetime import date, timedelta

def searchArtist(input: str):
# input will always be a string because we are getting it from the front end
    # if artist already exists in database return artist
    # otherwise call API
    artist = sc.search.search_artist_by_name(input, 0, 3)
    if artist is None:
        return []
    return artist

def selectArtist():

# method that returns top 50 cities for an artist


# monthly listeners by city
# recode all of this so that there is a method to get the local streaming audience
# there needs to be a method to push all the cities and countries into db
# there needs to be a method that calls from the db for all cities that are in the top 50 for an artist


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
