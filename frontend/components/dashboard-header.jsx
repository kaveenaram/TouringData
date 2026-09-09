export default function DashboardHeader({ onBack, backText }) {
  return (
    <header className="dashboard-header">
      <button
        className="dashboard-header__back"
        onClick={onBack}
      >
        <span className="dashboard-header__arrow">
          ↑
        </span>

        <span className="dashboard-header__back-text">
          {backText}
        </span>
      </button>
    </header>
  )
}