# all methods in main are to allow front end to access the backend and get data from the soundcharts api
from api import sc

def dashboard():
    # dashboard calls all needed methods for info

    # first: makes user search for artist and choose city
        # if artist does not exist, pop up error and try again
    # second: once artist is found, dashboard should automatically ask for information from API based on artist and city
    # find ways in backend to minimize API calls