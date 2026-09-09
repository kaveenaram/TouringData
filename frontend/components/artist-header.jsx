export default function ArtistHeader({ artist }) {
  return (
    <div className="artist-header">
      <img
        src={artist.imageUrl || "/default-artist.png"}
        alt={artist.name}
        className="artist-header__image"
      />

      <div className="artist-header__info">
        <strong className="artist-header__name">{artist.name}</strong>
        <span className="artist-header__genre">{artist.genre || "Unknown"}</span>
      </div>
    </div>
  )
}