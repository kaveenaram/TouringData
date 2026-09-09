export default function ArtistResult({ artist, onSelect }) {
  return (
    <button
      type="button"
      className="artist-result"
      onClick={() => onSelect(artist)}
    >
      <img
        src={artist.imageUrl || "/default-artist.png"}
        alt={artist.name}
        className="artist-result__image"
      />

      <div className="artist-result__info">
        <strong className="artist-result__name">{artist.name}</strong>
        <span className="artist-result__genre">{artist.genre || "Unknown"}</span>
      </div>
    </button>
  )
}