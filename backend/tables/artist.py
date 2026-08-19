from backend import db

class Artist(db.Model):
    uuid = db.Column(db.String(200), primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), nullable=False)
    appUrl = db.Column(db.String(200), nullable=True)
    imageUrl = db.Column(db.String(200), nullable=True)
    monthlyListeners = db.Column(db.String(200), nullable=True)

    

