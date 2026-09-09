"use client"

export default function SearchInput({ value, onChange, onSubmit, loading }) {
  return (
    <form onSubmit={onSubmit} className="search-input">
      <input
        type="search"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Search for an artist"
        disabled={loading}
        aria-label="Search for an artist"
      />
    </form>
  )
}