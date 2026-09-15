"use client"

export default function SearchInput({ value, onChange, onSubmit, loading }) {
  return (
    <form onSubmit={onSubmit} className="search-input">
      <input
        type="search"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="search for an artist"
        disabled={loading}
        aria-label="search for an artist"
      />
    </form>
  )
}