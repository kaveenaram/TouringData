"use client"

import ArtistResult from "./artist-result"

export default function ArtistResultsList({
  artists,
  loading,
  error,
  onSelect,
}) {
  if (loading) {
    return <div className="results-list results-list--loading">Searching...</div>
  }

  if (error) {
    return <div className="results-list results-list--error">{error}</div>
  }

  if (artists.length === 0) {
    return null
  }

  return (
    <div className="results-list" role="listbox">
      {artists.map((artist) => (
        <ArtistResult
          key={artist.uuid}
          artist={artist}
          onSelect={onSelect}
        />
      ))}
    </div>
  )
}