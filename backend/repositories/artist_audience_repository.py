# communications between artist_audience_service and soundcharts_service
# to make sure that the database is checked for cache before calling the api for info

from services.artist_audience_service import getLocalMonthlyListeners, setArtistAudience
from services.soundcharts_service import getLocalStreamingAudience

def getLocalMonthlyListeners(uuid, cityKey):
    localListeners = getLocalMonthlyListeners(uuid, cityKey) # help...
    if localListeners is None:
        payload = getLocalStreamingAudience(uuid)
        setArtistAudience(uuid, payload)
        localListeners = getLocalMonthlyListeners(uuid, cityKey)

    # triple check that this logic works, is this the correct snapshot?
    return localListeners



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