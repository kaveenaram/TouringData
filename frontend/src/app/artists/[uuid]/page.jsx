import { notFound } from "next/navigation"

export default async function ArtistPage({ params }) {
  const { uuid } = await params

  const response = await fetch(
    `http://localhost:5000/api/artists/${uuid}`
  )

  if (!response.ok) {
    notFound()
  }

  const artist = await response.json()

  return (
    <main>
      <h1>{artist.name}</h1>
      <p>{artist.genre}</p>
    </main>
  )
}