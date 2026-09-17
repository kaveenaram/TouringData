# touring data

a small touring research tool for artists, cities, audiences, and potential venues.

the app lets you search for an artist, explore where their listeners are located, select a city, and see an estimated attendance range alongside venue recommendations that fit that audience.

---

## current functionality

- search for artists
- select an artist and view their information
- view cities where the artist has listener data
- select a city to view local audience information
- calculate an estimated attendance range based on local monthly listeners
- recommend venues based on the estimated attendance
- display venue images, addresses, and capacities
- filter venue recommendations by capacity
- provide a fallback message for very small expected audiences
- navigate back to the artist search without refreshing the page

---

## project structure

### frontend

the frontend is built with next.js and react.

it handles:

- artist search and selection
- city selection
- displaying audience information
- displaying expected attendance
- showing recommended venues
- loading and error states
- the overall visual design and layout

the frontend communicates with the backend through the api.

### backend

the backend is built with python, flask, and sqlalchemy. it handles the data processing, api routes, database access, and external api integrations.

the backend is organized into a few main areas:

```text
backend/
├── repositories/
├── services/
├── tables/
├── api.py
├── database.py
├── main.py
├── routes.py
└── requirements.txt
```
---

## venue recommendations

the current venue recommendation logic uses the artist's local monthly listener count to estimate how many people might attend a show.
the estimated attendance is based on a 2%–4% range of local monthly listeners.

## testing notes

toronto has been the main city used for testing the venue selection and recommendation system.
venue selection for cities outside of toronto hasn't been tested as thoroughly yet because i ran out of api credits :(
because of this, some venue data or recommendations in other cities may not behave exactly as expected.

## known limitations

external api data can vary in availability and accuracy.
venue data is dependent on the external data sources.
venue recommendations outside of toronto have not been thoroughly tested.
api usage is limited by available credits.
some edge cases with very small audiences may require further testing.

## running the project

download from the development branch
install docker
navigate to main folder TouringData
docker compose up

