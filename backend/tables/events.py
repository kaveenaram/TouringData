from backend import db

class Events(db.Model):
    event_uuid = db.Column(db.String(200), primary_key=True)
    artist_uuid = db.Column(db.String(200), db.ForeignKey("Artist.uuid"))
    cityName = db.Column(db.String(200), db.ForeignKey("City.cityName"))
    venue_uuid = db.Column(db.String(200), db.ForeignKey("Venue.venue_uuid"))