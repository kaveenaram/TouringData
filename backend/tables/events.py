from backend import db

class Events(db.Model):
    event_uuid = db.Column(db.String(200), primary_key=True)
    artist_uuid = db.Column(db.String(200), db.ForeignKey("artist.uuid"))
    city_id = db.Column(db.Integer, db.ForeignKey("city.id"))
    venue_uuid = db.Column(db.String(200), db.ForeignKey("venue.venue_uuid"))