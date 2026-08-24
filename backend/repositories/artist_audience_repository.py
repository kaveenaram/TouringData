# communications between artist_audience_service and soundcharts_service
# to make sure that the database is checked for cache before calling the api for info

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