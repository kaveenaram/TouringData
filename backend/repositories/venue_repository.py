import re
import uuid

from backend import db
from backend.services import venue_service, location_service, apify_service
from backend.repositories import artist_audience_repository

MIN_ATTENDANCE_PCT = 0.01
MAX_ATTENDANCE_PCT = 0.03
DEFAULT_RESULT_LIMIT = 3

# fixed namespace so the same venue always resolves to the same UUID across runs
VENUE_NAMESPACE = uuid.UUID("d3b0f1f0-6f7a-4b3e-9c1a-1a2b3c4d5e6f")


def _normalizeText(text):
    if not text:
        return ""
    return re.sub(r"[^a-z0-9]+", " ", str(text).lower()).strip()


def _buildVenueUUID(name, cityName, countryCode):
    key = f"{_normalizeText(name)}|{_normalizeText(cityName)}|{_normalizeText(countryCode)}"
    return str(uuid.uuid5(VENUE_NAMESPACE, key))


def ensureCityVenuesLoaded(cityId: int, cityName: str, countryName: str, countryCode: str):
    """
    Cache gate: returns a status dict, never raises to the caller.
    """
    if location_service.cityHasVenuesLoaded(cityId):
        return {"cached": True, "venuesLoaded": 0}

    try:
        # query combines city + country name since Soundcharts/Songkick
        # cover the whole globe and a bare city name (e.g. "London") is
        # ambiguous. If testing shows a small city returning too few venues,
        # consider reading the event's metroAreaName instead of venueCity to
        # widen matching to the surrounding metro area.
        events = apify_service.searchEventsByCity(cityName, countryName)
    except apify_service.ApifyError as error:
        # IMPORTANT: do not mark the city loaded on failure
        return {"statusCode": error.status_code, "error": error.message}

    venuesByUUID = {}
    for event in events:
        if not isinstance(event, dict):
            continue

        name = event.get("venueName")
        if not name:
            # can't identify a venue without a name - skip safely
            continue

        eventCity = event.get("venueCity") or cityName
        eventCountry = event.get("venueCountry") or countryCode

        venueUUID = _buildVenueUUID(name, eventCity, eventCountry)
        if venueUUID in venuesByUUID:
            continue  # duplicate event at an already-seen venue

        venuesByUUID[venueUUID] = {
            "venueUUID": venueUUID,
            "name": name,
            "cityId": cityId,
            "countryCode": countryCode,
            "capacity": event.get("venueCapacity"),
            "address": event.get("venueStreet"),
            "region": event.get("venueRegion"),
            "postalCode": event.get("venuePostalCode"),
            "latitude": event.get("venueLatitude"),
            "longitude": event.get("venueLongitude"),
        }

    try:
        venue_service.bulkSetVenues(list(venuesByUUID.values()))
        location_service.markCityVenuesLoaded(cityId)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    # zero venues found is still a successful, cacheable outcome
    return {"cached": False, "venuesLoaded": len(venuesByUUID)}


def calculateCapacityRange(localMonthlyListeners):
    """1%-3% of local monthly listeners = expected attendance range."""
    listeners = int(localMonthlyListeners)
    minCapacity = round(listeners * MIN_ATTENDANCE_PCT)
    maxCapacity = round(listeners * MAX_ATTENDANCE_PCT)
    if maxCapacity < minCapacity:
        maxCapacity = minCapacity
    return minCapacity, maxCapacity


def findBestVenuesForArtist(artistUUID: str, cityId: int, limit=DEFAULT_RESULT_LIMIT):
    city = location_service.getCityById(cityId)
    if city is None:
        return {"statusCode": 404, "error": "City not found"}

    country = location_service.getCountryByCode(city.country_code)
    countryName = country.country_name if country else None

    loadResult = ensureCityVenuesLoaded(cityId, city.city_name, countryName, city.country_code)
    if isinstance(loadResult, dict) and "error" in loadResult:
        return loadResult

    localMonthlyListeners = artist_audience_repository.getLocalMonthlyListeners(
        artistUUID, cityId
    )
    if isinstance(localMonthlyListeners, dict) and "error" in localMonthlyListeners:
        return localMonthlyListeners
    if localMonthlyListeners is None:
        return {
            "statusCode": 404,
            "error": "No listener data available for this artist in this city",
        }

    minCapacity, maxCapacity = calculateCapacityRange(localMonthlyListeners)
    expectedAttendance = int(localMonthlyListeners) * (
        (MIN_ATTENDANCE_PCT + MAX_ATTENDANCE_PCT) / 2
    )

    candidates = venue_service.getVenuesByCityAndCapacity(cityId, minCapacity, maxCapacity)

    ranked = sorted(
        candidates,
        key=lambda v: abs(int(v.capacity) - expectedAttendance),
    )[:limit]

    return {
        "cityId": cityId,
        "cityName": city.city_name,
        "minCapacity": minCapacity,
        "maxCapacity": maxCapacity,
        "expectedAttendance": round(expectedAttendance),
        "venues": [
            {
                "venueUUID": v.venue_UUID,
                "name": v.name,
                "capacity": int(v.capacity) if v.capacity else None,
                "address": v.address,
                "region": v.region,
                "postalCode": v.postal_code,
                "latitude": v.latitude,
                "longitude": v.longitude,
                "cityId": v.city_id,
                "countryCode": v.country_code,
            }
            for v in ranked
        ],
    }