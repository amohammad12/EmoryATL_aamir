import { NavLink } from 'react-router-dom'

const mainNav = [
  { to: '/learn', label: 'learn', icon: '📖', color: 'bg-pink', activeColor: 'bg-pink', textColor: 'text-gray-700', activeTextColor: 'text-white' },
  { to: '/library', label: 'library', icon: '📚', color: 'bg-lime', activeColor: 'bg-lime', textColor: 'text-gray-700', activeTextColor: 'text-white' },
]

const userNav = { to: '/profile', label: 'profile', icon: '👤', color: 'bg-purple', activeColor: 'bg-purple', textColor: 'text-gray-700', activeTextColor: 'text-white' }

export default function Sidebar() {
  return (
    <aside className="hidden md:flex w-56 shrink-0 flex-col gap-3 p-6 pt-8 bg-white">
      {/* Main navigation */}
      <nav className="flex flex-col gap-2 bg-white rounded-3xl p-4 shadow-soft">
        {mainNav.map((n) => (
          <NavLink
            key={n.to}
            to={n.to}
            className={({ isActive }: { isActive: boolean }) =>
              `tap focus-ring px-3 py-2.5 flex items-center gap-3 rounded-xl transition-all ${
                isActive 
                  ? `${n.activeColor} shadow-sm` 
                  : 'hover:bg-gray-50 border-2 border-gray-200'
              }`
            }
            aria-label={n.label}
          >
            {({ isActive }) => (
              <>
                <span className={`text-2xl`}>{n.icon}</span>
                <span className={`capitalize font-bold ${isActive ? n.activeTextColor : n.textColor}`}>
                  {n.label}
                </span>
              </>
            )}
          </NavLink>
        ))}
      </nav>

      {/* User profile at bottom */}
      <nav className="mt-auto flex flex-col gap-2 bg-white rounded-3xl p-4 shadow-soft">
        <NavLink
          to={userNav.to}
          className={({ isActive }: { isActive: boolean }) =>
            `tap focus-ring px-3 py-2.5 flex items-center gap-3 rounded-xl transition-all ${
              isActive 
                ? `${userNav.activeColor} shadow-sm` 
                : 'hover:bg-gray-50 border-2 border-gray-200'
            }`
          }
          aria-label={userNav.label}
        >
          {({ isActive }) => (
            <>
              <span className={`text-2xl`}>{userNav.icon}</span>
              <span className={`capitalize font-bold ${isActive ? userNav.activeTextColor : userNav.textColor}`}>
                {userNav.label}
              </span>
            </>
          )}
        </NavLink>
      </nav>
    </aside>
  )
}
