# all methods in main are to allow front end to access the backend and get data from the soundcharts api

from backend.repositories import artist_audience_repository, artist_repository, venue_repository
from backend.services import location_service, venue_service
from backend import app, init_db


"""
        available_artists = []

        while not available_artists:
            artist = input("hello! please choose an artist:\n")
            available_artists = artist_repository.searchForArtist(artist)

            if available_artists:
                print("please choose one artist from the list")
                for i, artist in enumerate(available_artists):
                    print(f"{i+1}. {artist["name"]}, {artist["genre"]}: ({artist["uuid"]})")
                print(f"{len(available_artists)+1}. none")

                artist = int(input("select by number: "))

                if artist == len(available_artists)+1 or artist < 1 or artist > len(available_artists):
                    print("no artist selected, please try again")
                    break
                else:
                    selectedArtist = artist_repository.selectArtist(available_artists[artist-1])

                    cities = artist_audience_repository.getAllArtistCities(selectedArtist["uuid"])
                    if not cities:
                        return print("no cities found for this artist, please try again")
                    
                    for i, c in enumerate(cities):
                        print(
                            f"{i + 1}. "
                            f"{c['cityName']}, "
                            f"{c['countryCode']}"
                        )

                    city = int(input("select city: "))
                    city = cities[city-1]
                
                    selectedCity = artist_audience_repository.selectCity(selectedArtist["uuid"], city["cityId"])

                    print(
                        f"{selectedArtist["uuid"]}: {selectedArtist["name"]}"
                        f"\nTotal monthly listeners: "
                        f"{selectedArtist["monthlyListeners"]}"
                    )

                    print(
                        f"{selectedCity["cityName"]}, "
                        f"{selectedCity["countryCode"]} "
                        f"({selectedCity["cityKey"]}): "
                        f"{selectedCity["localMonthlyListeners"]} listeners "
                        f"as of {selectedCity["observedAt"]}"
                    )

            else:
                print("no artists found, please try again")

    print("byeeeee")
"""


def testVenueRecommendations():
    # Interactive CLI to exercise the venue cache/recommendation flow end-to-end.
    available_artists = []

    while not available_artists:
        artist = input("hello! please choose an artist:\n")
        available_artists = artist_repository.searchForArtist(artist)

        if not available_artists:
            print("no artists found, please try again")
            continue

        print("please choose one artist from the list")
        for i, a in enumerate(available_artists):
            print(f"{i + 1}. {a['name']}, {a['genre']}: ({a['uuid']})")
        print(f"{len(available_artists) + 1}. none")

        choice = int(input("select by number: "))
        if choice == len(available_artists) + 1 or choice < 1 or choice > len(available_artists):
            print("no artist selected, please try again")
            available_artists = []
            continue

        selectedArtist = artist_repository.selectArtist(available_artists[choice - 1])

        cities = artist_audience_repository.getAllArtistCities(selectedArtist["uuid"])
        if not cities:
            print("no cities found for this artist, please try again")
            available_artists = []
            continue

        for i, c in enumerate(cities):
            print(f"{i + 1}. {c['cityName']}, {c['countryCode']}")

        cityChoice = int(input("select city: "))
        city = cities[cityChoice - 1]

        print(f"\nLoading venues for {city['cityName']}, {city['countryCode']} "
              f"(this calls Apify on a cache miss and may take a moment)...\n")

        result = venue_repository.findBestVenuesForArtist(
            selectedArtist["uuid"], city["cityId"]
        )

        if isinstance(result, dict) and "error" in result:
            print(f"Error: {result['error']}")
            return

        print(f"Target capacity range: {result['minCapacity']}-{result['maxCapacity']}")
        print(f"Expected attendance: {result['expectedAttendance']}\n")

        if not result["venues"]:
            print("No matching venues found in this range.")
            return

        for i, v in enumerate(result["venues"]):
            print(f"{i + 1}. {v['name']} - capacity {v['capacity']} "
                  f"({v['address'] or 'address unknown'}, {v['region'] or ''})")

        # print all information from the venue table about the selected venues
        for i, v in enumerate(result["venues"]):
            print(f"\nVenue {i + 1}:")
            for key, value in v.items():
                print(f"{key}: {value}")



def displayTorontoVenues():
    """Ensures Toronto's venue cache is loaded, then prints every cached venue and its capacity."""
    location_service.setCountry("CA", "Canada")
    city = location_service.setCity("Toronto", "CA")

    loadResult = venue_repository.ensureCityVenuesLoaded(city.id, "Toronto", "CA")
    if isinstance(loadResult, dict) and "error" in loadResult:
        print(f"Error loading venues: {loadResult['error']}")
        return

    venues = venue_service.getVenuesByCity(city.id)
    if not venues:
        print("No venues found for Toronto.")
        return

    print(f"{len(venues)} venue(s) found in Toronto:\n")
    for v in venues:
        capacity = v.capacity if v.capacity else "unknown"
        print(f"- {v.name}: capacity {capacity}")


def main():
    init_db()
    with app.app_context():
        displayTorontoVenues()

    print("byeeeee")


if __name__ == "__main__":
    main()
