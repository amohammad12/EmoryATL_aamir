import { useEffect, useRef, useState } from 'react'

type Props = {
  src: string
  className?: string
}

export default function AudioPlayer({ src, className }: Props) {
  const audioRef = useRef<HTMLAudioElement | null>(null)
  const [playing, setPlaying] = useState(false)

  useEffect(() => {
    const a = audioRef.current
    if (!a) return
    const onEnd = () => setPlaying(false)
    a.addEventListener('ended', onEnd)
    return () => a.removeEventListener('ended', onEnd)
  }, [])

  const toggle = () => {
    const a = audioRef.current
    if (!a) return
    if (playing) {
      a.pause()
      setPlaying(false)
    } else {
      a.play()
      setPlaying(true)
    }
  }

  return (
    <div className={className}>
      <audio ref={audioRef} src={src} aria-label="audio" />
      <button
        className={`tap focus-ring pill px-6 py-3 text-lg font-bold ${playing ? 'bg-orange' : 'bg-pink'}`}
        onClick={toggle}
        aria-label={playing ? 'Pause audio' : 'Play audio'}
      >
        {playing ? 'Pause ⏸' : 'Play ▶️'}
      </button>
    </div>
  )
}
