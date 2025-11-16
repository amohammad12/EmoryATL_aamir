import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useApp } from '@context/AppContext'
import { login } from '@api/index'
import SkyDecorations from '@components/decorations/SkyDecorations'
import HillsWithTrees from '@components/decorations/HillsWithTrees'

export default function Login() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()
  const { setUser } = useApp()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const user = await login(username, password)
      setUser(user)
      navigate('/learn')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="h-screen flex items-center justify-center relative overflow-hidden">
      {/* Background decorations */}
      <SkyDecorations />
      <HillsWithTrees />
      
      {/* Login card */}
      <div className="relative z-10 w-full max-w-md mx-4">
        <div className="bg-white rounded-3xl shadow-2xl p-8 sm:p-12">
          {/* Logo/Title */}
          <div className="text-center mb-8">
            <div className="text-6xl mb-4">🎵</div>
            <h1 
              className="gradient-title text-5xl font-extrabold mb-2"
              data-text="12Tree"
            >
              12Tree
            </h1>
            <p className="text-gray-600 font-semibold text-lg">Learn through songs!</p>
          </div>

          {/* Login form */}
          <form onSubmit={handleSubmit} className="space-y-5">
            <div>
              <label htmlFor="username" className="block text-sm font-bold text-gray-700 mb-2">
                Username
              </label>
              <input
                id="username"
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-full px-4 py-3 rounded-xl border-2 border-gray-200 focus:border-pink focus:outline-none focus:ring-4 focus:ring-pink/20 transition-all font-medium"
                placeholder="Enter your username"
              />
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-bold text-gray-700 mb-2">
                Password
              </label>
              <input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-3 rounded-xl border-2 border-gray-200 focus:border-lime focus:outline-none focus:ring-4 focus:ring-lime/20 transition-all font-medium"
                placeholder="Enter your password"
              />
            </div>

            {error && (
              <div className="bg-red-50 border-2 border-red-300 rounded-xl p-3 text-red-700 text-sm">
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={loading || !username || !password}
              className="w-full bg-gradient-to-r from-pink to-purple text-white font-bold py-4 rounded-2xl shadow-lg hover:shadow-xl tap focus-ring transition-all text-lg disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Logging in...' : "Let's Sing! 🎤"}
            </button>
          </form>

          {/* Additional links */}
          <div className="mt-6 text-center space-y-2">
            <button className="text-sm text-gray-600 hover:text-gray-800 font-semibold tap">
              Forgot password?
            </button>
            <div className="text-sm text-gray-600">
              Don't have an account?{' '}
              <button 
                onClick={() => navigate('/signup')}
                className="text-purple font-bold hover:text-pink tap"
              >
                Sign up
              </button>
            </div>
          </div>
        </div>

        {/* Decorative elements around the card */}
        <div className="absolute -top-8 -left-8 text-6xl animate-bounce">⭐</div>
        <div className="absolute -top-4 -right-4 text-5xl" style={{ animation: 'float 3s ease-in-out infinite' }}>🎨</div>
        <div className="absolute -bottom-6 left-12 text-5xl" style={{ animation: 'float 2.5s ease-in-out infinite' }}>🎵</div>
        <div className="absolute -bottom-4 -right-8 text-6xl animate-bounce" style={{ animationDelay: '0.5s' }}>✨</div>
      </div>
    </div>
  )
}
