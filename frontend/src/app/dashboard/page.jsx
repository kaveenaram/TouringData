"use client"

import { useState } from "react"
import SearchBar from "../../../components/searchbar"

const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000/api"

export default function DashboardPage() {
  const [artist, setArtist] = useState(null)
  const [cities, setCities] = useState([])
  const [selectedCity, setSelectedCity] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  async function handleArtistSelect(selectedArtist) {
    setLoading(true)
    setError("")
    setSelectedCity(null)

    try {
      const artistResponse = await fetch(`${API_URL}/artists/select`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(selectedArtist),
      })

      const selectedArtistData = await artistResponse.json()

      if (!artistResponse.ok) {
        throw new Error(selectedArtistData.error || "Could not select artist")
      }

      setArtist(selectedArtistData)

      const citiesResponse = await fetch(
        `${API_URL}/artists/${selectedArtist.uuid}/cities`
      )

      const citiesData = await citiesResponse.json()

      if (!citiesResponse.ok) {
        throw new Error(citiesData.error || "Could not load cities")
      }

      setCities(citiesData)
    } catch (requestError) {
      setError(requestError.message)
      setArtist(null)
      setCities([])
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
    <main>
      <h1>Touring Data</h1>

      {!artist && (
        <SearchBar onArtistSelect={handleArtistSelect} />
      )}

      {loading && <p>Loading...</p>}
      {error && <p role="alert">{error}</p>}

      {artist && (
        <section>
          <h2>{artist.name}</h2>
          <p>{artist.genre || "Genre unknown"}</p>
          <p>
            Monthly listeners: {artist.monthlyListeners}
          </p>

          <h3>Top cities</h3>

          <ul>
            {cities.map((city) => (
              <li key={city.cityId}>
                <button
                  type="button"
                  onClick={() => handleCitySelect(city)}
                >
                  {city.cityName}, {city.countryCode}
                </button>
                <span>
                  {" "}
                  {city.localMonthlyListeners} listeners
                </span>
              </li>
            ))}
          </ul>
        </section>
      )}

      {selectedCity && (
        <section>
          <h2>
            {selectedCity.cityName}, {selectedCity.countryCode}
          </h2>
          <p>
            Local monthly listeners:{" "}
            {selectedCity.localMonthlyListeners}
          </p>
          <p>Observed: {selectedCity.observedAt}</p>
        </section>
      )}
    </main>
  )
}