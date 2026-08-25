from backend.api import sc

# please add in what to do with error codes




# search for artist by name
def searchByName(name: str):
    # returns max top 3 options
    # returns none if search does not work
    return sc.search.search_artist_by_name(name, 0, 3)


# search for artist by uuid
def getArtistByUUID(uuid: str):
    # returns artist data
    # returns none if artist does not exist
    return sc.artist.get_artist_metadata(uuid)


# search for local streaming audience
def getLocalStreamingAudience(uuid: str):
    # returns streaming audience data
    # returns none if artist does not exist
    return sc.artist.get_local_streaming_audience(uuid, "spotify")

def getCityKey(city: str, countryCode: str):
    response = sc.referential.get_cities_for_venue_festival(countryCode, city)
    return response

# or maybe just get venues in city...
# store venues into database
def getCapacityAppropriateVenuesinCity(cityKey:str, capacityLowerRange: str, capacityHigherRange: str):
    venues = sc.city.get_venues_by_citykey(cityKey)
   
