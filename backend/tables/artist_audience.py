from backend import db
from datetime import datetime, timezone

class Artist_Audience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist_uuid = db.Column(
        db.String(200),
        db.ForeignKey("artist.uuid"),
        nullable=False,
        index=True,
    )

    cityKey = db.Column(
        db.String(200),
        db.ForeignKey("city.cityKey"),
        nullable=False,
        index=True,
    )

    local_monthly_listeners = db.Column(
        db.String(200),
        nullable=False,
    )

    platform = db.Column(
        db.String(200),
        nullable=False,
        default="spotify",
    )

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
    
    __table_args__ = (
        db.UniqueConstraint(
            "artist_uuid",
            "cityKey",
            "platform",
            "observed_at",
            name="unique_artist_city_audience_snapshot",
        ),
    )