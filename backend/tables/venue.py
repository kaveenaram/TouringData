from backend import db

# update later based on new ticketmaster api

class Venue(db.Model):
    venue_uuid = db.Column(db.String(200), primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey("city.id"))
    country_code = db.Column(db.String(10), db.ForeignKey("country.country_code"))
    capacity = db.Column(db.String(200), nullable=False)
    imageUrl = db.Column(db.String(200), nullable=True)
    type = db.Column(db.String(200), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    websiteUrl = db.Column(db.String(200), nullable=True)
    region = db.Column(db.String(200), nullable=True)