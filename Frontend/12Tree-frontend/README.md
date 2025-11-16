# 12Tree – Sing to Learn (Frontend)

A React + TypeScript + Vite single-page app styled with Tailwind CSS. Optimized for tablets/laptops with a playful, preschool-friendly UI.

## Tech stack
- React 18 + TypeScript
- Vite 5
- React Router v6
- Tailwind CSS 3

## Scripts
- `npm run dev` – start dev server
- `npm run build` – production build
- `npm run preview` – preview built app

## Getting started

### Prerequisites
- Backend API running on `http://localhost:8000` (Pirate Karaoke Backend)
- Node.js 18+ installed

### Setup
1. Install dependencies
   ```bash
   npm install
   ```
2. (Optional) Configure environment variables
   ```bash
   cp .env.example .env
   # Edit .env if needed (default uses Vite proxy)
   ```
3. Start the dev server
   ```bash
   npm run dev
   ```
4. Open the URL printed by Vite (typically http://localhost:5173)

## Project structure
- `src/components/` shared UI: Sidebar, Header, ModeSwitcher, SongCard, LessonCard, FlashcardViewer, AudioPlayer, SongModal.
- `src/pages/` top-level routes: Library, Learn, MagicSongs, Cards.
- `src/context/` simple app context for user profile.
- `src/hooks/` hooks for songs/lessons.
- `src/api/` API stubs for integration.
- `src/styles/` Tailwind config lives at project root; global styles in `src/index.css`.

## Routes
- `/library` – Your songs (grid + modal)
- `/learn` – Lessons (hard skills + life skills)
- `/magic` – Magic songs (prompt → generated song demo)
- `/cards` – Flashcards (large card viewer)

## Backend Integration

This frontend is integrated with the Pirate Karaoke backend API. See [INTEGRATION.md](./INTEGRATION.md) for detailed documentation.

### Quick Overview
- **Music Mode**: Enter a word/topic → Backend generates a custom educational song
- **Real-time Progress**: Shows generation progress with a progress bar
- **Full-Screen Player**: Plays audio with karaoke-style scrolling lyrics
- **Caching**: Backend caches generated songs for instant replay

### API Endpoints
- `POST /api/generate` - Start song generation
- `GET /api/jobs/{job_id}` - Poll for job status and results
- `/outputs/*` - Serve generated audio files

## Notes
- Vite proxy configured to forward `/api` and `/outputs` requests to `http://localhost:8000`
- Tailwind theme includes pastel colors: skybg, lime, orange, yellow, pink, purple
- Keyboard/focus styles via `focus-ring` utility, ARIA labels on interactive elements
- Lyrics display with karaoke-style highlighting synced to audio playback
