import { useState } from 'react'
import AudioPlayer from './AudioPlayer'

type Props = {
  open: boolean
  onClose: () => void
  title: string
  artworkEmoji: string
  audioUrl: string
  lyrics?: string
  onAddToCards?: () => void
}

export default function SongModal({ open, onClose, title, artworkEmoji, audioUrl, lyrics, onAddToCards }: Props) {
  const [showLyrics, setShowLyrics] = useState(false)
  if (!open) return null
  return (
    <div className="fixed inset-0 bg-black/30 grid place-items-center p-4 z-50" role="dialog" aria-modal="true">
      <div className="card max-w-xl w-full p-4 sm:p-6">
        <div className="flex items-start gap-4">
          <div className="text-6xl bg-skybg rounded-2xl w-24 h-24 grid place-items-center">{artworkEmoji}</div>
          <div className="flex-1">
            <h2 className="text-2xl font-extrabold">{title}</h2>
            <div className="mt-3"><AudioPlayer src={audioUrl} /></div>
          </div>
          <button className="pill bg-yellow tap focus-ring" onClick={onClose} aria-label="Close">
            ✕
          </button>
        </div>
        <div className="mt-4 flex gap-3">
          <button className="pill bg-lime tap focus-ring" onClick={() => setShowLyrics((v: boolean) => !v)} aria-expanded={showLyrics}>
            {showLyrics ? 'Hide lyrics' : 'Show lyrics'}
          </button>
          {onAddToCards && (
            <button className="pill bg-purple tap focus-ring" onClick={onAddToCards}>Add to cards</button>
          )}
        </div>
        {showLyrics && (
          <div className="mt-4 p-4 bg-skybg rounded-xl text-lg leading-relaxed max-h-64 overflow-auto whitespace-pre-wrap">
            {lyrics || 'Lyrics coming soon...'}
          </div>
        )}
      </div>
    </div>
  )
}
