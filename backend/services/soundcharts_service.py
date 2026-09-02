from backend.api import sc
from datetime import date
import sys

# please add in what to do with error codes

"""
-----------------------------
Name
-----------------------------
Description
Use
-----------------------------
Parameters
Returns
-----------------------------
"""

class SoundchartsError(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(message)


import sys

def _handleError(error: SoundchartsError):
    """Handle SoundchartsError gracefully and exit"""
    print(f"\n[Soundcharts Service Error] {error.status_code} - {error.message}")
    print("[Soundcharts Service] Ending application gracefully...")
    sys.exit(1)

"""
-----------------------------
Name
-----------------------------
Description
Use
-----------------------------
Parameters
Returns
-----------------------------
"""

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

"""
-----------------------------
Name
-----------------------------
Description
Use
-----------------------------
Parameters
Returns
-----------------------------
"""

def _getErrorMessage(status_code: int):
    messages = {
        401: "Soundcharts authentication failed. Check your API credentials.",
        403: "This Soundcharts endpoint is not included in your current plan.",
        404: "The requested Soundcharts resource was not found.",
    }
    return messages.get(status_code, "Soundcharts request failed.")

"""
-----------------------------
Name
-----------------------------
Description
Use
-----------------------------
Parameters
Returns
-----------------------------
"""

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

"""
-----------------------------
Name
-----------------------------
Description
Use
-----------------------------
Parameters
Returns
-----------------------------
"""

# search for artist by name
def searchByName(name: str):
    # returns max top 10 options
    try:
        return _getItems(lambda: sc.search.search_artist_by_name(name, 0, 10))
    except SoundchartsError as error:
        _handleError(error)

"""
-----------------------------
Name
-----------------------------
Description
Use
-----------------------------
Parameters
Returns
-----------------------------
"""

# search for artist by uuid
def getArtistByUUID(uuid: str):
    # returns artist data
    try:
        return _getItems(lambda: sc.artist.get_artist_metadata(uuid))
    except SoundchartsError as error:
        _handleError(error)

"""
-----------------------------
Name
-----------------------------
Description
Use
-----------------------------
Parameters
Returns
-----------------------------
"""

def getArtistTotalMonthlyListeners(uuid: str):
    try:
        return _getItems(lambda: sc.artist.get_streaming_audience(uuid, "spotify", end_date=date.today().isoformat()))
    except SoundchartsError as error:
        _handleError(error)

"""
-----------------------------
Name
-----------------------------
Description
Use
-----------------------------
Parameters
Returns
-----------------------------
"""

# search for local streaming audience
def getLocalStreamingAudience(uuid: str):
    # returns streaming audience data with related metadata
    # returns empty dict if artist does not exist
    try:
        return _getPayload(lambda: sc.artist.get_local_streaming_audience(uuid, "spotify", end_date=date.today().isoformat()))
    except SoundchartsError as error:
        _handleError(error)

"""
-----------------------------
Name
-----------------------------
Description
Use
-----------------------------
Parameters
Returns
-----------------------------
"""

def getCityKey(city: str, countryCode: str):
    try:
        return _getItems(
            lambda: sc.referential.get_cities_for_venue_festival(countryCode, city)
        )
    except SoundchartsError as error:
        _handleError(error)

   
