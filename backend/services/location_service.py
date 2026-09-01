from backend.tables.location import City, Country
from backend import db

# location_service acts as a way to interact with the database's location tables (City and Country).



    # SETTERS

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

def setCity(city_name: str, country_code: str):

        city = City.query.filter_by(
            city_name=city_name,
            country_code=country_code,
        ).first()

        if city is None:
            city = City(
                city_name=city_name,
                country_code=country_code
            )
            db.session.add(city)
            db.session.flush()

        return city

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

def setCityKey(city_name: str, country_code: str, cityKey: str):
        city = setCity(city_name, country_code)
        if city.cityKey != cityKey:
            city.cityKey = cityKey
            db.session.flush()
        return city

# GETTERS

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

def getCityById(cityId: int):
        return db.session.get(City, cityId)

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

def getCountryByCode(country_code: str):
        return Country.query.filter_by(country_code=country_code).first()

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

def getCityByCityKey(cityKey: str):
        city = City.query.filter_by(cityKey=cityKey).first()
        if city is None:
            return None, None
        return city.city_name, city.country_code

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

def getCityByNameAndCountryCode(city_name: str, country_code: str):
        return City.query.filter_by(
            city_name=city_name,
            country_code=country_code,
        ).first()

