// lists the range of possible tickets sold / expected attendance.
// maybe like EXPECTED ATTENDANCE: 122 and then below it in italics (68-153) for example...

// and then shows the three venue components with their details.
// so if the venue data doesn't show up we can still have the expected attendance information displayed.

export default function DashboardTouringInfo({ expectedAttendance, minCapacity, maxCapacity, venues, MIN_ATTENDANCE_PCT, MAX_ATTENDANCE_PCT }) {
    return (
        <div>
            <div style={{ fontWeight: 'bold' }}>
                EXPECTED ATTENDANCE: {expectedAttendance}
                <div style={{ fontStyle: 'italic' }}>
                    ({minCapacity}-{maxCapacity})
                </div>
            </div>
            <div>
                This is the expected attendance range for the artist in this city based on a range of
                <div>
                    <a href="https://orphiq.com/resources/spotify-analytics-tour-routing" target="_blank" rel="noopener noreferrer">
                        {MIN_ATTENDANCE_PCT}%-{MAX_ATTENDANCE_PCT}% 
                    </a>
                </div>
                 of local monthly listeners. 
            </div>
            <div>
                {venues.map((venue) => (
                    <VenueInfo key={venue.venueID} venue={venue} />
                ))}
            </div>
        </div>
    );
}