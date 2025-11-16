# Backend Integration Guide

## Overview

This frontend is integrated with the Pirate Karaoke backend API to generate educational songs with lyrics.

## Backend Integration

### API Endpoints Used

1. **POST /api/generate**
   - Starts song generation for a given word/topic
   - Request: `{ word: string }`
   - Response: `{ job_id, status, progress?, result? }`

2. **GET /api/jobs/{job_id}**
   - Polls for job status and results
   - Response: `{ job_id, status, progress, error?, result? }`

3. **Static Files /outputs/**
   - Serves generated audio files

### Data Flow

1. User enters a topic/word in MusicMode
2. Frontend calls `POST /api/generate` with the word
3. Backend returns a job_id
4. Frontend polls `GET /api/jobs/{job_id}` every 2 seconds
5. Progress updates are displayed to the user
6. When complete, the result contains:
   - `word`: The input word
   - `lyrics`: Generated song lyrics
   - `audio_url`: Path to the generated audio file
   - `timings`: Word timing information
   - `duration`: Audio duration in seconds
   - `bpm`: Beats per minute

7. Frontend displays the song in FullScreenPlayer with:
   - Audio playback
   - Karaoke-style scrolling lyrics
   - Playback controls

## Development Setup

### Prerequisites

- Backend running on `http://localhost:8000`
- Node.js and npm installed

### Running the Frontend

```bash
# Install dependencies
npm install

# Start development server (with proxy to backend)
npm run dev
```

The development server will start on `http://localhost:5173` with proxy configured to forward API requests to the backend.

### Environment Variables

Create a `.env` file (see `.env.example`):

```env
# Leave empty for development (uses Vite proxy)
VITE_API_URL=

# For production, set to your backend URL:
# VITE_API_URL=https://your-backend.com
```

## Features Implemented

### Music Mode
- Text input for word/topic
- Real-time progress indicator during generation
- Error handling with user-friendly messages
- Automatic full-screen player on completion
- Add to library functionality

### Full-Screen Player
- Audio playback controls (play/pause, seek, rewind, fast-forward)
- Karaoke-style lyrics display
- Lyrics scroll and highlight in sync with audio
- Beautiful gradient background
- Close button to return to Music Mode

### Lyrics Display
- Lyrics are split by newline
- Current line is highlighted and enlarged
- Adjacent lines are visible but dimmed
- Smooth transitions between lines

## CORS Configuration

The Vite development server is configured with a proxy to avoid CORS issues:

```typescript
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true,
    },
    '/outputs': {
      target: 'http://localhost:8000',
      changeOrigin: true,
    },
  },
}
```

This means:
- `/api/*` requests are forwarded to `http://localhost:8000/api/*`
- `/outputs/*` requests are forwarded to `http://localhost:8000/outputs/*`

## Production Deployment

For production:

1. Set `VITE_API_URL` environment variable to your backend URL
2. Build the frontend: `npm run build`
3. Serve the `dist` folder
4. Ensure your backend has proper CORS headers configured

## Troubleshooting

### Backend Connection Issues
- Ensure backend is running on `http://localhost:8000`
- Check browser console for network errors
- Verify CORS is properly configured on backend

### Lyrics Not Displaying
- Check that backend returns `lyrics` field in the result
- Verify lyrics contain newline characters for proper splitting
- Inspect FullScreenPlayer component for any errors

### Audio Not Playing
- Verify `audio_url` is correctly returned from backend
- Check that audio files are accessible at `/outputs/*`
- Ensure audio files are in a browser-supported format (MP3, WAV)

## Testing

To test the integration:

1. Start the backend: `uvicorn app.main:app --reload`
2. Start the frontend: `npm run dev`
3. Navigate to Learn > Music Mode
4. Enter a word (e.g., "ship", "treasure", "ocean")
5. Click "♫ Play ♫"
6. Watch the progress indicator
7. When complete, verify:
   - Audio plays correctly
   - Lyrics are displayed
   - Lyrics highlight in sync with audio
   - All controls work (play/pause, seek, etc.)
