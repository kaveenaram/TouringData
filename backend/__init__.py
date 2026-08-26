from .database import app, db
from .database import init_db

init_db()

__all__ = ["app", "db"]
