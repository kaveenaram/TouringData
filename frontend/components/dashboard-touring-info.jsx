// lists the range of possible tickets sold / expected attendance.
// maybe like EXPECTED ATTENDANCE: 122 and then below it in italics (68-153) for example...

// and then shows the three venue components with their details.
// so if the venue data doesn't show up we can still have the expected attendance information displayed.

export default function DashboardTouringInfo({
  expectedAttendance,
  minCapacity,
  maxCapacity,
}) {
  return (
    <div className="dashboard-touring-info">

      <div className="dashboard-touring-info__expected-attendance">
        EXPECTED ATTENDANCE:{" "}
        {Number(expectedAttendance).toLocaleString()}
      </div>

      <div className="dashboard-touring-info__range">
        (
        {Number(minCapacity).toLocaleString()}
        {"–"}
        {Number(maxCapacity).toLocaleString()}
        )
      </div>

      <p className="dashboard-touring-info__information">
        This is the expected attendance range for the artist in this city
        based on a range of{" "}
        <a
          href="https://orphiq.com/resources/spotify-analytics-tour-routing"
          target="_blank"
          rel="noopener noreferrer"
        >
          2%–4%
        </a>{" "}
        of local monthly listeners.
      </p>

    </div>
  );
}