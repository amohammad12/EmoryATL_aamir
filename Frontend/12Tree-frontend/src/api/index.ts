// Backend API configuration
// Use relative URL to leverage Vite proxy in development
// In production, this should be configured via environment variable
const API_BASE_URL = import.meta.env.VITE_API_URL || ''
const POLL_INTERVAL = 2000 // Poll every 2 seconds

export interface WordTiming {
  word: string
  start: number
  end: number
}

export interface SongResult {
  title: string
  audioUrl: string
  lyrics: string
  timings?: WordTiming[]
  duration?: number
  bpm?: number
}

interface GenerateResponse {
  job_id: string
  status: string
  progress?: number
  error?: string
  result?: {
    word: string
    lyrics: string
    audio_url: string
    timings: WordTiming[]
    duration: number
    bpm: number
  }
}

interface JobStatusResponse {
  job_id: string
  status: string
  progress: number
  error?: string
  result?: {
    word: string
    lyrics: string
    audio_url: string
    timings: WordTiming[]
    duration: number
    bpm: number
  }
}

export async function generateSong(
  topic: string,
  onProgress?: (progress: number) => void
): Promise<SongResult> {
  try {
    // Step 1: Start song generation
    const generateResponse = await fetch(`${API_BASE_URL}/api/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ word: topic }),
    })

    if (!generateResponse.ok) {
      throw new Error(`Failed to start song generation: ${generateResponse.statusText}`)
    }

    const generateData: GenerateResponse = await generateResponse.json()

    // If result is already complete (cached), return it immediately
    if (generateData.status === 'completed' && generateData.result) {
      const result = generateData.result
      return {
        title: `The ${result.word.charAt(0).toUpperCase() + result.word.slice(1)} Song`,
        audioUrl: `${API_BASE_URL}${result.audio_url}`,
        lyrics: result.lyrics,
        timings: result.timings,
        duration: result.duration,
        bpm: result.bpm,
      }
    }

    // Step 2: Poll for job status
    const jobId = generateData.job_id

    return new Promise((resolve, reject) => {
      const pollInterval = setInterval(async () => {
        try {
          const statusResponse = await fetch(`${API_BASE_URL}/api/jobs/${jobId}`)

          if (!statusResponse.ok) {
            clearInterval(pollInterval)
            reject(new Error(`Failed to get job status: ${statusResponse.statusText}`))
            return
          }

          const statusData: JobStatusResponse = await statusResponse.json()

          // Update progress
          if (onProgress && statusData.progress !== undefined) {
            onProgress(statusData.progress)
          }

          // Check if completed
          if (statusData.status === 'completed' && statusData.result) {
            clearInterval(pollInterval)
            const result = statusData.result
            resolve({
              title: `The ${result.word.charAt(0).toUpperCase() + result.word.slice(1)} Song`,
              audioUrl: `${API_BASE_URL}${result.audio_url}`,
              lyrics: result.lyrics,
              timings: result.timings,
              duration: result.duration,
              bpm: result.bpm,
            })
          } else if (statusData.status === 'failed') {
            clearInterval(pollInterval)
            reject(new Error(statusData.error || 'Song generation failed'))
          }
        } catch (error) {
          clearInterval(pollInterval)
          reject(error)
        }
      }, POLL_INTERVAL)
    })
  } catch (error) {
    console.error('Error generating song:', error)
    throw error
  }
}

export async function saveSongToLibrary(song: SongResult, userId: string): Promise<void> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/library/songs`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        ...song,
        userId,
      }),
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.detail || `Failed to save song: ${response.statusText}`)
    }
  } catch (error) {
    console.error('Error saving song to library:', error)
    throw error
  }
}

export async function signup(username: string, email: string, password: string): Promise<{ username: string; email: string }> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/auth/signup`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, email, password }),
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.detail || `Signup failed: ${response.statusText}`)
    }

    const data = await response.json()
    return data.user
  } catch (error) {
    console.error('Error during signup:', error)
    throw error
  }
}

export async function login(username: string, password: string): Promise<{ username: string; email: string }> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, password }),
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.detail || `Login failed: ${response.statusText}`)
    }

    const data = await response.json()
    return data.user
  } catch (error) {
    console.error('Error during login:', error)
    throw error
  }
}

export async function getSongs() {
  // stub for GET /songs
}
export async function getLessons() {
  // stub for GET /lessons
}
export async function getCards() {
  // stub for GET /cards
}
