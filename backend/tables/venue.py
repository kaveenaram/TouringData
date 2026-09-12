from backend import db

class Venue(db.Model):
    venue_uuid = db.Column(db.String(200), primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey("city.id"))
    country_code = db.Column(db.String(10), db.ForeignKey("country.country_code"))
    capacity = db.Column(db.String(200), nullable=True)  # nullable: Apify doesn't always report capacity
    imageUrl = db.Column(db.String(200), nullable=True)
    type = db.Column(db.String(200), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    websiteUrl = db.Column(db.String(200), nullable=True)
    region = db.Column(db.String(200), nullable=True)
    postal_code = db.Column(db.String(50), nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)