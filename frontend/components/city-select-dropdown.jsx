export default function CitySelectDropdown({
  cities,
  onSelect,
  disabled,
  label,
}) {
  function handleChange(event) {
    const cityId = event.target.value
    const city = cities.find((item) => String(item.cityId) === cityId)
    if (city) {
      onSelect(city)
    }
  }

  return (
    <div className="city-select">
      {label && <label className="city-select__label">{label}</label>}

      <select
        defaultValue=""
        onChange={handleChange}
        disabled={disabled || cities.length === 0}
        className="city-select__dropdown"
      >
        <option value="" disabled>
          Choose a city
        </option>

        {cities.map((city) => (
          <option key={city.cityId} value={city.cityId}>
            {city.cityName}, {city.countryCode}
          </option>
        ))}
      </select>
    </div>
  )
}