import { useState, useEffect, useRef, useMemo } from 'react'

interface WordTiming {
  word: string
  start: number
  end: number
}

interface FullScreenPlayerProps {
  songTitle: string
  artist: string
  lyrics: string
  audioUrl: string
  timings?: WordTiming[]
  mode: 'music' | 'library'
  onClose: () => void
}

export default function FullScreenPlayer({
  songTitle,
  artist,
  lyrics,
  audioUrl,
  timings,
  mode,
  onClose
}: FullScreenPlayerProps) {
  const [isPlaying, setIsPlaying] = useState(false)
  const [currentTime, setCurrentTime] = useState(0)
  const [duration, setDuration] = useState(0)
  const audioRef = useRef<HTMLAudioElement>(null)

  // Split lyrics into lines
  const lyricsLines = lyrics ? lyrics.split('\n').filter(line => line.trim()) : []

  // Cute floating emojis for kids
  const floatingEmojis = useMemo(() => {
    const emojis = ['🌟', '⭐', '✨', '💫', '🎵', '🎶', '🎤', '🎨', '🌈', '☀️',
                    '🦋', '🌸', '🌺', '🌻', '🐝', '🎈', '🎉', '💖', '💕', '🌙']

    return Array.from({ length: 18 }, (_, i) => ({
      id: i,
      emoji: emojis[Math.floor(Math.random() * emojis.length)],
      left: `${Math.random() * 100}%`,
      animationDuration: `${15 + Math.random() * 20}s`, // 15-35 seconds
      animationDelay: `${Math.random() * 5}s`,
      size: Math.random() > 0.5 ? 'text-4xl' : 'text-3xl'
    }))
  }, [])
  
  useEffect(() => {
    const audio = audioRef.current
    if (!audio) return

    const handleTimeUpdate = () => {
      setCurrentTime(audio.currentTime)
    }

    const handleLoadedMetadata = () => {
      setDuration(audio.duration)
    }

    const handleEnded = () => setIsPlaying(false)

    audio.addEventListener('timeupdate', handleTimeUpdate)
    audio.addEventListener('loadedmetadata', handleLoadedMetadata)
    audio.addEventListener('ended', handleEnded)

    return () => {
      audio.removeEventListener('timeupdate', handleTimeUpdate)
      audio.removeEventListener('loadedmetadata', handleLoadedMetadata)
      audio.removeEventListener('ended', handleEnded)
    }
  }, [])
  
  const handlePlayPause = () => {
    const audio = audioRef.current
    if (!audio) return
    
    if (isPlaying) {
      audio.pause()
    } else {
      audio.play()
    }
    setIsPlaying(!isPlaying)
  }
  
  const handleSeek = (e: React.MouseEvent<HTMLDivElement>) => {
    const audio = audioRef.current
    if (!audio || duration === 0) return
    
    const rect = e.currentTarget.getBoundingClientRect()
    const x = e.clientX - rect.left
    const newTime = (x / rect.width) * duration
    audio.currentTime = newTime
    setCurrentTime(newTime)
  }
  
  const handleRewind = () => {
    const audio = audioRef.current
    if (!audio) return
    audio.currentTime = Math.max(0, audio.currentTime - 5)
  }
  
  const handleFastForward = () => {
    const audio = audioRef.current
    if (!audio) return
    audio.currentTime = Math.min(duration, audio.currentTime + 5)
  }
  
  const formatTime = (seconds: number): string => {
    if (!isFinite(seconds)) return '0:00'
    const mins = Math.floor(seconds / 60)
    const secs = Math.floor(seconds % 60)
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }
  
  return (
    <div className="fixed inset-0 bg-gradient-to-br from-purple via-pink to-orange z-50
                    flex flex-col overflow-hidden">
      <audio ref={audioRef} src={audioUrl} />

      {/* Floating Emojis for Kids */}
      <div className="absolute inset-0 pointer-events-none overflow-hidden">
        {floatingEmojis.map((item) => (
          <div
            key={item.id}
            className={`absolute ${item.size} opacity-60`}
            style={{
              left: item.left,
              animation: `float-up ${item.animationDuration} linear infinite`,
              animationDelay: item.animationDelay,
              bottom: '-10%',
            }}
          >
            {item.emoji}
          </div>
        ))}
      </div>

      <style>{`
        @keyframes float-up {
          0% {
            transform: translateY(0) rotate(0deg);
            opacity: 0;
          }
          10% {
            opacity: 0.6;
          }
          90% {
            opacity: 0.6;
          }
          100% {
            transform: translateY(-110vh) rotate(360deg);
            opacity: 0;
          }
        }
      `}</style>
      
      {/* Top Bar */}
      <div className="flex items-center justify-between p-6 text-white">
        <button 
          onClick={onClose}
          className="w-12 h-12 rounded-full hover:bg-white/20 flex items-center 
                     justify-center tap focus-ring text-2xl">
          ✕
        </button>
        
        <div className="flex items-center gap-2 px-4 py-2 bg-white/20 rounded-full 
                        backdrop-blur-sm">
          <span className="text-xl">🎵</span>
          <span className="font-bold capitalize">{mode} Mode</span>
        </div>
        
        <button className="w-12 h-12 rounded-full hover:bg-white/20 flex items-center 
                           justify-center tap focus-ring text-2xl">
          🔗
        </button>
      </div>
      
      {/* Song Info */}
      <div className="text-center text-white mb-8 px-6">
        <h1 className="text-5xl font-extrabold mb-2 drop-shadow-lg">
          {songTitle}
        </h1>
        <p className="text-2xl font-semibold opacity-90">
          by {artist}
        </p>
      </div>
      
      {/* Lyrics Display */}
      <div className="flex-1 overflow-y-auto px-6 pb-6">
        <div className="max-w-3xl mx-auto space-y-3">
          {lyricsLines.length > 0 ? (
            lyricsLines.map((line, index) => (
              <div
                key={index}
                className="text-center text-3xl font-bold text-white drop-shadow-lg"
              >
                {line}
              </div>
            ))
          ) : (
            <div className="text-2xl font-semibold text-white/60 text-center">
              No lyrics available
            </div>
          )}
        </div>
      </div>
      
      {/* Bottom Controls */}
      <div className="bg-gradient-to-t from-black/30 to-transparent backdrop-blur-md 
                      p-6 pt-8">
        {/* Progress Bar */}
        <div className="max-w-3xl mx-auto mb-6">
          <div 
            className="relative h-2 bg-white/30 rounded-full cursor-pointer"
            onClick={handleSeek}
          >
            <div 
              className="absolute inset-y-0 left-0 bg-white rounded-full transition-all"
              style={{ width: `${duration > 0 ? (currentTime / duration) * 100 : 0}%` }}
            />
            <div 
              className="absolute top-1/2 -translate-y-1/2 w-4 h-4 bg-white 
                         rounded-full shadow-lg transition-all"
              style={{ left: `calc(${duration > 0 ? (currentTime / duration) * 100 : 0}% - 8px)` }}
            />
          </div>
          
          <div className="flex justify-between text-white font-semibold mt-2">
            <span>{formatTime(currentTime)}</span>
            <span>{formatTime(duration)}</span>
          </div>
        </div>
        
        {/* Playback Controls */}
        <div className="flex items-center justify-center gap-6 mb-4">
          {/* Rewind 5 seconds */}
          <button 
            onClick={handleRewind}
            className="flex flex-col items-center gap-1 tap focus-ring">
            <div className="w-14 h-14 rounded-full bg-white/20 hover:bg-white/30 
                           flex items-center justify-center text-3xl transition-all">
              ⏪
            </div>
            <span className="text-xs text-white/70 font-semibold">-5s</span>
          </button>
          
          {/* Play/Pause */}
          <button 
            onClick={handlePlayPause}
            className="w-20 h-20 rounded-full bg-white shadow-2xl 
                       hover:scale-105 flex items-center justify-center 
                       tap focus-ring text-4xl transition-transform">
            {isPlaying ? '⏸️' : '▶️'}
          </button>
          
          {/* Fast Forward 5 seconds */}
          <button 
            onClick={handleFastForward}
            className="flex flex-col items-center gap-1 tap focus-ring">
            <div className="w-14 h-14 rounded-full bg-white/20 hover:bg-white/30 
                           flex items-center justify-center text-3xl transition-all">
              ⏩
            </div>
            <span className="text-xs text-white/70 font-semibold">+5s</span>
          </button>
        </div>
        
        {/* Status */}
        <div className="text-center text-white/80 font-semibold">
          Playing in {mode === 'music' ? 'Music' : 'Library'} Mode ✨
        </div>
      </div>
    </div>
  )
}
