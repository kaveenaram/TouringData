# communications between artist_service and soundcharts_service
# to make sure that the database is checked for cache before calling the api for info

# for example:
    # front end calls dashboard
    # from the dashboard: searching for artist
    # call comes to artist_repo
    # repo calls artist_service getArtistByName()
    # artist_service returns None, meaning now let's call the api
    # repo calls soundcharts searchForArtist()
    # repo calls artist_service setArtist()
    # repo returns data to dashboard
    # dashboard formats this data to be pushed to the front end
    # front end receives, front end happy