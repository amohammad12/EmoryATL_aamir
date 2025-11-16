import { Navigate, Outlet } from 'react-router-dom'
import { useApp } from '@context/AppContext'

export default function ProtectedRoute() {
  const { user } = useApp()

  // If no user is logged in, redirect to login page
  if (!user) {
    return <Navigate to="/login" replace />
  }

  // If user is logged in, render the child routes
  return <Outlet />
}
