import { createContext, useContext, useState, useEffect, ReactNode } from 'react'

type User = {
  username: string
  email: string
  avatar?: string
}

type AppState = {
  user: User | null
  setUser: (user: User | null) => void
  logout: () => void
}

const AppCtx = createContext<AppState | null>(null)

export function AppProvider({ children }: { children: ReactNode }) {
  const [user, setUserState] = useState<User | null>(null)

  // Load user from localStorage on mount
  useEffect(() => {
    const savedUser = localStorage.getItem('user')
    if (savedUser) {
      try {
        setUserState(JSON.parse(savedUser))
      } catch (e) {
        console.error('Error loading user from localStorage', e)
        localStorage.removeItem('user')
      }
    }
  }, [])

  const setUser = (newUser: User | null) => {
    setUserState(newUser)
    if (newUser) {
      localStorage.setItem('user', JSON.stringify(newUser))
    } else {
      localStorage.removeItem('user')
    }
  }

  const logout = () => {
    setUser(null)
  }

  return (
    <AppCtx.Provider value={{ user, setUser, logout }}>
      {children}
    </AppCtx.Provider>
  )
}

export function useApp() {
  const ctx = useContext(AppCtx)
  if (!ctx) throw new Error('AppContext missing')
  return ctx
}
