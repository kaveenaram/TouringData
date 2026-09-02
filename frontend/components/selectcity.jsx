export default function SelectCity({ cities, onCitySelect, disabled }) {
  function handleChange(event) {
    const cityId = event.target.value
    const city = cities.find((item) => String(item.cityId) === cityId)

    if (city) {
      onCitySelect(city)
    }
  }

  return (
    <label className="city-selector">
      <span>Select a city</span>

      <select
        defaultValue=""
        onChange={handleChange}
        disabled={disabled || cities.length === 0}
      >
        <option value="" disabled>
          Choose one of the top cities
        </option>

        {cities.map((city) => (
          <option key={city.cityId} value={city.cityId}>
            {city.cityName}, {city.countryCode} -{" "}
            {city.localMonthlyListeners} listeners
          </option>
        ))}
      </select>
    </label>
  )
}