import { useNavigate } from 'react-router-dom'

export default function Profile() {
  const navigate = useNavigate()

  const handleLogout = () => {
    navigate('/login')
  }

  return (
    <div className="max-w-4xl mx-auto">
      {/* Header with avatar and info */}
      <div className="bg-white rounded-3xl p-8 shadow-md mb-6">
        <div className="flex items-center gap-6">
          <div className="w-24 h-24 rounded-2xl bg-orange grid place-items-center text-5xl shadow-lg">
            🐱
          </div>
          <div>
            <h2 className="text-3xl font-extrabold text-gray-800 mb-1">coolcat</h2>
            <p className="text-lg text-gray-600 font-semibold">⭐ Level 3 Star Singer</p>
          </div>
        </div>
      </div>

      {/* Stats cards */}
      <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <div className="bg-white rounded-2xl p-6 shadow-md text-center">
          <div className="text-4xl mb-2">🎵</div>
          <div className="text-2xl font-bold text-gray-800 mb-1">12</div>
          <div className="text-sm text-gray-600 font-medium">Songs created</div>
        </div>
        <div className="bg-white rounded-2xl p-6 shadow-md text-center">
          <div className="text-4xl mb-2">📚</div>
          <div className="text-2xl font-bold text-gray-800 mb-1">8</div>
          <div className="text-sm text-gray-600 font-medium">Lessons completed</div>
        </div>
        <div className="bg-white rounded-2xl p-6 shadow-md text-center">
          <div className="text-4xl mb-2">🎨</div>
          <div className="text-xl font-bold text-gray-800 mb-1">Art History</div>
          <div className="text-sm text-gray-600 font-medium">Favorite topic</div>
        </div>
        <div className="bg-white rounded-2xl p-6 shadow-md text-center">
          <div className="text-4xl mb-2">🎖️</div>
          <div className="text-2xl font-bold text-gray-800 mb-1">5 days</div>
          <div className="text-sm text-gray-600 font-medium">Learning streak</div>
        </div>
      </div>

      {/* Settings */}
      <div className="bg-white rounded-3xl p-8 shadow-md">
        <h3 className="text-2xl font-bold text-gray-800 mb-6 flex items-center gap-2">
          <span className="text-3xl">⚙️</span> Settings
        </h3>
        
        <div className="space-y-6">
          {/* Voice preference */}
          <div>
            <label className="block text-sm font-bold text-gray-700 mb-3">Preferred Voice</label>
            <div className="flex gap-3">
              <button className="tap focus-ring px-6 py-3 rounded-2xl bg-pink text-white font-bold shadow-sm">
                Happy 😊
              </button>
              <button className="tap focus-ring px-6 py-3 rounded-2xl border-2 border-gray-200 text-gray-700 font-bold hover:bg-gray-50">
                Calm 😌
              </button>
              <button className="tap focus-ring px-6 py-3 rounded-2xl border-2 border-gray-200 text-gray-700 font-bold hover:bg-gray-50">
                Silly 🤪
              </button>
            </div>
          </div>

          {/* Subtitles toggle */}
          <div className="flex items-center justify-between">
            <div>
              <div className="font-bold text-gray-800">Subtitles</div>
              <div className="text-sm text-gray-600">Show lyrics while singing</div>
            </div>
            <button className="w-16 h-8 bg-lime rounded-full relative tap focus-ring">
              <div className="absolute right-1 top-1 w-6 h-6 bg-white rounded-full shadow-sm"></div>
            </button>
          </div>

          {/* Progress bar */}
          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="font-bold text-gray-800">Counting Progress</span>
              <span className="text-sm font-semibold text-gray-600">40%</span>
            </div>
            <div className="h-3 bg-gray-200 rounded-full overflow-hidden">
              <div className="h-full bg-gradient-to-r from-lime to-green-400" style={{ width: '40%' }}></div>
            </div>
          </div>

          {/* Logout button */}
          <div className="pt-4 border-t-2 border-gray-100">
            <button 
              onClick={handleLogout}
              className="w-full bg-gradient-to-r from-red-400 to-red-500 text-white font-bold py-4 rounded-2xl shadow-md hover:shadow-lg tap focus-ring transition-all flex items-center justify-center gap-2"
            >
              <span>🚪</span>
              Log Out
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
