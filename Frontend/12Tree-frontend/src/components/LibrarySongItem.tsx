interface LibrarySongItemProps {
  song: {
    id: string
    title: string
    artist: string
    emoji: string
    duration: string
  }
  onPlaySong: () => void
  onViewCards: () => void
}

export default function LibrarySongItem({
  song,
  onPlaySong,
  onViewCards
}: LibrarySongItemProps) {
  return (
    <div className="bg-white rounded-3xl shadow-md p-6 hover:shadow-lg transition-all">
      {/* Song Info */}
      <div className="flex items-center gap-4 mb-4">
        <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-purple to-pink 
                        flex items-center justify-center text-3xl shadow-sm 
                        flex-shrink-0">
          {song.emoji}
        </div>
        
        <div className="flex-1 min-w-0">
          <h3 className="font-bold text-2xl text-gray-800 truncate mb-1">
            {song.title}
          </h3>
          <p className="text-gray-600 font-medium">
            by {song.artist} • {song.duration}
          </p>
        </div>
      </div>
      
      {/* Action Buttons */}
      <div className="grid grid-cols-2 gap-3">
        <button 
          onClick={onPlaySong}
          className="bg-gradient-to-r from-pink to-purple text-white 
                     font-bold py-3 px-4 rounded-2xl shadow-md hover:shadow-lg 
                     tap focus-ring transition-all flex items-center 
                     justify-center gap-2">
          <span className="text-xl">▶️</span>
          <span>Song</span>
        </button>
        
        <button 
          onClick={onViewCards}
          className="border-2 border-pink text-pink font-bold py-3 px-4 
                     rounded-2xl hover:bg-pink hover:text-white tap focus-ring 
                     transition-all flex items-center justify-center gap-2">
          <span className="text-xl">🎴</span>
          <span>Cards</span>
        </button>
      </div>
    </div>
  )
}
