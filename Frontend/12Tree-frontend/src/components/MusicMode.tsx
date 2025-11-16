import React, { useState } from 'react'
import { useApp } from '@context/AppContext'
import FullScreenPlayer from '@components/FullScreenPlayer'
import Toast from '@components/Toast'
import { generateSong, saveSongToLibrary, SongResult } from '@api/index'
import HillsWithTrees from '@components/decorations/HillsWithTrees'

export default function MusicMode() {
  const { user } = useApp()
  const [topic, setTopic] = useState('')
  const [loading, setLoading] = useState(false)
  const [progress, setProgress] = useState(0)
  const [error, setError] = useState<string | null>(null)
  const [result, setResult] = useState<SongResult | null>(null)
  const [showFullScreen, setShowFullScreen] = useState(false)
  const [showAddToLibrary, setShowAddToLibrary] = useState(false)
  const [showToast, setShowToast] = useState(false)
  const [toastMessage, setToastMessage] = useState('')

  const onPlay = async () => {
    if (!topic.trim()) return
    setLoading(true)
    setProgress(0)
    setError(null)
    setResult(null)
    setShowAddToLibrary(false)

    try {
      const r = await generateSong(topic, (prog) => {
        setProgress(prog)
      })
      setResult(r)
      setLoading(false)
      setShowFullScreen(true) // Automatically open full-screen player
      setShowAddToLibrary(true) // Show add to library option
    } catch (err) {
      setLoading(false)
      setError(err instanceof Error ? err.message : 'Failed to generate song')
      console.error('Error generating song:', err)
    }
  }

  const handleAddToLibrary = async () => {
    if (!result) return

    if (!user) {
      setToastMessage('Please login to save songs to your library')
      setShowToast(true)
      return
    }

    try {
      await saveSongToLibrary(result, user.username)
      setToastMessage(`"${result.title}" added to Your Songs!`)
      setShowToast(true)
      setShowAddToLibrary(false)
    } catch (err) {
      console.error('Error saving to library:', err)
      const errorMsg = err instanceof Error ? err.message : 'Failed to save song to library'
      setToastMessage(errorMsg)
      setShowToast(true)
    }
  }

  // Full-screen player view
  if (showFullScreen && result) {
    return (
      <div className="relative">
        <FullScreenPlayer
          songTitle={result.title}
          artist="12Tree Music"
          lyrics={result.lyrics}
          audioUrl={result.audioUrl}
          timings={result.timings}
          mode="music"
          onClose={() => {
            setShowFullScreen(false)
            setResult(null) // Reset result when closing
            setTopic('') // Clear topic input
            setShowAddToLibrary(false)
          }}
        />
        
        {/* Add to Library Button - Floating */}
        {showAddToLibrary && (
          <button
            onClick={handleAddToLibrary}
            className="fixed bottom-8 right-8 bg-white text-gray-800 font-bold 
                       py-4 px-6 rounded-2xl shadow-2xl hover:shadow-xl 
                       tap focus-ring transition-all flex items-center gap-2 z-50
                       border-2 border-lime">
            <span className="text-2xl">➕</span>
            <span>Add to Library</span>
          </button>
        )}
        
        {/* Toast Notification */}
        {showToast && (
          <Toast
            message={toastMessage}
            icon="🎵"
            onClose={() => setShowToast(false)}
          />
        )}
      </div>
    )
  }

  return (
    <div className="relative min-h-[600px]">
      <HillsWithTrees />

      <div className="relative z-10 max-w-2xl mx-auto text-center">
        <div className="grid gap-6">
          <input
            id="topic"
            className="focus-ring rounded-3xl px-6 py-5 border-none outline-none shadow-lg text-lg bg-white text-center placeholder:text-gray-400"
            placeholder="What songs do you want to create?"
            value={topic}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) => setTopic(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter') {
                onPlay()
              }
            }}
            disabled={loading}
          />
          <button
            className="tap focus-ring bg-pink text-white font-bold text-xl rounded-3xl py-5 px-12 shadow-lg mx-auto disabled:opacity-50 disabled:cursor-not-allowed"
            onClick={onPlay}
            disabled={loading || !topic.trim()}
          >
            ♫ Play ♫
          </button>

          {/* Loading State with Progress */}
          {loading && (
            <div className="bg-white rounded-3xl shadow-lg p-6 max-w-md mx-auto">
              <div className="grid place-items-center text-lg text-gray-700 mb-4">
                Growing your song tree… 🌱
              </div>

              {/* Progress Bar */}
              <div className="w-full bg-gray-200 rounded-full h-8 overflow-hidden mb-2">
                <div
                  className="bg-gradient-to-r from-pink to-purple h-full transition-all duration-500 flex items-center justify-center text-white font-bold text-sm"
                  style={{ width: `${progress}%` }}
                >
                  {progress}%
                </div>
              </div>

              <p className="text-sm text-gray-600 mt-2">
                This may take 30-60 seconds...
              </p>
            </div>
          )}

          {/* Error State */}
          {error && !loading && (
            <div className="bg-red-50 border-2 border-red-300 rounded-3xl shadow-lg p-6 max-w-md mx-auto">
              <div className="text-4xl mb-2">❌</div>
              <div className="text-lg font-bold text-red-800 mb-2">
                Oops! Something went wrong
              </div>
              <div className="text-sm text-red-600">
                {error}
              </div>
              <button
                className="mt-4 bg-red-500 text-white font-bold py-2 px-6 rounded-2xl hover:bg-red-600 transition-colors"
                onClick={() => setError(null)}
              >
                Try Again
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
