type Props = {
  activeMode: 'music' | 'cards'
  onModeChange: (mode: 'music' | 'cards') => void
}

export default function ModeTabSwitcher({ activeMode, onModeChange }: Props) {
  return (
    <div className="flex justify-center mb-8">
      <div className="inline-flex bg-white rounded-full p-1.5 shadow-md border-2 border-gray-100">
        <button
          onClick={() => onModeChange('music')}
          className={`px-6 py-2.5 rounded-full font-bold text-sm transition-all tap focus-ring ${
            activeMode === 'music'
              ? 'bg-pink text-white shadow-sm'
              : 'text-gray-600 hover:text-gray-800'
          }`}
        >
          🎵 Music mode
        </button>
        <button
          onClick={() => onModeChange('cards')}
          className={`px-6 py-2.5 rounded-full font-bold text-sm transition-all tap focus-ring ${
            activeMode === 'cards'
              ? 'bg-pink text-white shadow-sm'
              : 'text-gray-600 hover:text-gray-800'
          }`}
        >
          🎴 Card mode
        </button>
      </div>
    </div>
  )
}
