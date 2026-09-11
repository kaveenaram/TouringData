from backend import db

class Country(db.Model):
    country_code = db.Column(db.String(10), primary_key=True)
    country_name = db.Column(db.String(200), nullable=False)


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cityKey = db.Column(db.String(200), unique=True, nullable=True, index=True)
    city_name = db.Column(db.String(200), nullable=False)
    country_code = db.Column(
        db.String(10),
        db.ForeignKey("country.country_code"),
        nullable=False,
    )

