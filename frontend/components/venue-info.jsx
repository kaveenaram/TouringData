/* return {
        "cityId": cityId,
        "cityName": city.city_name,
        "minCapacity": minCapacity,
        "maxCapacity": maxCapacity,
        "expectedAttendance": round(expectedAttendance),
        "venues": [
            {
                "venueID": v.venue_id,
                "name": v.name,
                "capacity": int(v.capacity) if v.capacity else None,
                "address": v.address,
                "region": v.region,
                "postalCode": v.postal_code,
                "latitude": v.latitude,
                "longitude": v.longitude,
                "cityId": v.city_id,
                "countryCode": v.country_code,
                "imageUrl": findVenueImageURL(v.venue_id),*/


// displays picture of the venue along with its details.
// in this order: image, then below name in bold, then below address, cityname, region, postal code, then below capacity

export default function VenueInfo({ venue, cityName }) {
  return (
    <div>
      <img
        src={venue.imageUrl}
        alt={venue.name}
        style={{
          width: "100%",
          height: "auto",
        }}
      />

      <div style={{ fontWeight: "bold" }}>
        {venue.name}
      </div>

      <div>
        {venue.address}, {cityName}, {venue.region},{" "}
        {venue.postalCode}
      </div>

      <div>
        Capacity: {venue.capacity}
      </div>
    </div>
  )
}