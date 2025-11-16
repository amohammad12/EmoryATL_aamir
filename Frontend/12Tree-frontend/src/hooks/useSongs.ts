import { useState, useEffect } from 'react'
import { useApp } from '@context/AppContext'

export type Song = {
  id: string
  title: string
  emoji: string
  duration: string
  audioUrl: string
  lyrics?: string
  timings?: any[]
  bpm?: number
}

const API_BASE_URL = import.meta.env.VITE_API_URL || ''

export function useSongs() {
  const { user } = useApp()
  const [songs, setSongs] = useState<Song[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchSongs = async () => {
      if (!user) {
        setSongs([])
        return
      }

      setLoading(true)
      setError(null)

      try {
        const response = await fetch(`${API_BASE_URL}/api/library/songs?user_id=${user.username}`)

        if (!response.ok) {
          throw new Error('Failed to fetch songs')
        }

        const data = await response.json()

        // Transform backend songs to frontend format
        const transformedSongs: Song[] = data.songs.map((song: any) => ({
          id: song.id,
          title: song.title,
          emoji: '🎵', // Default emoji, could be dynamic
          duration: song.duration ? `${Math.round(song.duration)}s` : 'Unknown',
          audioUrl: `${API_BASE_URL}${song.audioUrl}`,
          lyrics: song.lyrics,
          timings: song.timings,
          bpm: song.bpm,
        }))

        setSongs(transformedSongs)
      } catch (err) {
        console.error('Error fetching songs:', err)
        setError(err instanceof Error ? err.message : 'Failed to load songs')
        setSongs([])
      } finally {
        setLoading(false)
      }
    }

    fetchSongs()
  }, [user])

  return { songs, loading, error }
}
