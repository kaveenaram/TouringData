from backend.api import sc
from datetime import date
import sys

# please add in what to do with error codes



class SoundchartsError(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(message)


import sys

def _handleError(error: SoundchartsError):
    print(f"\n[Soundcharts Service Error] {error.status_code} - {error.message}")
    raise error


def _getItems(call):
    payload = None
    try:
        payload = call()
    except Exception as error:
        status_code = getattr(error, "status_code", None)
        response = getattr(error, "response", None)
        if status_code is None and response is not None:
            status_code = getattr(response, "status_code", None)

        if status_code in (401, 403, 404):
            _handleError(SoundchartsError(status_code, _getErrorMessage(status_code)))
        else:
            raise

    if not payload:
        return []

    errors = payload.get("errors", []) if isinstance(payload, dict) else []
    for error in errors:
        status_code = error.get("code")
        if status_code in (401, 403, 404):
            _handleError(SoundchartsError(status_code, _getErrorMessage(status_code)))

    return payload.get("items", [])



def _getErrorMessage(status_code: int):
    messages = {
        401: "Soundcharts authentication failed. Check your API credentials.",
        403: "This Soundcharts endpoint is not included in your current plan.",
        404: "The requested Soundcharts resource was not found.",
    }
    return messages.get(status_code, "Soundcharts request failed.")



def _getPayload(call):
    try:
        payload = call()
    except Exception as error:
        status_code = getattr(error, "status_code", None)
        response = getattr(error, "response", None)
        if status_code is None and response is not None:
            status_code = getattr(response, "status_code", None)

        if status_code in (401, 403, 404):
            raise SoundchartsError(status_code, _getErrorMessage(status_code)) from error

    if not payload:
        return {}

    errors = payload.get("errors", []) if isinstance(payload, dict) else []
    for error in errors:
        status_code = error.get("code")
        if status_code in (401, 403, 404):
            raise SoundchartsError(status_code, _getErrorMessage(status_code))

    return payload  # Return the full payload



# search for artist by name
def searchByName(name: str):
    # returns max top 10 options
    try:
        print(f"[Soundcharts Service] Searching for artist by name: {name}")
        return _getItems(lambda: sc.search.search_artist_by_name(name, 0, 10))
    except SoundchartsError as error:
        _handleError(error)



# search for artist by uuid
def getArtistByUUID(uuid: str):
    # returns artist data
    try:
        print(f"[Soundcharts Service] Searching for artist by UUID: {uuid}")
        return _getItems(lambda: sc.artist.get_artist_metadata(uuid))
    except SoundchartsError as error:
        _handleError(error)



def getArtistTotalMonthlyListeners(uuid: str):
    try:
        print(f"[Soundcharts Service] Getting total monthly listeners for artist UUID: {uuid}")
        return _getItems(lambda: sc.artist.get_streaming_audience(uuid, "spotify", end_date=date.today().isoformat()))
    except SoundchartsError as error:
        _handleError(error)



# search for local streaming audience
def getLocalStreamingAudience(uuid: str):
    # returns streaming audience data with related metadata
    # returns empty dict if artist does not exist
    try:
        print(f"[Soundcharts Service] Getting local streaming audience for artist UUID: {uuid}")
        return _getPayload(lambda: sc.artist.get_local_streaming_audience(uuid, "spotify", end_date=date.today().isoformat()))
    except SoundchartsError as error:
        _handleError(error)



def getCityKey(city: str, countryCode: str):
    try:
        print(f"[Soundcharts Service] Getting city key for {city}, {countryCode}")
        return _getItems(
            lambda: sc.referential.get_cities_for_venue_festival(countryCode, city)
        )
    except SoundchartsError as error:
        _handleError(error)

   
