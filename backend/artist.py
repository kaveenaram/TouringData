# should have all methods for getting artist data from soundcharts api
# minimize API calls


from api import sc

def searchArtist(input: str):
# input will always be a string because we are getting it from the front end
    artist = sc.search_artist_by_name(input, offset=0, limit=1)
    if artist is None:
        return "Try Again"
    return artist