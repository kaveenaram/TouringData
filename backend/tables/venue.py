from backend import db

class Venue(db.Model):
    venue_uuid = db.Column(db.String(200), primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    cityName = db.Column(db.String(200), db.ForeignKey("City.cityName"))
    countryCode = db.Column(db.String(200), db.ForeignKey("Country.countryCode"))
    capacity = db.Column(db.String(200), nullable=False)
    imageUrl = db.Column(db.String(200), nullable=True)
    type = db.Column(db.String(200), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    websiteUrl = db.Column(db.String(200), nullable=True)
    region = db.Column(db.String(200), nullable=True)