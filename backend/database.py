import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL",
    "sqlite:///touringdata.db",
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

def init_db():
    from backend.tables.artist import Artist
    from backend.tables.artist_audience import Artist_Audience
    from backend.tables.events import Events
    from backend.tables.location import City, Country
    from backend.tables.venue import Venue

    with app.app_context():
        db.create_all()


init_db()

