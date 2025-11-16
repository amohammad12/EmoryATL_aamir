type Props = {
  bg: string
  big: string
  label: string
  duration: string
  onClick: () => void
}
const patterns: Record<string, string> = {
  'bg-lime': 'pattern-dots',
  'bg-orange': 'pattern-stars',
  'bg-yellow': 'pattern-zigzag',
}

export default function LessonCard({ bg, big, label, duration, onClick }: Props) {
  const pattern = patterns[bg] || ''
  return (
    <button onClick={onClick} className="tap focus-ring text-center group"
      aria-label={`Start lesson ${label}`}>
      <div className="bg-white rounded-3xl p-4 border-4 border-gray-100 shadow-md transition-transform group-hover:scale-105">
        <div className={`${bg} ${pattern} rounded-2xl h-40 grid place-items-center mb-3 relative overflow-hidden`}>
          <div className="text-white text-5xl font-black tracking-wide drop-shadow-lg">{big}</div>
        </div>
        <div className="font-bold text-xl text-gray-800 mb-2">{label}</div>
        <span className="inline-block px-4 py-1.5 bg-gray-100 text-gray-600 rounded-full text-sm font-medium">{duration}</span>
      </div>
    </button>
  )
}
