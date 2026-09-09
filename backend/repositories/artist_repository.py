# communications between artist_service and soundcharts_service
# to make sure that the database is checked for cache before calling the api for info

# IMPORTS

from datetime import datetime
from backend.services import artist_service
from backend.services import soundcharts_service



def searchForArtist(name: str):

    # always call soundcharts first to show all options.
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
                "genre": (artist.get("genres", [{}])[0].get("root")
                          if artist.get("genres")
                          else None),
            })
        else:
            artists.append({
                "uuid": artist.uuid,
                "name": artist.name,
                "slug": artist.slug,
                "appUrl": artist.appUrl,
                "imageUrl": artist.imageUrl,
                "genre": artist.genre,
            })

    return artists


def selectArtist(artist: dict):
    if not artist or not artist.get("uuid"):
        return None

    uuid = artist["uuid"]
    cached_artist = artist_service.getArtistByUUID(uuid)
    cached_listeners = artist_service.getArtistMonthlyListeners(uuid)

    if cached_artist is not None and cached_listeners is not None:
        return {
            "uuid": cached_artist.uuid,
            "name": cached_artist.name,
            "slug": cached_artist.slug,
            "appUrl": cached_artist.appUrl,
            "imageUrl": cached_artist.imageUrl,
            "genre": cached_artist.genre,
            "monthlyListeners": cached_artist.monthlyListeners,
        }

    try:
        listener_items = soundcharts_service.getArtistTotalMonthlyListeners(uuid)
        listeners, observed_at = getArtistMonthlyListeners(listener_items)

        if listeners is None or observed_at is None:
            raise soundcharts_service.SoundchartsError(
                503,
                "Monthly listener information is unavailable.",
            )

        saved_artist = artist_service.setArtist(
            uuid=uuid,
            name=artist.get("name", ""),
            slug=artist.get("slug", ""),
            appUrl=artist.get("appUrl"),
            imageUrl=artist.get("imageUrl"),
            genre=artist.get("genre"),
            monthlyListeners=str(listeners),
            observed_at=observed_at,
            fetched_at=datetime.now(),
        )

        return {
            "uuid": saved_artist.uuid,
            "name": saved_artist.name,
            "slug": saved_artist.slug,
            "appUrl": saved_artist.appUrl,
            "imageUrl": saved_artist.imageUrl,
            "genre": saved_artist.genre,
            "monthlyListeners": saved_artist.monthlyListeners,
        }

    except soundcharts_service.SoundchartsError:
        if cached_artist is not None:
            return {
                "uuid": cached_artist.uuid,
                "name": cached_artist.name,
                "slug": cached_artist.slug,
                "appUrl": cached_artist.appUrl,
                "imageUrl": cached_artist.imageUrl,
                "genre": cached_artist.genre,
                "monthlyListeners": cached_artist.monthlyListeners,
            }

        return {
            "statusCode": 503,
            "error": "Artist information is currently unavailable.",
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


