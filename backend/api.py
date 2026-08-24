import os
from flask_cors import CORS
from soundcharts import SoundchartsClient
from dotenv import load_dotenv
from backend import app

load_dotenv()  # Load environment variables from .env file

CORS(app)

# initialize the soundchards client with the API credentials from environment variables

SOUNDCHARTS_API_ID = os.getenv("SOUNDCHARTS_API_ID")
SOUNDCHARTS_API_KEY = os.getenv("SOUNDCHARTS_API_KEY")
SOUNDCHARTS_API_URL = os.getenv("SOUNDCHARTS_API_BASE_URL", "https://customer.api.soundcharts.com")

# soundcharts client allows us to access the api, returns JSON
sc = SoundchartsClient(api_id=SOUNDCHARTS_API_ID, api_key=SOUNDCHARTS_API_KEY)

# needs to initialize ticketmaster api as well for venues