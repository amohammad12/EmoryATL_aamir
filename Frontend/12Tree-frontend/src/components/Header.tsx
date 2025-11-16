import { useLocation } from 'react-router-dom'

export default function Header() {
  const { pathname } = useLocation()
  
  const getTitleAndSubtitle = () => {
    if (pathname === '/learn') return null // No header on learn page - it has mode switcher
    if (pathname === '/library') return { title: 'Your Library', subtitle: null }
    if (pathname === '/profile') return { title: 'Your Profile', subtitle: null }
    return { title: 'Learn', subtitle: null }
  }
  
  const headerData = getTitleAndSubtitle()
  
  // Don't render header on learn page
  if (!headerData) return null
  
  const { title } = headerData

  return (
    <header className="mb-6 text-center">
      <h1 
        className="gradient-title text-5xl sm:text-6xl font-extrabold"
        data-text={title}
        style={{
          WebkitTextStroke: '0px',
        }}
      >
        {title}
      </h1>
    </header>
  )
}
