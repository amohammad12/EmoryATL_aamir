export default function AstrophysicsCard() {
  return (
    <svg viewBox="0 0 300 200" className="w-full h-full">
      {/* Background with pattern */}
      <rect width="300" height="200" fill="url(#purpleGradient)" rx="16"/>
      <defs>
        <linearGradient id="purpleGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#6366f1" />
          <stop offset="100%" stopColor="#4f46e5" />
        </linearGradient>
      </defs>
      
      {/* Stars in background */}
      <circle cx="50" cy="30" r="2" fill="white" opacity="0.6"/>
      <circle cx="240" cy="50" r="2" fill="white" opacity="0.8"/>
      <circle cx="200" cy="160" r="2" fill="white" opacity="0.5"/>
      <circle cx="80" cy="170" r="2" fill="white" opacity="0.7"/>
      <circle cx="260" cy="120" r="2" fill="white" opacity="0.6"/>
      
      {/* Tablet with galaxy */}
      <rect x="60" y="60" width="100" height="80" rx="8" fill="#1e293b" stroke="#475569" strokeWidth="3"/>
      <rect x="70" y="70" width="80" height="60" rx="4" fill="#0f172a"/>
      
      {/* Galaxy on tablet */}
      <circle cx="110" cy="100" r="20" fill="url(#galaxyGradient)"/>
      <defs>
        <radialGradient id="galaxyGradient">
          <stop offset="0%" stopColor="#a855f7" />
          <stop offset="100%" stopColor="#3b82f6" />
        </radialGradient>
      </defs>
      
      {/* Stars around galaxy */}
      <circle cx="95" cy="85" r="1.5" fill="#fbbf24"/>
      <circle cx="125" cy="92" r="1.5" fill="#fbbf24"/>
      <circle cx="105" cy="115" r="1.5" fill="#fbbf24"/>
      
      {/* Yellow star top right */}
      <g transform="translate(230, 60)">
        <polygon points="0,-12 3,-4 12,-4 5,2 8,10 0,5 -8,10 -5,2 -12,-4 -3,-4" fill="#fbbf24"/>
      </g>
      
      {/* Saturn */}
      <ellipse cx="200" cy="120" rx="35" ry="35" fill="url(#saturnGradient)"/>
      <defs>
        <linearGradient id="saturnGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#f5deb3" />
          <stop offset="100%" stopColor="#daa520" />
        </linearGradient>
      </defs>
      
      {/* Saturn rings */}
      <ellipse cx="200" cy="120" rx="50" ry="15" fill="none" stroke="#f5deb3" strokeWidth="6" opacity="0.7"/>
      <ellipse cx="200" cy="120" rx="50" ry="15" fill="none" stroke="#daa520" strokeWidth="2" opacity="0.5"/>
    </svg>
  )
}
