# 🏴‍☠️ Pirate Sea Shanty Karaoke Backend

Generate educational pirate-themed sea shanties with karaoke-style word highlighting for preschool kids (ages 3-5)!

## 🎯 Features

- **Pirate-Themed Lyrics**: Gemini AI generates kid-safe sea shanties with "Arr!" and "Yo-ho!" vocalizations
- **Bark AI Singing**: Expressive singing vocals using Suno's Bark TTS model
- **Karaoke Timing**: Word-by-word synchronization for sing-along
- **Auto Beat Matching**: BPM detection and instrumental selection
- **MongoDB Caching**: Instant responses for popular words
- **Async Processing**: Celery background tasks with real-time progress

## 🏗️ Architecture

```
FastAPI Backend (Python 3.10+)
├── MongoDB (Beanie ODM) - Database & caching
├── Redis + Celery - Async task queue
├── Gemini API - Lyrics generation
├── Bark TTS - Expressive singing synthesis (GPU-accelerated)
├── Librosa - Audio analysis & BPM detection
├── Pydub - Audio mixing
└── Aeneas - Karaoke word timing
```

## 📦 Project Structure

```
EmoryHack/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Settings management
│   ├── database.py          # MongoDB connection
│   ├── models.py            # Beanie models (Job, SongCache)
│   ├── tasks.py             # Celery background tasks
│   └── services/
│       ├── __init__.py
│       ├── rhyme_service.py      # Rhyme word generation
│       ├── lyrics_service.py     # Gemini AI pirate lyrics
│       ├── vocal_service.py      # Bark TTS singing synthesis
│       ├── beat_manager.py       # Beat library management
│       ├── audio_service.py      # Audio mixing & BPM
│       └── karaoke_service.py    # Aeneas word timing
├── beats/
│   └── pirate-shanty/       # Beat loop files (.wav)
├── outputs/                 # Generated songs (.mp3)
├── temp/                    # Temporary processing files
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variables template
├── setup.sh                 # Automated setup script
├── SETUP_PLAN.md            # Detailed setup instructions
├── IMPROVED_PLAN.md         # Full implementation plan
└── Readme.md                # This file
```

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.10+
- MongoDB 6.0+
- Redis 6.0+
- FFmpeg
- CUDA-capable GPU (recommended for Bark TTS)

### 2. One-Command Setup

```bash
chmod +x setup.sh
./setup.sh
```

### 3. Configure Environment

```bash
# Copy .env file
cp .env.example .env

# Edit and add your Gemini API key
nano .env
# GEMINI_API_KEY=your_key_here (get free at https://ai.google.dev/)
```

### 4. Start Services

**Terminal 1 - MongoDB:**
```bash
sudo systemctl start mongod  # Linux
brew services start mongodb-community  # macOS
```

**Terminal 2 - Celery Worker:**
```bash
source venv/bin/activate
celery -A app.tasks worker --loglevel=info
```

**Terminal 3 - FastAPI Server:**
```bash
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Test It!

```bash
# Generate a pirate shanty
curl -X POST http://localhost:8000/api/generate \
  -H 'Content-Type: application/json' \
  -d '{"word": "ship"}'

# Get the job status (replace JOB_ID)
curl http://localhost:8000/api/jobs/JOB_ID

# Download the generated song
http://localhost:8000/outputs/song_xxxxx.mp3
```

## 📖 Detailed Setup

See **[SETUP_PLAN.md](SETUP_PLAN.md)** for comprehensive installation instructions including:
- MongoDB setup (local & Atlas)
- Redis setup (local & Cloud)
- Troubleshooting
- Production deployment

## 🎵 API Endpoints

### Generate Song
```http
POST /api/generate
Content-Type: application/json

{
  "word": "ship"
}
```

**Response:**
```json
{
  "job_id": "abc-123",
  "status": "processing",
  "progress": 0
}
```

### Get Job Status
```http
GET /api/jobs/{job_id}
```

**Response:**
```json
{
  "job_id": "abc-123",
  "status": "completed",
  "progress": 100,
  "result": {
    "word": "ship",
    "lyrics": "Verse 1:\nOn a ship we sail (arr!)...",
    "audio_url": "/outputs/song_abc123.mp3",
    "timings": [
      {"word": "On", "start": 0.0, "end": 0.3},
      {"word": "a", "start": 0.3, "end": 0.5}
    ],
    "duration": 30.5,
    "bpm": 95.0
  }
}
```

### Get Cached Song
```http
GET /api/cache/{word}
```

### Health Check
```http
GET /health
```

## 🔧 Technologies

| Component | Technology | Why? |
|-----------|-----------|------|
| Web Framework | FastAPI | Fast, modern, async Python API |
| Database | MongoDB + Beanie | NoSQL, flexible schema, async |
| Task Queue | Celery + Redis | Background processing |
| LLM | Gemini API | Free, powerful, pirate-themed prompts |
| TTS | Bark (Suno) | Expressive singing, musical vocalizations! |
| Audio Processing | Librosa, Pydub | Industry standard |
| Karaoke Timing | Aeneas | Forced alignment |

## 💰 Cost Breakdown

| Service | Free Tier | Cost |
|---------|-----------|------|
| Gemini API | 60 req/min | $0 |
| Bark TTS | Open-source (local) | $0 |
| MongoDB Atlas | 512MB M0 | $0 |
| Redis Cloud | 30MB | $0 |
| GPU Hosting | Varies by provider | Variable (GPU required) |
| **TOTAL** | ~1000 songs/month | **Free + GPU costs** |

**Note:** Bark runs locally and is free but requires GPU for optimal performance.

## 🎓 Educational Value

Each shanty teaches kids:
- **Vocabulary**: Simple rhyming words
- **Rhythm**: Musical timing and tempo
- **Pirate Culture**: Fun maritime themes
- **Phonics**: Word pronunciation
- **Memory**: Repetitive chorus structure

## 🔒 Safety Features

- Kid-safe content filtering
- No violence, alcohol, or mature themes
- COPPA compliant (no PII collection)
- Educational focus
- Parental guidance prompts

## 📚 Documentation

- **[SETUP_PLAN.md](SETUP_PLAN.md)** - Complete installation guide
- **[IMPROVED_PLAN.md](IMPROVED_PLAN.md)** - Full technical specification
- **[Plan.md](Plan.md)** - Original design document

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📝 License

This project is created for EmoryHack hackathon.

## 🙏 Acknowledgments

- **Gemini API** by Google - Free LLM
- **Bark** by Suno - Open-source expressive TTS
- **Looperman.com** - Free beats
- **Aeneas** - Forced alignment
- **FastAPI** - Modern web framework
- **HuggingFace Transformers** - Model hosting and inference

## 🏴‍☠️ Arr! Let's Make Some Shanties!

Built with ❤️ for preschool pirates everywhere!

---

**Questions?** Check [SETUP_PLAN.md](SETUP_PLAN.md) or open an issue!
