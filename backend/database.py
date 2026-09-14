import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL",
    "sqlite:///touringdata.db",
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# global limiter instance; individual routes opt into stricter limits via @limiter.limit(...)
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["200 per hour"],
)

def init_db():
    from backend.tables.artist import Artist
    from backend.tables.artist_audience import Artist_Audience
    from backend.tables.events import Events
    from backend.tables.location import City, Country
    from backend.tables.venue import Venue

    with app.app_context():
        db.create_all()


