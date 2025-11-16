# Quick Start Guide - Full Stack Setup

This guide will help you run both the backend API and the React frontend together.

## Prerequisites

- Python 3.8+ with virtual environment
- Node.js 18+
- MongoDB running (or MongoDB Atlas connection)
- Redis running (for Celery task queue)

## Backend Setup

### 1. Start MongoDB and Redis

```bash
# MongoDB (if running locally)
mongod

# Redis (if running locally)
redis-server
```

### 2. Start the Backend API

```bash
# From the project root
cd /mnt/c/Users/sufya/OneDrive/Desktop/EmoryHack

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Start FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend API will be running at `http://localhost:8000`

### 3. Start Celery Worker (in a new terminal)

```bash
# From the project root
cd /mnt/c/Users/sufya/OneDrive/Desktop/EmoryHack

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Start Celery worker
celery -A app.tasks worker --loglevel=info
```

## Frontend Setup

### 1. Install Dependencies

```bash
# Navigate to frontend directory
cd Frontend/12Tree-frontend

# Install dependencies
npm install
```

### 2. Start Development Server

```bash
# From Frontend/12Tree-frontend
npm run dev
```

The frontend will be running at `http://localhost:5173`

## Testing the Integration

1. Open your browser to `http://localhost:5173`
2. Navigate to **Learn** page (or click the tree icon in sidebar)
3. Make sure you're in **Music Mode** (should be default)
4. Enter a word in the input field (e.g., "ship", "treasure", "ocean")
5. Click **♫ Play ♫** button
6. Watch the progress bar as the song is generated (30-60 seconds)
7. When complete, the full-screen player will open with:
   - The generated audio
   - Karaoke-style scrolling lyrics
   - Playback controls

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                         Browser                              │
│                  http://localhost:5173                       │
│                                                              │
│  ┌────────────────────────────────────────────────────┐     │
│  │         React Frontend (Vite)                      │     │
│  │  • Music Mode component                            │     │
│  │  • API integration (src/api/index.ts)             │     │
│  │  • Full-screen player with lyrics                 │     │
│  └────────────────────────────────────────────────────┘     │
│                           │                                  │
│                           │ Vite Proxy                       │
│                           ▼                                  │
└───────────────────────────┼──────────────────────────────────┘
                            │
                            │ HTTP Requests
                            │
┌───────────────────────────▼──────────────────────────────────┐
│                    Backend API                               │
│              http://localhost:8000                           │
│                                                              │
│  ┌────────────────────────────────────────────────────┐     │
│  │         FastAPI Server                             │     │
│  │  • POST /api/generate - Start generation          │     │
│  │  • GET /api/jobs/{id} - Poll status               │     │
│  │  • /outputs/* - Serve audio files                 │     │
│  └────────────────────────────────────────────────────┘     │
│                           │                                  │
│                           │ Celery Task                      │
│                           ▼                                  │
│  ┌────────────────────────────────────────────────────┐     │
│  │         Celery Worker                              │     │
│  │  • Generate lyrics (GPT-4)                        │     │
│  │  • Create beat/music                              │     │
│  │  • Generate vocals (Bark/ElevenLabs)              │     │
│  │  • Mix audio                                      │     │
│  └────────────────────────────────────────────────────┘     │
│                           │                                  │
│                           ▼                                  │
│  ┌────────────────────────────────────────────────────┐     │
│  │         MongoDB                                    │     │
│  │  • Jobs collection (status tracking)              │     │
│  │  • SongCache collection (completed songs)         │     │
│  └────────────────────────────────────────────────────┘     │
└──────────────────────────────────────────────────────────────┘
```

## Data Flow

1. **User Input** → User enters a word (e.g., "ship")
2. **Frontend** → Calls `POST /api/generate { word: "ship" }`
3. **Backend** → Creates Celery task, returns `job_id`
4. **Frontend** → Polls `GET /api/jobs/{job_id}` every 2 seconds
5. **Celery Worker** → Processes task:
   - Generates pirate-themed lyrics
   - Creates musical beat
   - Generates vocals
   - Mixes final audio
6. **Backend** → Updates job status in MongoDB
7. **Frontend** → Receives completed result with:
   - `lyrics`: Generated song lyrics
   - `audio_url`: Path to audio file
   - `duration`, `bpm`, `timings`
8. **Frontend** → Displays in full-screen player

## Troubleshooting

### Backend won't start
- Check MongoDB is running
- Check Redis is running
- Verify all environment variables are set
- Check logs for missing dependencies

### Frontend won't start
- Run `npm install` to ensure dependencies are installed
- Check Node.js version (18+ required)
- Clear node_modules and reinstall if needed

### Songs not generating
- Check Celery worker is running
- Check backend logs for errors
- Verify API keys are configured (OpenAI, ElevenLabs, etc.)
- Check MongoDB connection

### Lyrics not displaying
- Verify backend returns `lyrics` field
- Check browser console for errors
- Ensure audio file is accessible at `/outputs/*`

### CORS errors
- The Vite proxy should handle CORS automatically
- If issues persist, check backend CORS settings in `app/main.py`

## Next Steps

- Customize the frontend theme in `tailwind.config.ts`
- Add more features to the Music Mode
- Implement the Library persistence (save songs)
- Add user authentication
- Deploy to production

## Support

For detailed integration documentation, see:
- Frontend: `Frontend/12Tree-frontend/INTEGRATION.md`
- Frontend README: `Frontend/12Tree-frontend/README.md`
