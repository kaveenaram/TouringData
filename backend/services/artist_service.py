from backend.tables.artist import Artist
from backend.tables.artist_audience import Artist_Audience
from datetime import datetime, timezone, timedelta
from backend import db

# artist_service acts as a way to interact with the database's artist table.

# SETTERS

"""
-----------------------------
Name
-----------------------------
Description
Use
-----------------------------
Parameters
Returns
-----------------------------
"""

def setArtist(uuid: str, name: str, slug: str, appUrl: str, imageUrl: str, monthlyListeners: str, observed_at: datetime, fetched_at: datetime):
    # check if artist is in database by uuid
    # if artist is not in database or data is outdated, create artist
    # otherwise return artist

    # due to sqllite constraints, timezone info must be naive
    if observed_at and observed_at.tzinfo:
        observed_at = observed_at.replace(tzinfo=None)
    if fetched_at and fetched_at.tzinfo:
        fetched_at = fetched_at.replace(tzinfo=None)
    
    cutoff_date = datetime.now() - timedelta(days=28)

    artist = getArtistByUUID(uuid)
    is_new_artist = artist is None

    if is_new_artist:
        artist = Artist(uuid=uuid)
        db.session.add(artist)

    if is_new_artist or artist.fetched_at is None or artist.fetched_at < cutoff_date:
        artist.name = name
        artist.slug = slug
        artist.appUrl = appUrl
        artist.imageUrl = imageUrl
        artist.monthlyListeners = monthlyListeners
        artist.observed_at = observed_at
        artist.fetched_at = fetched_at
        db.session.commit()
        db.session.refresh(artist)

    return artist

# GETTERS 

"""
-----------------------------
Name
-----------------------------
Description
Use
-----------------------------
Parameters
Returns
-----------------------------
"""

def getArtistbyName(name: str):
    # check if artist is in database by name, case insensitive
    # if artist is not in database return None
    # otherwise return artist
    artist = Artist.query.filter(Artist.name.ilike(name)).first()
    return artist

"""
-----------------------------
Name
-----------------------------
Description
Use
-----------------------------
Parameters
Returns
-----------------------------
"""

def getArtistByUUID(uuid: str):
    # check if artist is in database by uuid
    # if artist is not in database return None
    # otherwise return artist
    artist = Artist.query.filter_by(uuid=uuid).first()
    return artist

"""
-----------------------------
Name
-----------------------------
Description
Use
-----------------------------
Parameters
Returns
-----------------------------
"""

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

"""
-----------------------------
Name
-----------------------------
Description
Use
-----------------------------
Parameters
Returns
-----------------------------
"""

def getArtistImageUrl(uuid: str):
    # check if artist is in database by uuid
    # if artist is not in database return None
    # otherwise return artist image url
    artist = getArtistByUUID(uuid)
    return artist.imageUrl if artist else None

"""
-----------------------------
Name
-----------------------------
Description
Use
-----------------------------
Parameters
Returns
-----------------------------
"""

def getArtistAppUrl(uuid: str):
    # check if artist is in database by uuid
    # if artist is not in database return None
    # otherwise return artist app url
    artist = getArtistByUUID(uuid)
    return artist.appUrl if artist else None

"""
-----------------------------
Name
-----------------------------
Description
Use
-----------------------------
Parameters
Returns
-----------------------------
"""

def getArtistSlug(uuid: str):
    # check if artist is in database by uuid
    # if artist is not in database return None
    # otherwise return artist slug
    artist = getArtistByUUID(uuid)
    return artist.slug if artist else None

