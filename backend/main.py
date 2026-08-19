# all methods in main are to allow front end to access the backend and get data from the soundcharts api

def dashboard():
    # dashboard calls all needed methods for info

    # first: makes user search for artist and choose city
        # if artist does not exist, pop up error and try again
    # second: once artist is found, dashboard should automatically ask for information from API based on artist and city
    # find ways in backend to minimize API calls

    # ex / puesdo code
    # input = "Jae Stephens"
    # THIS WOULD NEED TO BE IN ARTIST.PY TO HIDE THE TRY AGAIN PART
    # artist = json.loads(sc.search_for_artist(input, offset=0, limit=1))
    # if artist = None: "Try Again" --> searchMethod
    # else artist_uuid = artist["uuid"] 
    # now you would use this uuid to access the rest of the info through the artist.py methods

    # how to mock api calls in python