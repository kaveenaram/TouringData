"use client"

import { useState } from "react"
import SearchInput from "../../components/search-input"
import ArtistResultsList from "../../components/artist-results-list"
import CitySelectDropdown from "../../components/city-select-dropdown"
import DashboardHeader from "../../components/dashboard-header"
import DashboardArtistInfo from "../../components/dashboard-artist-info"
import DashboardCityInfo from "../../components/dashboard-city-info"
import VenuePreview from "../../components/venue-preview"
import Loading from "../../components/loading"
import DashboardTouringInfo from "../../components/dashboard-touring-info"
import VenueInfo from "../../components/venue-info"


const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000/api"

export default function Home() {
  const [query, setQuery] = useState("")
  const [artists, setArtists] = useState([])

  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  const [selectedArtist, setSelectedArtist] = useState(null)
  const [cities, setCities] = useState([])
  const [selectedCity, setSelectedCity] = useState(null)

  const [venues, setVenues] = useState([])
  const [venuesLoading, setVenuesLoading] = useState(false)
  const [venuesError, setVenuesError] = useState("")

  const [citiesLoading, setCitiesLoading] = useState(false)
  const [citiesError, setCitiesError] = useState("")


  // ==========================================
  // SEARCH FOR ARTISTS
  // ==========================================

  async function handleSearch(event) {
    event.preventDefault()

    const name = query.trim()

    if (!name) {
      setArtists([])
      return
    }

    setLoading(true)
    setError("")

    try {
      const response = await fetch(
        `${API_URL}/artists/search?name=${encodeURIComponent(name)}`
      )

      const data = await response.json()

      if (!response.ok || !Array.isArray(data)) {
        throw new Error(data.error || "Search failed")
      }

      setArtists(data)
    } catch (err) {
      setError(
        getFriendlyError(
          err,
          "We couldn't load the search results. Please try again."
        )
      )
    } finally {
      setLoading(false)
    }
  }


  // ==========================================
  // SELECT ARTIST
  //
  // IMPORTANT:
  // Artist loading and city loading are now
  // completely separate.
  // ==========================================

  async function handleArtistSelect(artist) {
    setLoading(true)
    setError("")

    // Clear previous artist/city information
    setSelectedCity(null)
    setCities([])
    setCitiesError("")
    setCitiesLoading(false)

    try {
      const response = await fetch(
        `${API_URL}/artists/select`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(artist),
        }
      )

      const data = await response.json()

      if (!response.ok) {
        throw new Error(
          data.error || "Could not select artist"
        )
      }

      // ==========================================
      // IMPORTANT:
      // Show the artist immediately.
      // We do NOT wait for cities.
      // ==========================================

      setSelectedArtist(data)

      setArtists([])
      setQuery("")

      setLoading(false)

      // ==========================================
      // NOW load cities separately
      // ==========================================

      loadCities(artist.uuid)

    } catch (err) {
      setError(
        getFriendlyError(
          err,
          "We couldn't load this artist. Please try again."
        )
      )

      setSelectedArtist(null)
      setCities([])
      setSelectedCity(null)
      setCitiesLoading(false)

      setLoading(false)
    }
  }


  // ==========================================
  // LOAD CITIES
  //
  // This function is intentionally independent
  // from artist selection.
  // ==========================================

  async function loadCities(artistUuid) {
    setCitiesLoading(true)
    setCitiesError("")
    setCities([])

    try {
      const response = await fetch(
        `${API_URL}/artists/${artistUuid}/cities`
      )

      // Don't assume the response is JSON.
      const text = await response.text()

      let data

      try {
        data = JSON.parse(text)
      } catch {
        throw new Error("Could not load cities")
      }

      if (!response.ok) {
        throw new Error(
          data?.error || "Could not load cities"
        )
      }

      if (!Array.isArray(data)) {
        throw new Error("Could not load cities")
      }

      // Cities successfully loaded.
      setCities(data)

    } catch (err) {
      console.error("City loading error:", err)

      // IMPORTANT:
      // This does NOT affect selectedArtist.
      // The user stays on the artist dashboard.

      setCities([])
      setCitiesError(
        "No specific city data available."
      )

    } finally {
      setCitiesLoading(false)
    }
  }

  // ==========================================
  // LOAD VENUES
  // ==========================================

  async function loadVenues(artistuuid, cityId) {
  setVenuesLoading(true)
  setVenuesError("")
  setVenues([])

  try {
    const response = await fetch(
      `${API_URL}/venues/recommend?artist_id=${encodeURIComponent(
        artistuuid
      )}&city_id=${encodeURIComponent(cityId)}`
    )

    const text = await response.text()

    let data

    try {
      data = JSON.parse(text)
    } catch {
      throw new Error("Could not load venues")
    }

    if (!response.ok) {
      throw new Error(data?.error || "Could not load venues")
    }

    setVenues(data.venues || [])

  } catch (err) {
    console.error("Venue loading error:", err)

    setVenues([])
    setVenuesError("No recommended venues available.")
  } finally {
    setVenuesLoading(false)
  }
}

  // ==========================================
  // SELECT CITY
  // ==========================================

  async function handleCitySelect(city) {
    setSelectedCity(null)
    setVenues([])
    setVenuesError("")

    if (!selectedArtist) {
      return
    }

    setLoading(true)
    setError("")

    try {
      const response = await fetch(
        `${API_URL}/artists/${selectedArtist.uuid}/cities/${city.cityId}/audience`
      )

      const text = await response.text()

      let audienceData

      try {
        audienceData = JSON.parse(text)
      } catch {
        throw new Error("Could not load city data")
      }

      if (!response.ok) {
        throw new Error(
          audienceData?.error || "Could not load city data"
        )
      }

      setSelectedCity(audienceData)
      loadVenues(selectedArtist.uuid, city.cityId)

    } catch (err) {
      console.error("City audience error:", err)

      setError(
        getFriendlyError(
          err,
          "We couldn't load the data for this city. Please try again."
        )
      )

    } finally {
      setLoading(false)
    }
  }

  

  // ==========================================
  // BACK TO SEARCH
  // ==========================================

  function handleBackToSearch() {
    setSelectedArtist(null)
    setCities([])
    setSelectedCity(null)

    setVenues([])
    setVenuesLoading(false)
    setVenuesError("")

    setCitiesLoading(false)
    setCitiesError("")

    setError("")
    setArtists([])
    setQuery("")
  } 


  // ==========================================
  // FRIENDLY ERRORS
  // ==========================================

  function getFriendlyError(error, fallback) {
    const message = error?.message?.toLowerCase() || ""

    if (message.includes("failed to fetch")) {
      return "We couldn't connect to the server. Please try again."
    }

    if (message.includes("search failed")) {
      return "We couldn't search for that artist. Please try again."
    }

    if (message.includes("select artist")) {
      return "We couldn't load that artist. Please try again."
    }

    if (message.includes("load cities")) {
      return "We couldn't load the available cities. Please try again."
    }

    if (message.includes("city data")) {
      return "We couldn't load the data for this city. Please try again."
    }

    return fallback
  }


  // ==========================================
  // RENDER
  // ==========================================

  return (
    <main className="app">

      {/* =====================================
          SEARCH
          ===================================== */}

      {!selectedArtist && (
        <section className="app__search">

          <h1 className="app__title">
            touring data
          </h1>

          <p className="app__description">
            discover where your favorite artists are heard, explore listener data by
            city, and find the venues that could bring them to your audience
            </p>

          <SearchInput
            value={query}
            onChange={setQuery}
            onSubmit={handleSearch}
            loading={loading}
          />

          <ArtistResultsList
            artists={artists}
            loading={loading}
            error={error}
            onSelect={handleArtistSelect}
          />

        </section>
      )}


      {/* =====================================
          ARTIST DASHBOARD
          ===================================== */}

      {selectedArtist && (
        <section className="app__dashboard">

          <DashboardHeader
            onBack={handleBackToSearch}
            backText="go back to search"
          />


          {/* Artist information appears immediately */}

          <DashboardArtistInfo
            artist={selectedArtist}
          />


          {/* =================================
              CITY DATA
              ================================= */}

          {citiesLoading && (
            <p className="app__loading">
              Loading city data...
            </p>
          )}


          {!citiesLoading && cities.length > 0 && (
            <div className="app__city-section">

              {selectedCity && (
                <p className="app__city-prompt">
                  Want to look for another city for this artist?
                </p>
              )}

              <CitySelectDropdown
                cities={cities}
                onSelect={handleCitySelect}
                disabled={loading}
                label={
                  selectedCity
                    ? "Select another city"
                    : "Select a city"
                }
              />

            </div>
          )}


          {/* =================================
              NO CITY DATA
              ================================= */}

          {!citiesLoading &&
            cities.length === 0 &&
            citiesError && (
              <p className="app__info">
                No specific city data available.
              </p>
          )}


          {/* =================================
              SELECTED CITY
              ================================= */}

          {selectedCity && (
            <>
              <DashboardCityInfo
                artist={selectedArtist}
                city={selectedCity}
              />

              {/* VENUES */}

               
              <section className="venue-section">

                {venuesLoading && (
                  <Loading />
                )}

                {!venuesLoading && venuesError && (
                  <p className="app__info">
                    {venuesError}
                  </p>
                )}

                {!venuesLoading && !venuesError && venues.length > 0 && (
                  <div className="venue-grid">
                    {venues.map((venue) => (
                      <VenueInfo
                        key={venue.venueID}
                        venue={venue}
                        cityName={selectedCity.name}
                      />
                    ))}
                  </div>
                )}

              </section>
            </>
          )}


          {/* =================================
              CITY/API ERROR
              ================================= */}

          {error && (
            <p className="app__error">
              {error}
            </p>
          )}

        </section>
      )}

    </main>
  )
}