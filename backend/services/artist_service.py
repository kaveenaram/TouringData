from tables.artist import Artist
from tables.artist_audience import Artist_Audience
from datetime import datetime, timezone, timedelta
from backend import db
from location_service import Location_Service

# artist_service acts as a way to interact with the database's artist table.

# SETTERS

# set artist
def setArtist(uuid: str, name: str, slug: str, appUrl: str, imageUrl: str, monthlyListeners: str, observed_at: datetime, fetched_at: datetime):
    # check if artist is in database by uuid
    # if artist is not in database or data is outdated, create artist
    # otherwise return artist
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=28)
    artist = getArtistByUUID(uuid)

    if artist is None or artist.observed_at < cutoff_date:

        artist = Artist(
            uuid=uuid,
            name=name,
            slug=slug,
            appUrl=appUrl,
            imageUrl=imageUrl,
            monthlyListeners=monthlyListeners,
            observed_at=observed_at,
            fetched_at=fetched_at,
        )

        db.session.add(artist)
        db.session.commit()
        db.session.refresh(artist)

    return artist

# GETTERS 

# get artist by name
def getArtistbyName(name: str):
    # check if artist is in database by name, case insensitive
    # if artist is not in database return None
    # otherwise return artist
    artist = Artist.query.filter(Artist.name.ilike(name)).first()
    return artist

# get artist by uuid
def getArtistByUUID(uuid: str):
    # check if artist is in database by uuid
    # if artist is not in database return None
    # otherwise return artist
    artist = Artist.query.filter_by(uuid=uuid).first()
    return artist

# get artist monthly listeners by uuid
def getArtistMonthlyListeners(uuid: str):
    # check if artist is in database by uuid
    # if artist is not in database return None
    # otherwise return most recent artist monthly listeners

    cutoff_date = datetime.now(timezone.utc) - timedelta(days=28)

    artist = getArtistByUUID(uuid)
    if artist is None:
        return None
    else:
        if artist.observed_at >= cutoff_date:
            return artist.monthlyListeners
        else:
            return None

# get artist image url by uuid
def getArtistImageUrl(uuid: str):
    # check if artist is in database by uuid
    # if artist is not in database return None
    # otherwise return artist image url
    artist = getArtistByUUID(uuid)
    return artist.imageUrl if artist else None

# get artist app url by uuid
def getArtistAppUrl(uuid: str):
    # check if artist is in database by uuid
    # if artist is not in database return None
    # otherwise return artist app url
    artist = getArtistByUUID(uuid)
    return artist.appUrl if artist else None

# get artist slug by uuid
def getArtistSlug(uuid: str):
    # check if artist is in database by uuid
    # if artist is not in database return None
    # otherwise return artist slug
    artist = getArtistByUUID(uuid)
    return artist.slug if artist else None

