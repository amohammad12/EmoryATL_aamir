import AstrophysicsCard from './illustrations/AstrophysicsCard'
import ArtHistoryCard from './illustrations/ArtHistoryCard'

type Props = {
  title: string
  imageEmoji: string
  duration: string
  onOpen: () => void
}

const cardIllustrations: Record<string, JSX.Element> = {
  '🔢': <AstrophysicsCard />,
  '🪥': <ArtHistoryCard />,
  '🤝': <div className="w-full h-full bg-gradient-to-br from-lime-400 to-lime-500 rounded-2xl pattern-dots grid place-items-center text-7xl">🤝</div>,
}

export default function SongCard({ title, imageEmoji, duration, onOpen }: Props) {
  const illustration = cardIllustrations[imageEmoji] || <div className="w-full h-full bg-gradient-to-br from-blue-400 to-blue-500 rounded-2xl grid place-items-center text-6xl">{imageEmoji}</div>
  return (
    <button onClick={onOpen} className="tap text-left focus-ring group" aria-label={`Open ${title}`}>
      <div className="bg-white rounded-3xl p-4 shadow-md border-4 border-gray-100 transition-transform group-hover:scale-105">
        <div className="h-44 rounded-2xl overflow-hidden mb-3">
          {illustration}
        </div>
        <div className="text-center">
          <div className="font-bold text-xl text-gray-800 mb-2">{title}</div>
          <span className="inline-block px-4 py-1.5 bg-gray-100 text-gray-600 rounded-full text-sm font-medium">{duration}</span>
        </div>
      </div>
    </button>
  )
}
