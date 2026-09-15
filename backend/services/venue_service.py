from sqlalchemy import cast, Integer
from backend import db
from backend.tables.venue import Venue

def getVenueByID(venueID: str):
    return db.session.get(Venue, venueID)

def getVenuesByCity(cityId: int):
    return Venue.query.filter_by(city_id=cityId).all()

def getVenuesByCityAndCapacity(cityId: int, minCapacity: int, maxCapacity: int):
    return (
        Venue.query
        .filter(Venue.city_id == cityId)
        .filter(Venue.capacity.isnot(None))
        .filter(Venue.capacity != "")
        .filter(~Venue.name.ilike("%parking%"))
        .filter(~Venue.name.ilike("%parking lot%"))
        .filter(~Venue.name.ilike("%parking garage%"))
        .filter(cast(Venue.capacity, Integer) >= minCapacity)
        .filter(cast(Venue.capacity, Integer) <= maxCapacity)
        .all()
    )

def setVenue(venueID, name, cityId, countryCode, capacity, address=None,
                 region=None, postalCode=None, latitude=None, longitude=None):
    venue = getVenueByID(venueID)

    if venue is None:
        venue = Venue(venue_id=venueID)
        db.session.add(venue)

    venue.name = name
    venue.city_id = cityId
    venue.country_code = countryCode
    venue.capacity = str(capacity) if capacity not in (None, "") else None
    venue.address = address
    venue.region = region
    venue.postal_code = postalCode
    venue.latitude = latitude
    venue.longitude = longitude

    return venue

def bulkSetVenues(venues: list):
    saved = [setVenue(**v) for v in venues]
    db.session.flush()
    return saved

def setVenueImageURL(venueID: str, imageUrl: str):
    venue = getVenueByID(venueID)
    if venue is None:
        return None
    venue.imageUrl = imageUrl
    db.session.commit()
    return venue