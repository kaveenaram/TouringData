import os
from apify_client import ApifyClient


class ApifyError(Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message
        super().__init__(message)


APIFY_TOKEN = os.getenv("APIFY_TOKEN")
APIFY_VENUE_ACTOR_ID = os.getenv("APIFY_VENUE_ACTOR_ID", "m9qbUfZoYuKxE9fht")


def _getClient():
    if not APIFY_TOKEN:
        raise ApifyError(500, "APIFY_TOKEN is not configured.")
    return ApifyClient(APIFY_TOKEN)


def searchEventsByCity(cityName: str, countryName: str, maxItems: int = 250, maxPages: int = 0, fetchDetails: bool = True):

    client = _getClient()

    query = f"{cityName}, {countryName}" if countryName else cityName

    run_input = {
        "mode": "search",
        "query": query,
        "searchType": "cities",
        "fetchDetails": fetchDetails,
        "maxItems": maxItems,
        "maxPages": maxPages,
    }

    try:
        run = client.actor(APIFY_VENUE_ACTOR_ID).call(run_input=run_input)
    except Exception as error:
        raise ApifyError(502, f"Apify run failed: {error}") from error

    # call() returns a run object (or None on failure) with attribute access, not a dict
    if run is None or not getattr(run, "default_dataset_id", None):
        raise ApifyError(502, "Apify run did not return a dataset.")

    try:
        return list(client.dataset(run.default_dataset_id).iterate_items())
    except Exception as error:
        raise ApifyError(502, f"Could not read Apify dataset: {error}") from error
