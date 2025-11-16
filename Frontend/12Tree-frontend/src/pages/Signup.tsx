import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useApp } from '@context/AppContext'
import { signup, login } from '@api/index'
import SkyDecorations from '@components/decorations/SkyDecorations'
import HillsWithTrees from '@components/decorations/HillsWithTrees'

export default function Signup() {
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()
  const { setUser } = useApp()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')

    // Validate passwords match
    if (password !== confirmPassword) {
      setError('Passwords do not match')
      return
    }

    if (password.length < 6) {
      setError('Password must be at least 6 characters')
      return
    }

    setLoading(true)

    try {
      // Create account
      await signup(username, email, password)

      // Login automatically
      const user = await login(username, password)
      setUser(user)
      navigate('/learn')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Signup failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="h-screen flex items-center justify-center relative overflow-hidden">
      {/* Background decorations */}
      <SkyDecorations />
      <HillsWithTrees />
      
      {/* Signup card */}
      <div className="relative z-10 w-full max-w-md mx-4">
        <div className="bg-white rounded-3xl shadow-2xl p-8 sm:p-12">
          {/* Logo/Title */}
          <div className="text-center mb-6">
            <div className="text-6xl mb-3">🎨</div>
            <h1 
              className="gradient-title text-5xl font-extrabold mb-2"
              data-text="Join 12Tree"
            >
              Join 12Tree
            </h1>
            <p className="text-gray-600 font-semibold">Start your learning journey!</p>
          </div>

          {/* Signup form */}
          <form onSubmit={handleSubmit} className="space-y-4">
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
                placeholder="Choose a username"
              />
            </div>

            <div>
              <label htmlFor="email" className="block text-sm font-bold text-gray-700 mb-2">
                Email
              </label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-4 py-3 rounded-xl border-2 border-gray-200 focus:border-lime focus:outline-none focus:ring-4 focus:ring-lime/20 transition-all font-medium"
                placeholder="your@email.com"
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
                className="w-full px-4 py-3 rounded-xl border-2 border-gray-200 focus:border-purple focus:outline-none focus:ring-4 focus:ring-purple/20 transition-all font-medium"
                placeholder="Create a password"
              />
            </div>

            <div>
              <label htmlFor="confirmPassword" className="block text-sm font-bold text-gray-700 mb-2">
                Confirm Password
              </label>
              <input
                id="confirmPassword"
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                className="w-full px-4 py-3 rounded-xl border-2 border-gray-200 focus:border-orange focus:outline-none focus:ring-4 focus:ring-orange/20 transition-all font-medium"
                placeholder="Confirm your password"
              />
            </div>

            {error && (
              <div className="bg-red-50 border-2 border-red-300 rounded-xl p-3 text-red-700 text-sm">
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={loading || !username || !email || !password || !confirmPassword}
              className="w-full bg-gradient-to-r from-lime to-green-400 text-white font-bold py-4 rounded-2xl shadow-lg hover:shadow-xl tap focus-ring transition-all text-lg mt-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Creating Account...' : 'Create Account 🎉'}
            </button>
          </form>

          {/* Additional links */}
          <div className="mt-6 text-center">
            <div className="text-sm text-gray-600">
              Already have an account?{' '}
              <button 
                onClick={() => navigate('/login')}
                className="text-purple font-bold hover:text-pink tap"
              >
                Log in
              </button>
            </div>
          </div>
        </div>

        {/* Decorative elements around the card */}
        <div className="absolute -top-8 -left-8 text-6xl animate-bounce">🌟</div>
        <div className="absolute -top-4 -right-4 text-5xl" style={{ animation: 'float 3s ease-in-out infinite' }}>🎈</div>
        <div className="absolute -bottom-6 left-12 text-5xl" style={{ animation: 'float 2.5s ease-in-out infinite' }}>📚</div>
        <div className="absolute -bottom-4 -right-8 text-6xl animate-bounce" style={{ animationDelay: '0.5s' }}>🎨</div>
      </div>
    </div>
  )
}
