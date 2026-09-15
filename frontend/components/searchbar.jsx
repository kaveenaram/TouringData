"use client"

import { useState } from "react"
import SearchResult from "./searchresult"

const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000/api"

export default function SearchBar({ onArtistSelect }) {
  const [query, setQuery] = useState("")
  const [artists, setArtists] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  async function searchArtists(event) {
    event.preventDefault()

    const name = query.trim()

    if (!name) {
      setArtists([])
      return
    }

    setLoading(true)
    setError("")
    setArtists([])

    try {
      const response = await fetch(
        `${API_URL}/artists/search?name=${encodeURIComponent(name)}`
      )

      const data = await response.json()

      if (!response.ok || !Array.isArray(data)) {
        throw new Error(data.error || "Search failed")
      }

      setArtists(data)
    } catch (requestError) {
      setError(requestError.message)
    } finally {
      setLoading(false)
    }
  }

  function handleSelect(artist) {
    setQuery(artist.name)
    setArtists([])
    onArtistSelect?.(artist)
  }

  return (
    <div className="search-container">
      <form onSubmit={searchArtists}>
        <input
          type="search"
          value={query}
          placeholder="search for an artist"
          onChange={(event) => setQuery(event.target.value)}
          aria-label="search for an artist"
        />
      </form>

      {loading && <p className="search-status">searching...</p>}
      {error && <p className="search-error">{error}</p>}

      {artists.length > 0 && (
        <div className="search-results" role="listbox">
          {artists.map((artist) => (
            <SearchResult
              key={artist.uuid}
              artist={artist}
              onSelect={handleSelect}
            />
          ))}
        </div>
      )}
    </div>
  )
}