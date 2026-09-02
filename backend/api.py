import os
from pathlib import Path
from flask_cors import CORS
from soundcharts import SoundchartsClient
from dotenv import load_dotenv
from .routes import artists_bp

load_dotenv(Path(__file__).with_name(".env"))  # Load environment variables from .env file

# TESTING

from backend import app, init_db

CORS(app)
init_db()

# initialize the soundchards client with the API credentials from environment variables

SOUNDCHARTS_API_ID = os.getenv("SOUNDCHARTS_API_ID")
SOUNDCHARTS_API_KEY = os.getenv("SOUNDCHARTS_API_KEY")
SOUNDCHARTS_API_URL = os.getenv("SOUNDCHARTS_API_BASE_URL", "https://customer.api.soundcharts.com")

# soundcharts client allows us to access the api, returns JSON
sc = SoundchartsClient(app_id=SOUNDCHARTS_API_ID, api_key=SOUNDCHARTS_API_KEY)

app.register_blueprint(artists_bp)