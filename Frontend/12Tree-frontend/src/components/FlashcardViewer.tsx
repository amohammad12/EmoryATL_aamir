import AudioPlayer from './AudioPlayer'

type Card = { id: string; symbol: string; hint: string; audioUrl?: string }

type Props = {
  cards: Card[]
}

import { useState } from 'react'

export default function FlashcardViewer({ cards }: Props) {
  const [index, setIndex] = useState(0)
  const c = cards[index]
  const prev = () => setIndex((i: number) => (i - 1 + cards.length) % cards.length)
  const next = () => setIndex((i: number) => (i + 1) % cards.length)

  return (
    <div className="grid gap-4">
      <div className="card p-8 grid place-items-center">
        <div className="text-7xl mb-4">{c.symbol}</div>
        <div className="text-gray-600 text-lg">{c.hint}</div>
      </div>
      <div className="flex items-center justify-between">
        <button className="pill bg-yellow tap focus-ring" onClick={prev} aria-label="Previous card">← Prev</button>
        {c.audioUrl && <AudioPlayer src={c.audioUrl} />}
        <button className="pill bg-yellow tap focus-ring" onClick={next} aria-label="Next card">Next →</button>
      </div>
    </div>
  )
}
