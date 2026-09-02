"use client"

import { useState } from "react"
import SearchBar from "../../components/searchbar"
import SelectCity from "../../components/selectcity"

const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000/api"

export default function Home() {
  const [artist, setArtist] = useState(null)
  const [cities, setCities] = useState([])
  const [selectedCity, setSelectedCity] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  async function handleArtistSelect(searchResult) {
    setLoading(true)
    setError("")
    setArtist(null)
    setCities([])
    setSelectedCity(null)

    try {
      const artistResponse = await fetch(`${API_URL}/artists/select`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(searchResult),
      })

      const artistData = await artistResponse.json()

      if (!artistResponse.ok) {
        throw new Error(artistData.error || "Could not select artist")
      }

      setArtist(artistData)

      const citiesResponse = await fetch(
        `${API_URL}/artists/${searchResult.uuid}/cities`
      )

      const citiesData = await citiesResponse.json()

      if (!citiesResponse.ok) {
        throw new Error(citiesData.error || "Could not load cities")
      }

      setCities(citiesData)
    } catch (requestError) {
      setError(requestError.message)
    } finally {
      setLoading(false)
    }
  }

  async function handleCitySelect(city) {
    setLoading(true)
    setError("")

    try {
      const response = await fetch(
        `${API_URL}/artists/${artist.uuid}/cities/${city.cityId}/audience`
      )

      const audienceData = await response.json()

      if (!response.ok) {
        throw new Error(audienceData.error || "Could not load audience data")
      }

      setSelectedCity(audienceData)
    } catch (requestError) {
      setError(requestError.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="landing-page">
      <section className="landing-content">
        <h1>touring data</h1>

        {!artist && (
          <SearchBar onArtistSelect={handleArtistSelect} />
        )}

        {loading && <p className="search-status">Loading...</p>}
        {error && <p className="search-error">{error}</p>}

        {artist && (
          <section className="artist-summary">
            <h2>
              {artist.uuid}: {artist.name}
            </h2>

            <p>
              Total monthly listeners: {artist.monthlyListeners}
            </p>

            <SelectCity
              cities={cities}
              onCitySelect={handleCitySelect}
              disabled={loading}
            />
          </section>
        )}

        {selectedCity && (
          <section className="city-summary">
            <p>
              {selectedCity.cityName}, {selectedCity.countryCode}{" "}
              ({selectedCity.cityKey}):{" "}
              {selectedCity.localMonthlyListeners} listeners as of{" "}
              {selectedCity.observedAt}
            </p>
          </section>
        )}
      </section>
    </main>
  )
}