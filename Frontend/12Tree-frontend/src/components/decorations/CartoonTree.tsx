type Props = {
  className?: string
  style?: React.CSSProperties
  variant?: 1 | 2 | 3
}

export default function CartoonTree({ className = '', style = {}, variant = 1 }: Props) {
  if (variant === 1) {
    // Round puffy tree
    return (
      <svg className={className} style={style} viewBox="0 0 100 120" fill="none">
        {/* Trunk */}
        <rect x="42" y="70" width="16" height="50" rx="4" fill="#8B6F47" />
        
        {/* Foliage - 3 overlapping circles */}
        <circle cx="50" cy="45" r="28" fill="#7BC950" />
        <circle cx="35" cy="55" r="22" fill="#6BB540" />
        <circle cx="65" cy="55" r="22" fill="#6BB540" />
        
        {/* Highlights */}
        <circle cx="45" cy="40" r="8" fill="#8FD863" opacity="0.7" />
        <circle cx="60" cy="48" r="6" fill="#8FD863" opacity="0.7" />
      </svg>
    )
  } else if (variant === 2) {
    // Pine/Christmas tree style
    return (
      <svg className={className} style={style} viewBox="0 0 100 120" fill="none">
        {/* Trunk */}
        <rect x="43" y="80" width="14" height="40" rx="3" fill="#8B6F47" />
        
        {/* Foliage - triangular layers */}
        <path d="M50 20 L70 50 L30 50 Z" fill="#5FAD41" />
        <path d="M50 40 L75 70 L25 70 Z" fill="#6BB540" />
        <path d="M50 60 L80 90 L20 90 Z" fill="#7BC950" />
      </svg>
    )
  } else {
    // Bushy tree
    return (
      <svg className={className} style={style} viewBox="0 0 100 120" fill="none">
        {/* Trunk */}
        <rect x="40" y="75" width="20" height="45" rx="5" fill="#8B6F47" />
        
        {/* Foliage - irregular rounded shape */}
        <ellipse cx="50" cy="50" rx="35" ry="30" fill="#7BC950" />
        <ellipse cx="35" cy="55" rx="25" ry="28" fill="#6BB540" />
        <ellipse cx="65" cy="55" rx="25" ry="28" fill="#6BB540" />
        <ellipse cx="50" cy="35" rx="28" ry="25" fill="#8FD863" />
        
        {/* Highlights */}
        <ellipse cx="42" cy="45" rx="10" ry="8" fill="#9FE873" opacity="0.6" />
        <ellipse cx="62" cy="50" rx="8" ry="7" fill="#9FE873" opacity="0.6" />
      </svg>
    )
  }
}
