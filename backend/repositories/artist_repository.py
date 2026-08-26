# communications between artist_service and soundcharts_service
# to make sure that the database is checked for cache before calling the api for info

from datetime import datetime, timezone

from backend.services import artist_service
from backend.services import soundcharts_service

# for example:
    # front end calls dashboard
    # from the dashboard: searching for artist
    # call comes to artist_repo
    # repo calls artist_service getArtistByName()
    # artist_service returns None, meaning now let's call the api
    # repo calls soundcharts searchForArtist()
    # repo calls soundcharts getArtistTotalMonthlyListeners()
    # repo calls artist_service setArtist()
    # repo returns data to dashboard
    # dashboard formats this data to be pushed to the front end
    # front end receives, front end happy

# only when an artist is selected does it call for their monthly listeners and put them in the database

def searchForArtist(name: str):
    result = artist_service.getArtistbyName(name)
    if result is not None:
        result = [result]
    else:
        try:
            result = soundcharts_service.searchByName(name)
        except soundcharts_service.SoundchartsError as error:
            return {
                "statusCode": error.status_code,
                "error": error.message,
            }

    if not result:
        return []

    artists = []
    for artist in result:
        if isinstance(artist, dict):
            artists.append({
                "uuid": artist.get("uuid"),
                "name": artist.get("name"),
                "slug": artist.get("slug"),
                "appUrl": artist.get("appUrl"),
                "imageUrl": artist.get("imageUrl"),
            })
        else:
            artists.append({
                "uuid": artist.uuid,
                "name": artist.name,
                "slug": artist.slug,
                "appUrl": artist.appUrl,
                "imageUrl": artist.imageUrl,
            })

    return artists

def selectArtist(artist: dict):
    #check/save artist metadata
    #check audience cache
    #if stale, call Soundcharts once
    #save all city snapshots
    #return selected artist data
    if not artist or not artist.get("uuid"):
        return None

    uuid = artist["uuid"]
    try:
        listener_items = soundcharts_service.getArtistTotalMonthlyListeners(uuid)
    except soundcharts_service.SoundchartsError as error:
        return {
            "statusCode": error.status_code,
            "error": error.message,
        }
    listeners, observed_at = getArtistMonthlyListeners(listener_items)

    if listeners is None or observed_at is None:
        return None

    fetched_at = datetime.now(timezone.utc)
    artist = artist_service.setArtist(
        uuid=uuid,
        name=artist.get("name", ""),
        slug=artist.get("slug", ""),
        appUrl=artist.get("appUrl"),
        imageUrl=artist.get("imageUrl"),
        monthlyListeners=str(listeners),
        observed_at=observed_at,
        fetched_at=fetched_at,
    )

    return {
        "uuid": artist.uuid,
        "name": artist.name,
        "slug": artist.slug,
        "appUrl": artist.appUrl,
        "imageUrl": artist.imageUrl,
        "monthlyListeners": artist.monthlyListeners,
    }


def getArtistMonthlyListeners(items: list):
    if not items:
        return None, None

    latest_item = max(
        items,
        key=lambda item: item.get("date", ""),
        default=None,
    )

    if latest_item is None:
        return None, None

    observed_at_value = latest_item.get("date")
    if observed_at_value is None:
        return latest_item.get("value"), None

    observed_at = datetime.fromisoformat(
        observed_at_value.replace("Z", "+00:00")
    )

    return latest_item.get("value"), observed_at


