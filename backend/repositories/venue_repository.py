from backend import db
from backend.services import soundcharts_service, venue_service, location_service, parse_service
from backend.repositories import artist_audience_repository

MIN_ATTENDANCE_PCT = 0.02
MAX_ATTENDANCE_PCT = 0.04
DEFAULT_RESULT_LIMIT = 3

# floor to drop unpublished/junk capacities (e.g. "capacity: 1") at ingestion time
MIN_STORABLE_CAPACITY = 5


def ensureCityVenuesLoaded(cityId: int, cityName: str, countryCode: str):


    if location_service.cityHasVenuesLoaded(cityId):
        return {"cached": True, "venuesLoaded": 0}

    try:
        venues = parse_service.searchAllVenuesByCity(
            cityName, country_code=countryCode, min_capacity=MIN_STORABLE_CAPACITY
        )
    except parse_service.ParseError as error:
        # IMPORTANT: do not mark the city loaded on failure
        return {"statusCode": error.status_code, "error": error.message}

    venuesByID = {}
    for venue in venues:
        if not isinstance(venue, dict):
            continue

        venueID = venue.get("id")
        name = venue.get("name")
        if venueID is None or not name:
            # can't identify a venue without an id/name - skip safely
            continue

        capacity = venue.get("capacity")
        if capacity is None or capacity < MIN_STORABLE_CAPACITY:
            continue

        venuesByID[str(venueID)] = {
            "venueID": str(venueID),
            "name": name,
            "cityId": cityId,
            "countryCode": venue.get("countryCode") or countryCode,
            "capacity": capacity,
            "address": venue.get("address1"),
            "region": venue.get("state"),
            "postalCode": venue.get("postalCode"),
            "latitude": venue.get("latitude"),
            "longitude": venue.get("longitude"),
        }

    try:
        venue_service.bulkSetVenues(list(venuesByID.values()))
        location_service.markCityVenuesLoaded(cityId)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    # zero venues found is still a successful, cacheable outcome
    return {"cached": False, "venuesLoaded": len(venuesByID)}


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
    if country is None:
        return {"statusCode": 404, "error": "Country not found for this city"}

    loadResult = ensureCityVenuesLoaded(cityId, city.city_name, city.country_code)
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
                "venueID": v.venue_id,
                "name": v.name,
                "capacity": int(v.capacity) if v.capacity else None,
                "address": v.address,
                "region": v.region,
                "postalCode": v.postal_code,
                "latitude": v.latitude,
                "longitude": v.longitude,
                "cityId": v.city_id,
                "countryCode": v.country_code,
                "imageUrl": findVenueImageURL(v.venue_id),
            }
            for v in ranked
        ],
    }

def findVenueMetadataByName(venue_name: str):
    try:
        return soundcharts_service.getVenueMetadataByName(venue_name)
    except Exception as error:
        return {"statusCode": 500, "error": str(error)}

def findVenueImageURL(venue_id: str):
    venue = venue_service.getVenueByID(venue_id)
    if venue is None:
        return None

    if venue.imageUrl:
        return venue.imageUrl

    city = location_service.getCityById(venue.city_id)
    if city is None:
        return None

    payload = findVenueMetadataByName(venue.name)
    if isinstance(payload, dict) and "error" in payload:
        return None
    if not payload:
        return None

    # we have to confirm that the image belongs to the correct venue based on city and country
    for item in payload:
        if (
            item.get("imageUrl")
            and item.get("cityName", "").strip().lower() == city.city_name.strip().lower()
            and item.get("countryCode") == venue.country_code
        ):
            imageURL = item.get("imageUrl")
            venue_service.setVenueImageURL(venue_id, imageURL)
            return imageURL
        
    return None