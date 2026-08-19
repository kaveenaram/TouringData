from backend import db

class Country(db.Model):
    countryCode = db.Column(db.String(200), primary_key=True)
    countryName = db.Column(db.String(200), nullable=False)

class City(db.Model):
    cityName = db.Column(db.String(200), primary_key=True)
    countryCode = db.Column(db.String(200), db.ForeignKey("Country.countryCode"))