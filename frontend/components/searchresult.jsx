export default function SearchResult({ artist, onSelect }) {
  return (
    <button
      type="button"
      className="search-result"
      onClick={() => onSelect(artist)}
    >
      <img
        src={artist.imageUrl || "/default-artist.png"}
        alt=""
        className="artist-image"
      />

      <span className="artist-details">
        <strong>{artist.name}</strong>
        <small>{artist.genre || "Genre unknown"}</small>
      </span>
    </button>
  )
}