import type { Config } from 'tailwindcss'

export default {
  content: [
    './index.html',
    './src/**/*.{ts,tsx}',
  ],
  theme: {
    extend: {
      fontFamily: {
        display: ['Poppins', 'system-ui', 'sans-serif'],
      },
      colors: {
        skybg: '#CFEAFF',
        lime: '#B4F461',
        orange: '#FFB86B',
        yellow: '#FFE082',
        pink: '#FF9ECF',
        purple: '#C4B5FD',
      },
      boxShadow: {
        soft: '0 8px 24px rgba(0,0,0,0.08)',
      },
      borderRadius: {
        xl: '1.25rem',
        '2xl': '1.75rem',
      },
    },
  },
  plugins: [],
} satisfies Config
