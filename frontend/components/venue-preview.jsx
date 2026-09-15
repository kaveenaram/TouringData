export default function VenuePreview({ expectedAttendance }) {
  return (
    <div className="venue-preview">
      <p className="venue-preview__placeholder">
        with an expected attendance of {expectedAttendance}, consider opening
        for other artists to help grow your audience :)
      </p>
    </div>
  )
}