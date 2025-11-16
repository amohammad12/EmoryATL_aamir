type Props = { className?: string }
export default function TreeLogo({ className }: Props) {
  return (
    <svg
      className={className}
      viewBox="0 0 64 64"
      xmlns="http://www.w3.org/2000/svg"
      aria-label="12Tree logo"
      role="img"
    >
      <defs>
        <linearGradient id="g" x1="0" x2="1">
          <stop offset="0%" stopColor="#B4F461" />
          <stop offset="100%" stopColor="#FF9ECF" />
        </linearGradient>
      </defs>
      <circle cx="32" cy="28" r="18" fill="url(#g)" />
      <rect x="28" y="30" width="8" height="18" rx="3" fill="#8B5E3C" />
      <path d="M20 24c6 2 10-6 16-4 4 1 6 6 10 6" stroke="#6B7280" strokeWidth="2" fill="none" />
      <text x="14" y="20" fontFamily="Poppins, sans-serif" fontWeight="800" fontSize="10" fill="#1F2937">12</text>
      <text x="32" y="20" fontFamily="Poppins, sans-serif" fontWeight="800" fontSize="10" fill="#1F2937">♪</text>
    </svg>
  )
}
