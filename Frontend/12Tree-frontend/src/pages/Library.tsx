import { useState } from 'react'
import LibrarySongItem from '@components/LibrarySongItem'
import FullScreenPlayer from '@components/FullScreenPlayer'
import CardViewScreen from '@components/CardViewScreen'
import { useSongs, Song } from '@hooks/useSongs'

type ViewMode = 'list' | 'song' | 'cards'
type LibrarySection = 'songs' | 'cards'

export default function Library() {
  const { songs, loading, error } = useSongs()
  const [viewMode, setViewMode] = useState<ViewMode>('list')
  const [activeSongId, setActiveSongId] = useState<string | null>(null)
  const [activeSection, setActiveSection] = useState<LibrarySection>('songs')
  
  // Mock saved cards (in real app, this would come from a hook/API)
  const [savedCards] = useState([
    { id: 'c1', title: 'Counting Practice', cardCount: 4, emoji: '🔢' },
    { id: 'c2', title: 'Letters ABC', cardCount: 4, emoji: '📝' },
    { id: 'c3', title: 'Shapes & Colors', cardCount: 4, emoji: '🎨' },
  ])
  
  const activeSong = songs.find(s => s.id === activeSongId)
  
  const handlePlaySong = (songId: string) => {
    setActiveSongId(songId)
    setViewMode('song')
  }
  
  const handleViewCards = (songId: string) => {
    setActiveSongId(songId)
    setViewMode('cards')
  }
  
  const handleClose = () => {
    setViewMode('list')
    setActiveSongId(null)
  }
  
  // Generate mock cards for each song
  const generateMockCards = (title: string) => [
    { id: '1', front: `What is ${title} about?`, back: 'Learning through music!', known: false },
    { id: '2', front: 'Key concept?', back: 'Practice makes perfect', known: false },
    { id: '3', front: 'Remember this?', back: 'Sing along to learn!', known: true },
  ]
  
  // Full-screen song player
  if (viewMode === 'song' && activeSong) {
    return (
      <FullScreenPlayer
        songTitle={activeSong.title}
        artist="12Tree"
        lyrics={activeSong.lyrics || 'No lyrics available for this song.'}
        audioUrl={activeSong.audioUrl}
        mode="library"
        onClose={handleClose}
      />
    )
  }
  
  // Card view screen
  if (viewMode === 'cards' && activeSong) {
    return (
      <CardViewScreen
        songTitle={activeSong.title}
        cards={generateMockCards(activeSong.title)}
        onClose={handleClose}
      />
    )
  }
  
  // Library list view
  return (
    <div className="max-w-4xl mx-auto">
      {/* Section Tabs */}
      <div className="mb-8">
        <div className="flex gap-3">
          <button
            onClick={() => setActiveSection('songs')}
            className={`flex-1 py-3 px-6 rounded-2xl font-bold transition-all tap focus-ring ${
              activeSection === 'songs'
                ? 'bg-gradient-to-r from-pink to-purple text-white shadow-md'
                : 'bg-white text-gray-700 border-2 border-gray-200 hover:border-pink'
            }`}
          >
            <span className="text-xl mr-2">🎵</span>
            Your Songs
          </button>
          <button
            onClick={() => setActiveSection('cards')}
            className={`flex-1 py-3 px-6 rounded-2xl font-bold transition-all tap focus-ring ${
              activeSection === 'cards'
                ? 'bg-gradient-to-r from-purple to-pink text-white shadow-md'
                : 'bg-white text-gray-700 border-2 border-gray-200 hover:border-purple'
            }`}
          >
            <span className="text-xl mr-2">🎴</span>
            Your Cards
          </button>
        </div>
      </div>
      
      {/* Your Songs Section */}
      {activeSection === 'songs' && (
        <div className="space-y-4">
          {loading ? (
            <div className="bg-white rounded-3xl shadow-md p-12 text-center">
              <div className="text-6xl mb-4">⏳</div>
              <h3 className="text-2xl font-bold text-gray-800 mb-2">Loading your songs...</h3>
            </div>
          ) : error ? (
            <div className="bg-white rounded-3xl shadow-md p-12 text-center">
              <div className="text-6xl mb-4">❌</div>
              <h3 className="text-2xl font-bold text-gray-800 mb-2">Error loading songs</h3>
              <p className="text-gray-600 font-medium">{error}</p>
            </div>
          ) : songs.length === 0 ? (
            <div className="bg-white rounded-3xl shadow-md p-12 text-center">
              <div className="text-6xl mb-4">🎵</div>
              <h3 className="text-2xl font-bold text-gray-800 mb-2">No songs yet!</h3>
              <p className="text-gray-600 font-medium">
                Generate songs in Music Mode and add them to your library
              </p>
            </div>
          ) : (
            songs.map((song: Song) => (
              <div 
                key={song.id}
                className="bg-white rounded-3xl shadow-md p-6 hover:shadow-lg transition-all"
              >
                <div className="flex items-center gap-4 mb-4">
                  <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-purple to-pink 
                                  flex items-center justify-center text-3xl shadow-sm flex-shrink-0">
                    {song.emoji}
                  </div>
                  
                  <div className="flex-1 min-w-0">
                    <h3 className="font-bold text-2xl text-gray-800 truncate mb-1">
                      {song.title}
                    </h3>
                    <p className="text-gray-600 font-medium">
                      by 12Tree • {song.duration}
                    </p>
                  </div>
                </div>
                
                {/* Only Play Song button */}
                <button 
                  onClick={() => handlePlaySong(song.id)}
                  className="w-full bg-gradient-to-r from-pink to-purple text-white 
                             font-bold py-3 px-4 rounded-2xl shadow-md hover:shadow-lg 
                             tap focus-ring transition-all flex items-center 
                             justify-center gap-2">
                  <span className="text-xl">▶️</span>
                  <span>Play Song</span>
                </button>
              </div>
            ))
          )}
        </div>
      )}
      
      {/* Your Cards Section */}
      {activeSection === 'cards' && (
        <div className="space-y-4">
          {savedCards.length === 0 ? (
            <div className="bg-white rounded-3xl shadow-md p-12 text-center">
              <div className="text-6xl mb-4">🎴</div>
              <h3 className="text-2xl font-bold text-gray-800 mb-2">No cards yet!</h3>
              <p className="text-gray-600 font-medium">
                Create cards in Card Mode and add them to your library
              </p>
            </div>
          ) : (
            savedCards.map((cardSet) => (
              <div 
                key={cardSet.id}
                className="bg-white rounded-3xl shadow-md p-6 hover:shadow-lg transition-all"
              >
                <div className="flex items-center gap-4 mb-4">
                  <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-lime to-green-400 
                                  flex items-center justify-center text-3xl shadow-sm flex-shrink-0">
                    {cardSet.emoji}
                  </div>
                  
                  <div className="flex-1 min-w-0">
                    <h3 className="font-bold text-2xl text-gray-800 truncate mb-1">
                      {cardSet.title}
                    </h3>
                    <p className="text-gray-600 font-medium">
                      {cardSet.cardCount} cards
                    </p>
                  </div>
                </div>
                
                <button 
                  onClick={() => handleViewCards(cardSet.id)}
                  className="w-full bg-gradient-to-r from-purple to-pink text-white 
                             font-bold py-3 px-4 rounded-2xl shadow-md hover:shadow-lg 
                             tap focus-ring transition-all flex items-center 
                             justify-center gap-2">
                  <span className="text-xl">🎴</span>
                  <span>Study Cards</span>
                </button>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  )
}
