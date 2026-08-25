from tables.location import City, Country
from backend import db

# location_service acts as a way to interact with the database's location tables (City and Country).

class Location_Service:

    # SETTERS

    def setCountry(country_code: str, country_name: str):

        country = Country.query.filter_by(country_code=country_code).first()

        if country is None:
            country = Country(
                country_code=country_code,
                country_name=country_name
            )
            db.session.add(country)
            db.session.commit()
            db.session.refresh(country)

        return country

    def setCity(cityKey: str, city_name: str, country_code: str):

        city = City.query.filter_by(
            cityKey=cityKey,
            city_name=city_name,
            country_code=country_code,
        ).first()

        if city is None:
            city = City(cityKey=cityKey,
                city_name=city_name,
                country_code=country_code
            )
            db.session.add(city)
            db.session.commit()
            db.session.refresh(city)

        return city

    # GETTERS

    def getCountryByCode(country_code: str):
        return Country.query.filter_by(country_code=country_code).first()

    def getCityByNameAndCountryCode(city_name: str, country_code: str):
        return City.query.filter_by(
            city_name=city_name,
            country_code=country_code,
        ).first()

    def getCityNameAndCountryNameByCityId(city_id: str):
        city = db.session.get(City, city_id)
        if city is None:
            return None, None
        country = Country.query.filter_by(country_code=city.country_code).first()
        if country is None:
            return city.city_name, None
        return city.city_name, country.country_name

