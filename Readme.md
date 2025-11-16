# 🎵 12Tree - AI-Powered Educational Song Generator for Kids

> **Transform any topic into gentle, educational songs for preschoolers (ages 3-5)**

Built for **EmoryHack 2024** | Powered by AI | Designed for Learning

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.0-61DAFB?logo=react)](https://reactjs.org/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-47A248?logo=mongodb)](https://www.mongodb.com/)
[![ElevenLabs](https://img.shields.io/badge/ElevenLabs-TTS-blueviolet)](https://elevenlabs.io/)
[![Gemini](https://img.shields.io/badge/Gemini-2.5_Flash-4285F4?logo=google)](https://ai.google.dev/)

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [System Flow](#-system-flow)
- [Project Structure](#-project-structure)
- [Quick Start](#-quick-start)
- [Detailed Setup](#-detailed-setup)
- [API Documentation](#-api-documentation)
- [Frontend Features](#-frontend-features)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🌟 Overview

**12Tree** is an AI-powered educational platform that generates custom songs for preschool children. Simply enter any topic (like "sun", "butterfly", or "friendship"), and our system creates:

- ✅ Gentle, age-appropriate lyrics that teach concepts
- ✅ Professional singing vocals via ElevenLabs AI
- ✅ Custom background music perfectly synced
- ✅ Beautiful karaoke-style player
- ✅ Personal library to save favorites

**Perfect for:**
- 👶 Parents teaching their toddlers
- 👨‍🏫 Preschool teachers creating lesson content
- 🎓 Educational content creators
- 🏠 Homeschooling families

---

## 🎯 Key Features

### 🎨 For Users
- **Instant Song Generation**: Create custom educational songs in 30-60 seconds
- **User Authentication**: Secure sign-up/login with password hashing (bcrypt)
- **Personal Library**: Save and organize your favorite songs
- **Beautiful UI**: Colorful, kid-friendly interface with smooth animations
- **Karaoke Mode**: Display all lyrics while song plays
- **Multi-User Support**: Each user has their own private library

### 🤖 AI & Technology
- **Smart Lyrics**: Gemini 2.5 Flash generates meaningful, educational content
- **Realistic Singing**: ElevenLabs TTS with singing voice configuration
- **Custom Music**: Randomly selected background tracks trimmed to vocal length
- **Audio Mixing**: Professional-quality mixing with fade-outs
- **Caching System**: Instant replay of previously generated songs
- **Async Processing**: Real-time progress updates during generation

### 🎓 Educational Focus
- **Age-Appropriate**: Gentle, soothing content for 3-5 year olds
- **Meaningful Lyrics**: Each line teaches something about the topic
- **Natural Language**: Simple words kids already know
- **Safe Content**: No harsh words, pirate exclamations, or inappropriate themes
- **Clear Pronunciation**: Optimized for learning and sing-along

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    12Tree Architecture                       │
└─────────────────────────────────────────────────────────────┘

┌──────────────────┐          ┌──────────────────────────────┐
│                  │          │       Backend Layer          │
│  React Frontend  │◄────────►│  FastAPI + Celery + Redis    │
│  (TypeScript)    │  REST    │                              │
│                  │   API    │  ┌────────────────────────┐  │
│  - Login/Signup  │          │  │  Core Services:        │  │
│  - Music Mode    │          │  │  - User Auth (bcrypt)  │  │
│  - Library       │          │  │  - Lyrics (Gemini)     │  │
│  - Karaoke UI    │          │  │  - Vocals (ElevenLabs) │  │
│                  │          │  │  - Audio Mixing        │  │
└──────────────────┘          │  │  - Background Music    │  │
                              │  └────────────────────────┘  │
                              │                              │
                              │  ┌────────────────────────┐  │
                              │  │  Task Queue:           │  │
                              │  │  - Celery Workers      │  │
                              │  │  - Redis Broker        │  │
                              │  └────────────────────────┘  │
                              └──────────────────────────────┘
                                           │
                                           ▼
┌─────────────────────────────────────────────────────────────┐
│                     Data & Storage                          │
├─────────────────────────────────────────────────────────────┤
│  MongoDB Atlas                                              │
│  - Users (authentication)                                   │
│  - UserLibrary (saved songs per user)                       │
│  - SongCache (generated songs)                              │
│  - Jobs (task status)                                       │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    External APIs                            │
├─────────────────────────────────────────────────────────────┤
│  🤖 Gemini 2.5 Flash    → Lyrics Generation                │
│  🎙️  ElevenLabs TTS      → Singing Voice Synthesis         │
│  🎵 Custom Music Files  → Background Instrumentals          │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 Tech Stack

### Frontend
| Technology | Version | Purpose |
|-----------|---------|---------|
| **React** | 18.x | UI framework |
| **TypeScript** | 5.x | Type safety |
| **Vite** | 5.x | Build tool & dev server |
| **Tailwind CSS** | 3.x | Styling |
| **React Router** | 6.x | Navigation |

### Backend
| Technology | Version | Purpose |
|-----------|---------|---------|
| **FastAPI** | 0.104+ | REST API framework |
| **Python** | 3.10+ | Backend language |
| **Celery** | 5.3+ | Async task queue |
| **Redis** | 5.0+ | Message broker |
| **Pydantic** | 2.5+ | Data validation |
| **bcrypt** | 4.1+ | Password hashing |

### Database
| Technology | Version | Purpose |
|-----------|---------|---------|
| **MongoDB** | 6.0+ | Primary database |
| **Beanie** | 1.24+ | Async ODM |
| **Motor** | 3.3+ | Async MongoDB driver |

### AI & Audio
| Technology | Version | Purpose |
|-----------|---------|---------|
| **Gemini API** | 2.5 Flash | Lyrics generation |
| **ElevenLabs** | 1.5+ | TTS singing vocals |
| **Bark** | Latest | Fallback TTS |
| **pydub** | 0.25+ | Audio processing |
| **librosa** | 0.10+ | Audio analysis |

---

## 🔄 System Flow

### Song Generation Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                    Song Generation Flow                         │
└─────────────────────────────────────────────────────────────────┘

1. USER INPUT
   │
   ├─► User enters topic (e.g., "butterfly")
   │
   ▼

2. RHYME GENERATION
   │
   ├─► pronouncing library finds kid-friendly rhyming words
   ├─► Filters out pirate/harsh words
   │
   ▼

3. LYRICS CREATION (Gemini AI)
   │
   ├─► Prompt: "Create gentle, educational song about [topic]"
   ├─► Requirements: 4-6 lines, age-appropriate, meaningful
   ├─► Safety filter: Remove any pirate exclamations
   ├─► Output: Clean, educational lyrics
   │
   ▼

4. VOCAL SYNTHESIS (ElevenLabs)
   │
   ├─► Format: "[singing gently and sweetly like a lullaby]"
   ├─► Settings: style=0.8, stability=0.3 for singing
   ├─► Voice: Child-friendly preset
   ├─► Output: High-quality singing vocals (.mp3)
   │
   ▼

5. BACKGROUND MUSIC
   │
   ├─► Select random track from 4 custom tracks
   ├─► Trim to exact vocal duration
   ├─► Apply 1-second fade-out
   │
   ▼

6. AUDIO MIXING
   │
   ├─► Load vocals and background
   ├─► Mix: vocals (100%) + instrumental (40%)
   ├─► Export final song (.mp3, 192kbps)
   │
   ▼

7. METADATA & CACHING
   │
   ├─► Calculate BPM, duration
   ├─► Generate timings for karaoke
   ├─► Save to MongoDB SongCache
   ├─► Return to user (instant on replay!)
   │
   ▼

8. USER LIBRARY
   │
   └─► User can save to personal library
       └─► Stored in MongoDB with user_id
```

### User Authentication Flow

```
SIGNUP                           LOGIN
   │                               │
   ├─► Username + Email + Password │
   ├─► Validate (unique, length)   ├─► Username + Password
   ├─► Hash password (bcrypt)      ├─► Find user in MongoDB
   ├─► Save to MongoDB Users       ├─► Verify password
   ├─► Auto-login                  ├─► Update last_login
   │                               │
   └────────────────┬──────────────┘
                    │
                    ▼
           Store in localStorage
                    │
                    ▼
          User can access library
```

---

## 📁 Project Structure

```
EmoryHack/
│
├── Frontend/                          # React Frontend
│   └── 12Tree-frontend/
│       ├── src/
│       │   ├── api/
│       │   │   └── index.ts          # API client, auth functions
│       │   ├── components/
│       │   │   ├── FullScreenPlayer.tsx    # Karaoke player
│       │   │   ├── MusicMode.tsx           # Song generation UI
│       │   │   ├── LibrarySongItem.tsx     # Library items
│       │   │   └── Toast.tsx               # Notifications
│       │   ├── pages/
│       │   │   ├── Login.tsx               # Login page
│       │   │   ├── Signup.tsx              # Signup page
│       │   │   ├── Library.tsx             # User's saved songs
│       │   │   └── Learn.tsx               # Main dashboard
│       │   ├── context/
│       │   │   └── AppContext.tsx          # Global state (user)
│       │   ├── hooks/
│       │   │   └── useSongs.ts             # Fetch user library
│       │   └── main.tsx                    # App entry point
│       ├── package.json
│       └── vite.config.ts
│
├── app/                               # FastAPI Backend
│   ├── main.py                        # FastAPI application
│   ├── config.py                      # Settings (env variables)
│   ├── database.py                    # MongoDB connection
│   ├── models.py                      # Beanie models
│   │                                  #  - User
│   │                                  #  - Job
│   │                                  #  - SongCache
│   │                                  #  - UserLibrary
│   ├── tasks.py                       # Celery background tasks
│   └── services/
│       ├── rhyme_service.py           # Rhyme generation
│       ├── lyrics_service.py          # Gemini lyrics AI
│       ├── vocal_service.py           # ElevenLabs/Bark TTS
│       ├── background_music_service.py # Music track manager
│       ├── beat_generator.py          # Fallback beat generator
│       └── audio_service.py           # Audio mixing utilities
│
├── background_music/                  # Custom Music Tracks
│   ├── track1.mp3
│   ├── track2.mp3
│   ├── track3.mp3
│   ├── track4.mp3
│   └── README.md
│
├── outputs/                           # Generated songs
├── temp/                              # Temporary files
├── Docs/                              # Documentation
│   ├── QUICKSTART.md
│   ├── CUSTOM_MUSIC_SETUP.md
│   ├── OPTIMIZATION_GUIDE.md
│   └── ...
│
├── requirements.txt                   # Python dependencies
├── .env                               # Environment variables
├── .env.example                       # Template
└── README.md                          # This file
```

---

## 🚀 Quick Start

### Prerequisites

Ensure you have the following installed:
- **Node.js** 18+ and **npm**
- **Python** 3.10+
- **MongoDB** (local or Atlas)
- **Redis** (local or cloud)

### 1. Clone Repository

```bash
git clone <your-repo-url>
cd EmoryHack
```

### 2. Backend Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
nano .env  # Add your API keys
```

**Required Environment Variables:**
```bash
# .env file
GEMINI_API_KEY=your_gemini_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
MONGODB_URL=your_mongodb_connection_string
REDIS_URL=redis://localhost:6379/0

# Optional
USE_CUSTOM_BACKGROUND_MUSIC=True
TTS_PROVIDER=elevenlabs
```

### 3. Frontend Setup

```bash
cd Frontend/12Tree-frontend

# Install dependencies
npm install

# Configure API URL (if needed)
echo "VITE_API_URL=http://localhost:8000" > .env

# Build for production (optional)
npm run build
```

### 4. Add Background Music (Optional)

Place your 4 MP3 tracks in `background_music/`:
```bash
background_music/
├── track1.mp3
├── track2.mp3
├── track3.mp3
└── track4.mp3
```

### 5. Start Services

**Terminal 1 - Redis:**
```bash
redis-server
```

**Terminal 2 - MongoDB:**
```bash
mongod  # If running locally
# Or use MongoDB Atlas (cloud)
```

**Terminal 3 - Celery Worker:**
```bash
cd EmoryHack
source venv/bin/activate
celery -A app.tasks worker --loglevel=info
```

**Terminal 4 - FastAPI Backend:**
```bash
cd EmoryHack
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 5 - React Frontend:**
```bash
cd Frontend/12Tree-frontend
npm run dev
```

### 6. Access Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## 📖 Detailed Setup

### MongoDB Setup

**Option 1: Local MongoDB**
```bash
# Install MongoDB
# Ubuntu/Debian:
sudo apt-get install mongodb

# macOS:
brew install mongodb-community

# Start MongoDB
mongod
```

**Option 2: MongoDB Atlas (Recommended)**
1. Go to https://www.mongodb.com/cloud/atlas
2. Create free M0 cluster
3. Get connection string
4. Add to `.env`: `MONGODB_URL=mongodb+srv://...`

### Redis Setup

**Option 1: Local Redis**
```bash
# Ubuntu/Debian:
sudo apt-get install redis-server

# macOS:
brew install redis

# Start Redis
redis-server
```

**Option 2: Redis Cloud (Recommended)**
1. Go to https://redis.com/try-free/
2. Create free 30MB database
3. Get connection URL
4. Add to `.env`: `REDIS_URL=redis://...`

### Get API Keys

**Gemini API (Free):**
1. Visit https://ai.google.dev/
2. Click "Get API Key"
3. Create new key
4. Add to `.env`: `GEMINI_API_KEY=...`

**ElevenLabs API:**
1. Visit https://elevenlabs.io/
2. Sign up for free account (10,000 characters/month)
3. Get API key from settings
4. Add to `.env`: `ELEVENLABS_API_KEY=...`

---

## 📚 API Documentation

### Authentication Endpoints

#### Sign Up
```http
POST /api/auth/signup
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure123"
}
```

**Response:**
```json
{
  "message": "Account created successfully",
  "user": {
    "username": "john_doe",
    "email": "john@example.com"
  }
}
```

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "john_doe",
  "password": "secure123"
}
```

**Response:**
```json
{
  "message": "Login successful",
  "user": {
    "username": "john_doe",
    "email": "john@example.com"
  }
}
```

### Song Generation Endpoints

#### Generate Song
```http
POST /api/generate
Content-Type: application/json

{
  "word": "butterfly"
}
```

**Response:**
```json
{
  "job_id": "abc-123-def-456",
  "status": "processing",
  "progress": 0
}
```

#### Get Job Status
```http
GET /api/jobs/{job_id}
```

**Response (Processing):**
```json
{
  "job_id": "abc-123",
  "status": "processing",
  "progress": 45,
  "error": null
}
```

**Response (Completed):**
```json
{
  "job_id": "abc-123",
  "status": "completed",
  "progress": 100,
  "result": {
    "word": "butterfly",
    "lyrics": "The butterfly is soft and light\nIt dances in the air...",
    "audio_url": "/outputs/song_abc123.mp3",
    "timings": [
      {"word": "The", "start": 0.0, "end": 0.2},
      {"word": "butterfly", "start": 0.2, "end": 0.8}
    ],
    "duration": 25.5,
    "bpm": 95.0
  }
}
```

### Library Endpoints

#### Save Song to Library
```http
POST /api/library/songs
Content-Type: application/json

{
  "userId": "john_doe",
  "title": "The Butterfly Song",
  "lyrics": "...",
  "audioUrl": "/outputs/song_abc.mp3",
  "timings": [...],
  "duration": 25.5,
  "bpm": 95.0
}
```

#### Get User's Library
```http
GET /api/library/songs?user_id=john_doe
```

**Response:**
```json
{
  "songs": [
    {
      "id": "507f1f77bcf86cd799439011",
      "title": "The Butterfly Song",
      "lyrics": "...",
      "audioUrl": "/outputs/song_abc.mp3",
      "timings": [...],
      "duration": 25.5,
      "bpm": 95.0,
      "addedAt": "2024-11-15T12:00:00"
    }
  ]
}
```

#### Delete from Library
```http
DELETE /api/library/songs/{song_id}
```

### Cache Endpoints

#### Get Cached Song
```http
GET /api/cache/{word}
```

#### Delete Cached Song
```http
DELETE /api/cache/{word}
```

---

## 🎨 Frontend Features

### Pages

1. **Login / Signup**
   - Secure authentication with validation
   - Password confirmation
   - Auto-login after signup

2. **Music Mode**
   - Topic input with instant validation
   - Real-time progress bar (0-100%)
   - Full-screen karaoke player
   - Add to library button

3. **Library**
   - Display all saved songs
   - Play songs instantly (from cache)
   - Delete songs
   - Empty state UI

4. **Karaoke Player**
   - Full-screen gradient background
   - Display all lyrics at once (no line-by-line)
   - Play/pause, skip ±5s controls
   - Progress bar with seek
   - Beautiful animations

### User Experience

- **Responsive Design**: Works on desktop, tablet, mobile
- **Smooth Animations**: Tailwind transitions and transforms
- **Toast Notifications**: Success/error messages
- **Loading States**: Skeletons and spinners
- **Error Handling**: User-friendly error messages
- **Persistent Auth**: localStorage for staying logged in

---

## 🌐 Deployment

### Backend Deployment (Railway/Render)

1. **Railway** (Recommended):
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy
railway up
```

2. **Environment Variables**:
   - Add all `.env` variables to Railway dashboard
   - Set `MONGODB_URL` to Atlas connection string
   - Set `REDIS_URL` to Redis Cloud URL

3. **Start Command**:
```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Frontend Deployment (Vercel/Netlify)

**Vercel:**
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
cd Frontend/12Tree-frontend
vercel --prod
```

**Build Settings:**
- Build Command: `npm run build`
- Output Directory: `dist`
- Environment Variable: `VITE_API_URL=https://your-backend.railway.app`

### MongoDB Atlas

1. Create M0 free cluster
2. Add IP whitelist (0.0.0.0/0 for development)
3. Create database user
4. Get connection string
5. Replace in `.env`

### Redis Cloud

1. Create 30MB free database at https://redis.com/try-free/
2. Get connection URL
3. Replace in `.env`

---

## 🎯 Core Algorithm: Song Generation

```python
# Simplified pseudocode

def generate_song(word: str):
    # 1. Find rhymes (5-10%)
    rhymes = get_kid_friendly_rhymes(word)

    # 2. Generate lyrics (15-25%)
    lyrics = gemini.create_gentle_educational_song(
        topic=word,
        rhymes=rhymes,
        style="gentle, educational, lullaby-like"
    )

    # 3. Clean lyrics (30%)
    lyrics = remove_pirate_exclamations(lyrics)
    lyrics = remove_structure_labels(lyrics)

    # 4. Generate vocals (40-60%)
    vocals = elevenlabs.text_to_speech(
        text=f"[singing gently and sweetly like a lullaby]\n{lyrics}",
        voice="child_friendly",
        settings={"style": 0.8, "stability": 0.3}
    )

    # 5. Select background music (65-70%)
    track = random.choice(background_tracks)
    duration = get_audio_duration(vocals)
    background = trim_and_fade(track, duration)

    # 6. Mix audio (75-90%)
    final = mix(
        vocals=vocals,
        background=background,
        vocals_volume=1.0,
        background_volume=0.4
    )

    # 7. Generate metadata (95-100%)
    bpm = detect_bpm(final)
    timings = generate_karaoke_timings(vocals, lyrics)

    # 8. Cache and return
    cache.save(word, final, lyrics, timings, bpm)
    return {
        "lyrics": lyrics,
        "audio_url": final.url,
        "timings": timings,
        "duration": duration,
        "bpm": bpm
    }
```

---

## 🔐 Security Features

- ✅ **Password Hashing**: bcrypt with salt
- ✅ **Input Validation**: Pydantic models
- ✅ **SQL Injection Prevention**: NoSQL (MongoDB)
- ✅ **CORS Protection**: Configured origins
- ✅ **Rate Limiting**: Celery task limits
- ✅ **User Isolation**: Per-user libraries
- ✅ **Environment Variables**: Sensitive data in `.env`

---

## 🧪 Testing

### Backend Tests
```bash
# Install pytest
pip install pytest pytest-asyncio

# Run tests
pytest tests/
```

### Frontend Tests
```bash
# Install testing library
npm install --save-dev @testing-library/react

# Run tests
npm test
```

---

## 📊 Performance Metrics

| Metric | Value |
|--------|-------|
| Song Generation Time | 30-60 seconds |
| Cached Song Load | < 1 second |
| API Response Time | < 100ms |
| Frontend Load Time | < 2 seconds |
| Database Query Time | < 50ms |

---

## 🤝 Contributing

We welcome contributions! Here's how:

1. **Fork** the repository
2. **Create** a feature branch
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit** your changes
   ```bash
   git commit -m 'Add amazing feature'
   ```
4. **Push** to the branch
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open** a Pull Request

### Code Style

- **Python**: Follow PEP 8, use black formatter
- **TypeScript**: Follow ESLint rules, use prettier
- **Commits**: Use conventional commits (feat:, fix:, docs:)

---

## 📝 License

This project is created for **EmoryHack 2024** hackathon.

For educational and demonstration purposes only.

---

## 🙏 Acknowledgments

- **Google Gemini** - Free, powerful AI for lyrics generation
- **ElevenLabs** - Professional TTS with singing capabilities
- **Suno Bark** - Open-source fallback TTS
- **MongoDB Atlas** - Free cloud database
- **Redis Cloud** - Free cache and task queue
- **FastAPI** - Modern, fast Python web framework
- **React** - Powerful UI library
- **Tailwind CSS** - Beautiful styling system

---

## 👥 Team

Built with ❤️ by the **12Tree Team** for EmoryHack 2024

---

## 📞 Contact & Support

- **Issues**: Open an issue on GitHub
- **Questions**: Check the `/Docs` folder
- **Demo**: [Live Demo Link](#) (if deployed)

---

## 🎉 Try It Now!

```bash
# 1. Clone
git clone <repo-url>
cd EmoryHack

# 2. Setup Backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Add your API keys!

# 3. Setup Frontend
cd Frontend/12Tree-frontend
npm install

# 4. Start Everything
# Terminal 1: redis-server
# Terminal 2: celery -A app.tasks worker --loglevel=info
# Terminal 3: uvicorn app.main:app --reload
# Terminal 4: npm run dev

# 5. Visit http://localhost:5173
```

**That's it! Start creating educational songs! 🎵**

---

<div align="center">

**Made with 💜 for preschool learners everywhere**

⭐ Star this repo if you found it helpful!

</div>
