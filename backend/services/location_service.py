from backend.tables.location import City, Country
from backend import db

# location_service acts as a way to interact with the database's location tables (City and Country).



    # SETTERS



def setCountry(country_code: str, country_name: str):

        country = Country.query.filter_by(country_code=country_code).first()

        if country is None:
            country = Country(
                country_code=country_code,
                country_name=country_name
            )
            db.session.add(country)
            db.session.flush()
            
        return country



def setCity(city_name: str, country_code: str):
        print(f"[setCity] Called for {city_name}, {country_code}")
        city = City.query.filter_by(
            city_name=city_name,
            country_code=country_code,
        ).first()
        print(f"[setCity] Found existing city: {city is not None}")

        if city is None:
            print(f"[setCity] Creating new city record")
            city = City(
                city_name=city_name,
                country_code=country_code
            )
            db.session.add(city)
            db.session.flush()
            print(f"[setCity] New city created with ID: {city.id}")

        return city



def setCityKey(city_name: str, country_code: str, cityKey: str):
        city = setCity(city_name, country_code)
        if city.cityKey != cityKey:
            city.cityKey = cityKey
            db.session.flush()
        return city

# GETTERS



def getCityById(cityId: int):
        return db.session.get(City, cityId)



def getCountryByCode(country_code: str):
        return Country.query.filter_by(country_code=country_code).first()



def getCityByCityKey(cityKey: str):
        city = City.query.filter_by(cityKey=cityKey).first()
        if city is None:
            return None, None
        return city.city_name, city.country_code



def getCityByNameAndCountryCode(city_name: str, country_code: str):
        print(f"[getCityByNameAndCountryCode] Querying for {city_name}, {country_code}")
        result = City.query.filter_by(
            city_name=city_name,
            country_code=country_code,
        ).first()
        print(f"[getCityByNameAndCountryCode] Result: {result is not None}")
        return result

