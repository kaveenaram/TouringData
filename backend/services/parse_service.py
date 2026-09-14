import os
import requests

PARSE_API_KEY = os.getenv("PARSE_API_KEY")
PARSE_SCRAPER_ID = os.getenv("PARSE_SCRAPER_ID", "2f8af6ad-0d75-4c4f-a0e0-1a22caa8307b")
PARSE_BASE_URL = "https://api.parse.bot/scraper"


class ParseError(Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message
        super().__init__(message)


def searchVenuesByCity(city, state=None, country_code=None, page=1, page_size=100,
                        radius_km=None, min_capacity=None, max_capacity=None):
    """Calls one page of search_venues_by_city and returns the response's "data" object."""
    if not PARSE_API_KEY:
        raise ParseError(500, "PARSE_API_KEY is not configured.")

    params = {"city": city, "page": page, "page_size": page_size}
    if state:
        params["state"] = state
    if country_code:
        params["country_code"] = country_code
    if radius_km is not None:
        params["radius_km"] = radius_km
    if min_capacity is not None:
        params["min_capacity"] = min_capacity
    if max_capacity is not None:
        params["max_capacity"] = max_capacity

    try:
        response = requests.get(
            f"{PARSE_BASE_URL}/{PARSE_SCRAPER_ID}/search_venues_by_city",
            headers={"X-API-Key": PARSE_API_KEY},
            params=params,
            timeout=15,
        )
    except requests.RequestException as error:
        raise ParseError(502, f"Parse request failed: {error}") from error

    if response.status_code != 200:
        raise ParseError(response.status_code, f"Parse API returned {response.status_code}")

    payload = response.json()
    if payload.get("status") != "success":
        raise ParseError(502, "Parse API returned an unexpected response.")

    return payload["data"]


def searchAllVenuesByCity(city, state=None, country_code=None, radius_km=None,
                           min_capacity=0, max_capacity=100000, page_size=100, max_pages=10):
    """Paginates search_venues_by_city until has_more is false or max_pages is reached."""
    venues = []
    page = 1

    while page <= max_pages:
        data = searchVenuesByCity(
            city, state=state, country_code=country_code, page=page,
            page_size=page_size, radius_km=radius_km,
            min_capacity=min_capacity, max_capacity=max_capacity,
        )
        venues.extend(data.get("venues", []))

        if not data.get("has_more"):
            break
        page += 1

    return venues
