from backend.api import sc

# please add in what to do with error codes

class SoundchartsError(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(message)


def _getItems(call):
    try:
        payload = call()
    except Exception as error:
        status_code = getattr(error, "status_code", None)
        response = getattr(error, "response", None)
        if status_code is None and response is not None:
            status_code = getattr(response, "status_code", None)

        if status_code in (401, 403, 404):
            raise SoundchartsError(status_code, _getErrorMessage(status_code)) from error
        raise SoundchartsError(502, "Soundcharts could not be reached.") from error

    if not payload:
        return []

    errors = payload.get("errors", []) if isinstance(payload, dict) else []
    for error in errors:
        status_code = error.get("code")
        if status_code in (401, 403, 404):
            raise SoundchartsError(status_code, _getErrorMessage(status_code))

    return payload.get("items", [])


def _getErrorMessage(status_code: int):
    messages = {
        401: "Soundcharts authentication failed. Check your API credentials.",
        403: "This Soundcharts endpoint is not included in your current plan.",
        404: "The requested Soundcharts resource was not found.",
    }
    return messages.get(status_code, "Soundcharts request failed.")



# search for artist by name
def searchByName(name: str):
    # returns max top 3 options
    # returns none if search does not work
    
    return _getItems(lambda: sc.search.search_artist_by_name(name, 0, 3))


# search for artist by uuid
def getArtistByUUID(uuid: str):
    # returns artist data
    # returns none if artist does not exist
    return _getItems(lambda: sc.artist.get_artist_metadata(uuid))

def getArtistTotalMonthlyListeners(uuid: str):
    return _getItems(lambda: sc.artist.get_streaming_audience(uuid, "spotify"))


# search for local streaming audience
def getLocalStreamingAudience(uuid: str):
    # returns streaming audience data
    # returns none if artist does not exist
    return _getItems(lambda: sc.artist.get_local_streaming_audience(uuid, "spotify"))

def getCityKey(city: str, countryCode: str):
    return _getItems(
        lambda: sc.referential.get_cities_for_venue_festival(countryCode, city)
    )


   
