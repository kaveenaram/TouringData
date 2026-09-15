export default function DashboardCityInfo({ artist, city }) {
  return (
    <div className="dashboard-city-info">
      <div className="dashboard-city-info__section">
        <p className="dashboard-city-info__label">
          monthly listener count
        </p>
        <p className="dashboard-city-info__value">
            {formatNumber(artist.monthlyListeners)}
        </p>
      </div>

      <div className="dashboard-city-info__section">
        <p className="dashboard-city-info__label">
          monthly listener count in {city.cityName}, {city.countryCode}
        </p>
        <p className="dashboard-city-info__value">
            {formatNumber(city.localMonthlyListeners)}
        </p>
      </div>
    </div>
  )
}

function formatNumber(value) {
  if (value === null || value === undefined || value === "") {
    return "Currently unavailable"
  }

  return Number(value).toLocaleString()
}