import { useEffect } from 'react'

interface ToastProps {
  message: string
  icon?: string
  onClose: () => void
  duration?: number
}

export default function Toast({ message, icon = '✓', onClose, duration = 3000 }: ToastProps) {
  useEffect(() => {
    const timer = setTimeout(() => {
      onClose()
    }, duration)

    return () => clearTimeout(timer)
  }, [duration, onClose])

  return (
    <div className="fixed top-8 left-1/2 -translate-x-1/2 z-[100] animate-slide-down">
      <div className="bg-white rounded-2xl shadow-2xl px-6 py-4 flex items-center gap-3 border-2 border-lime">
        <div className="w-10 h-10 rounded-full bg-lime flex items-center justify-center text-2xl">
          {icon}
        </div>
        <p className="font-bold text-gray-800 text-lg">
          {message}
        </p>
      </div>
    </div>
  )
}
