from datetime import timezone, datetime
from backend import db

class Artist(db.Model):

    uuid = db.Column(db.String(200), primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), nullable=False)
    appUrl = db.Column(db.String(200), nullable=True)
    imageUrl = db.Column(db.String(200), nullable=True)
    monthlyListeners = db.Column(db.String(200), nullable=True)
    observed_at = db.Column(
            db.DateTime(timezone=True),
            nullable=False,
            default=lambda: datetime.now(timezone.utc),
        )
    
    fetched_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )