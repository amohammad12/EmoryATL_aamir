export default function ArtHistoryCard() {
  return (
    <svg viewBox="0 0 300 200" className="w-full h-full">
      {/* Background */}
      <rect width="300" height="200" fill="url(#orangeGradient)" rx="16"/>
      <defs>
        <linearGradient id="orangeGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#fb923c" />
          <stop offset="100%" stopColor="#f97316" />
        </linearGradient>
      </defs>
      
      {/* Paint palette */}
      <ellipse cx="100" cy="120" rx="40" ry="35" fill="#8b5a3c" stroke="#654321" strokeWidth="3"/>
      
      {/* Palette holes */}
      <circle cx="95" cy="105" r="8" fill="#ef4444"/>
      <circle cx="115" cy="100" r="8" fill="#3b82f6"/>
      <circle cx="85" cy="125" r="8" fill="#22c55e"/>
      <circle cx="105" cy="130" r="8" fill="#eab308"/>
      <circle cx="120" cy="120" r="8" fill="#a855f7"/>
      
      {/* Picture frame */}
      <rect x="170" y="70" width="90" height="100" rx="4" fill="#8b4513" stroke="#654321" strokeWidth="4"/>
      <rect x="180" y="80" width="70" height="80" fill="#87ceeb"/>
      
      {/* Mountain in picture */}
      <polygon points="215,140 195,115 235,115" fill="#10b981"/>
      
      {/* Sun in picture */}
      <circle cx="220" cy="95" r="8" fill="#fbbf24"/>
      
      {/* Cloud in picture */}
      <ellipse cx="195" cy="90" rx="10" ry="6" fill="white"/>
      <ellipse cx="202" cy="88" rx="8" ry="5" fill="white"/>
      
      {/* Paintbrushes */}
      <g transform="translate(50, 60)">
        <rect x="0" y="0" width="6" height="50" fill="#8b4513" rx="1"/>
        <ellipse cx="3" cy="0" rx="5" ry="8" fill="#ef4444"/>
      </g>
      <g transform="translate(65, 50)">
        <rect x="0" y="0" width="6" height="60" fill="#8b4513" rx="1"/>
        <ellipse cx="3" cy="0" rx="5" ry="8" fill="#3b82f6"/>
      </g>
      
      {/* Books */}
      <rect x="245" y="160" width="40" height="35" fill="#dc2626" stroke="#991b1b" strokeWidth="2"/>
      <line x1="245" y1="177" x2="285" y2="177" stroke="#991b1b" strokeWidth="2"/>
    </svg>
  )
}
