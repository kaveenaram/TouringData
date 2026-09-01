# all methods in main are to allow front end to access the backend and get data from the soundcharts api

from backend.repositories import artist_audience_repository, artist_repository
from backend import app, init_db
def main():
    # we will be testing the functionality of our repositories

    print("welcome")
    init_db()
    with app.app_context():
        available_artists = []

        print("yay")
        while not available_artists:
            artist = input("hello! please choose an artist:\n")
            available_artists = artist_repository.searchForArtist(artist)

            if available_artists:
                print("please choose one artist from the list")
                for i, artist in enumerate(available_artists):
                    print(f"{i+1}. {artist["name"]}, {artist["uuid"]}")
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
    return 

if __name__ == "__main__":
    main()