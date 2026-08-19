from backend import db

class Artist_Audience(db.Model):
    uuid = db.Column(db.String(200), db.ForeignKey("Artist.uuid"))
    cityName = db.Column(db.String(200), db.ForeignKey("City.cityName"))
    localMonthlyListeners = db.Column(db.String(200), nullable=False)
