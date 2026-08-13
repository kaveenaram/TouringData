import os
import requests
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

SOUNDCHARTS_API_ID = os.getenv("SOUNDCHARTS_API_ID")
SOUNDCHARTS_API_KEY = os.getenv("SOUNDCHARTS_API_KEY")
SOUNDCHARTS_API_URL = os.getenv("SOUNDCHARTS_API_BASE_URL", "https://customer.api.soundcharts.com")

# soundcharts client allows us to access the api, returns JSON
from soundcharts.client import SoundchartsClient
sc = SoundchartsClient(api_id=SOUNDCHARTS_API_ID, api_key=SOUNDCHARTS_API_KEY)