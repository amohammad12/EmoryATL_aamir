import { Outlet, NavLink } from 'react-router-dom'
import Sidebar from '@components/Sidebar'
import Header from '@components/Header'
import SkyDecorations from '@components/decorations/SkyDecorations'

export default function App() {
  return (
    <div className="h-screen flex relative overflow-hidden">
      <SkyDecorations />
      <Sidebar />
      <main className="flex-1 p-8 pt-12 relative overflow-y-auto">
        <Header />
        <div className="relative z-10">
          <Outlet />
        </div>
      </main>
    </div>
  )
}
