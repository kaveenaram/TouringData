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

    city_id = db.Column(
        db.Integer,
        db.ForeignKey("city.id"),
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
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
    )

    fetched_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
    )
    
    __table_args__ = (
        db.UniqueConstraint(
            "artist_uuid",
            "city_id",
            "platform",
            "observed_at",
            name="unique_artist_city_audience_snapshot",
        ),
    )