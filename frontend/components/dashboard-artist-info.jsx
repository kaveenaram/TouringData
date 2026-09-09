export default function DashboardArtistInfo({ artist }) {
  return (
    <div className="dashboard-artist-info">
      <img
        src={artist.imageUrl || "/default-artist.png"}
        alt={artist.name}
        className="dashboard-artist-info__image"
      />

      <div className="dashboard-artist-info__content">
        <h1 className="dashboard-artist-info__name">{artist.name}</h1>

        <p className="dashboard-artist-info__genre">
          <span className="dashboard-artist-info__label">genre:</span>
          {artist.genre || "Unknown"}
        </p>
      </div>
    </div>
  )
}