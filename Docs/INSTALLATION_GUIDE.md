# 🏴‍☠️ Pirate Karaoke - Complete Installation Guide

## 📋 Table of Contents
1. [System Requirements](#system-requirements)
2. [Install System Dependencies](#install-system-dependencies)
3. [Python Virtual Environment](#python-virtual-environment)
4. [Install Python Libraries](#install-python-libraries)
5. [Tool-by-Tool Guide](#tool-by-tool-guide)
6. [Database Setup](#database-setup)
7. [Configuration](#configuration)
8. [Testing](#testing)
9. [Troubleshooting](#troubleshooting)

---

## System Requirements

### What You Have

- ✅ Python 3.12.3 (WSL2/Linux)
- ✅ WSL2 on Windows
- ✅ Project files downloaded

### What You Need to Install
- ❌ MongoDB 6.0+ (Database)
- ❌ Redis 6.0+ (Task queue)
- ❌ FFmpeg (Audio processing)
- ❌ System audio libraries
- ❌ Python virtual environment
- ❌ All Python packages

---

## PART 1: Install System Dependencies

### Step 1.1: Update System Packages

```bash
sudo apt update && sudo apt upgrade -y
```

**What this does:** Updates your package list and existing packages

### Step 1.2: Install FFmpeg & Audio Libraries

```bash
sudo apt install -y \
    ffmpeg \
    libsndfile1 \
    libsndfile1-dev \
    rubberband-cli \
    espeak-ng \
    build-essential \
    python3-dev \
    python3-pip \
    python3-venv
```

**What each does:**
- `ffmpeg`: Audio/video processing (required for mixing)
- `libsndfile1`: Sound file reading/writing
- `rubberband-cli`: Time-stretching audio (optional but useful)
- `espeak-ng`: Text-to-speech engine (fallback for TTS)
- `build-essential`: C/C++ compilers (needed for some Python packages)
- `python3-dev`: Python development headers
- `python3-pip`: Python package installer
- `python3-venv`: Virtual environment creator

**Verify installation:**
```bash
ffmpeg -version
which rubberband
```

---

## PART 2: Install MongoDB

### Option A: Install MongoDB on WSL2 (Recommended)

```bash
# Import MongoDB public GPG key
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -

# Add MongoDB repository
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list

# Update package list
sudo apt update

# Install MongoDB
sudo apt install -y mongodb-org

# Create data directory
sudo mkdir -p /data/db
sudo chown -R $USER /data/db

# Start MongoDB
sudo mongod --fork --logpath /var/log/mongodb.log --dbpath /data/db
```

**What MongoDB does:**
- Stores generated song data
- Caches lyrics for popular words
- Tracks job status for async tasks

**Verify MongoDB:**
```bash
mongosh --eval "db.version()"
# Should output: 6.0.x
```

### Option B: Use MongoDB Atlas (Cloud - Free)

If local install fails:
1. Go to https://www.mongodb.com/cloud/atlas
2. Create free M0 cluster (512MB)
3. Get connection string
4. Update `.env` with: `MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/`

---

## PART 3: Install Redis

### Install Redis on WSL2

```bash
# Install Redis
sudo apt install -y redis-server

# Start Redis
sudo service redis-server start

# Enable auto-start
sudo systemctl enable redis-server
```

**What Redis does:**
- Message broker for Celery (async task queue)
- Stores task results
- Manages background job processing

**Verify Redis:**
```bash
redis-cli ping
# Should output: PONG
```

### Alternative: Use Redis Cloud (Free)

1. Go to https://redis.com/try-free/
2. Create free 30MB database
3. Get connection URL
4. Update `.env` with: `REDIS_URL=redis://default:password@host:port`

---

## PART 4: Python Virtual Environment

### Create Virtual Environment

```bash
# Navigate to project directory
cd /mnt/c/Users/sufya/OneDrive/Desktop/EmoryHack

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# You should see (venv) in your prompt
```

**What a virtual environment does:**
- Isolates project dependencies
- Prevents conflicts with system Python
- Makes project portable

**To activate later:**
```bash
source venv/bin/activate
```

**To deactivate:**
```bash
deactivate
```

---

## PART 5: Install Python Libraries

### Upgrade pip first

```bash
python -m pip install --upgrade pip
```

### Install all requirements

```bash
pip install -r requirements.txt
```

This installs **42 packages**. It may take 5-10 minutes.

### If installation fails on specific packages:

**Aeneas (karaoke timing) - Known to fail:**
```bash
# Try with build flag
pip install aeneas --use-pep517

# If still fails, comment it out in requirements.txt
# The app will use fallback timing (still works!)
```

**Pyrubberband (time-stretching) - May fail:**
```bash
# Install rubberband first (already done above)
sudo apt install rubberband-cli
pip install pyrubberband
```

---

## PART 6: Tool-by-Tool Guide

### 1. FastAPI (Web Framework)
**What it does:** Creates REST API endpoints for frontend
**Used in:** `app/main.py`
**Key endpoints:**
- `POST /api/generate` - Generate new song
- `GET /api/jobs/{job_id}` - Check job status
- `GET /api/cache/{word}` - Get cached song

### 2. Beanie + Motor (MongoDB ODM)
**What it does:** Database operations with async support
**Used in:** `app/database.py`, `app/models.py`
**Models:**
- `Job`: Track song generation jobs
- `SongCache`: Cache completed songs

### 3. Celery + Redis (Background Tasks)
**What it does:** Process heavy tasks (song generation) in background
**Used in:** `app/tasks.py`
**Tasks:**
- `generate_song_task`: Main song generation
- `cleanup_old_files`: Remove old cached files

### 4. Gemini API (LLM for Lyrics)
**What it does:** Generates pirate-themed educational lyrics
**Used in:** `app/services/lyrics_service.py`
**Get free API key:** https://ai.google.dev/
**Prompts:** Creates rhyming verses with "Arr!" and "Yo-ho!"

### 5. Edge TTS (Text-to-Speech - FREE!)
**What it does:** Converts lyrics to natural-sounding vocals
**Used in:** `app/services/vocal_service.py`
**Voices available:**
- `en-US-JennyNeural` (female, friendly)
- `en-US-GuyNeural` (male)
- `en-GB-SoniaNeural` (British female)
**Cost:** 100% FREE, unlimited!

### 6. Librosa (Audio Analysis)
**What it does:** BPM detection, audio loading, beat tracking
**Used in:** `app/services/audio_service.py`
**Key functions:**
- `librosa.beat.beat_track()` - Detect BPM
- `librosa.load()` - Load audio files
- `librosa.frames_to_time()` - Convert frames to timestamps

### 7. Pydub (Audio Mixing)
**What it does:** Mix vocals + instrumentals, volume control
**Used in:** `app/services/audio_service.py`
**Key operations:**
- Overlay audio tracks
- Adjust volume (dB)
- Export MP3/WAV

### 8. Aeneas (Karaoke Word Timing)
**What it does:** Sync words to audio timestamps
**Used in:** `app/services/karaoke_service.py`
**Output:** `[{"word": "Arr", "start": 0.0, "end": 0.5}, ...]`
**Fallback:** If not installed, uses evenly distributed timing

### 9. Pronouncing + NLTK (Rhyme Generation)
**What it does:** Generate rhyming words for input
**Used in:** `app/services/rhyme_service.py`
**Example:**
- Input: "ship"
- Output: ["trip", "slip", "dip", "flip"]

### 10. Pyrubberband (Time-Stretching)
**What it does:** Match beat tempo to vocal BPM
**Used in:** `app/services/beat_manager.py`
**Example:** Stretch 90 BPM beat to match 95 BPM vocals

---

## PART 7: Download NLTK Data

```bash
# With venv activated
python -c "import nltk; nltk.download('cmudict')"
```

**What this does:** Downloads pronunciation dictionary for rhyme generation

---

## PART 8: Create Project Directories

```bash
# Create required directories
mkdir -p beats/pirate-shanty
mkdir -p outputs
mkdir -p temp

# Verify
ls -la
# You should see beats/, outputs/, temp/
```

**What each directory does:**
- `beats/pirate-shanty/`: Store instrumental beat loops (.wav files)
- `outputs/`: Final generated songs (.mp3)
- `temp/`: Temporary processing files (auto-cleaned)

---

## PART 9: Configure Environment Variables

### Create .env file

```bash
# Copy example file
cp .env.example .env

# Edit with your favorite editor
nano .env
# Or: vim .env
# Or: code .env (VS Code)
```

### Configure .env

```env
# ===== CRITICAL: Get free Gemini API key =====
GEMINI_API_KEY=YOUR_KEY_HERE
# Get at: https://ai.google.dev/

# ===== Redis =====
REDIS_URL=redis://localhost:6379/0

# ===== MongoDB =====
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=pirate_karaoke

# ===== Application Settings =====
SAMPLE_RATE=24000
MAX_CONCURRENT_JOBS=3
CACHE_EXPIRY_DAYS=7

# ===== Directories =====
BEATS_DIR=beats
OUTPUT_DIR=outputs
TEMP_DIR=temp

# ===== Audio Settings =====
VOCALS_VOLUME=1.0
INSTRUMENTAL_VOLUME=0.4
PIRATE_SHANTY_BPM_MIN=90
PIRATE_SHANTY_BPM_MAX=110

# ===== Edge TTS Settings =====
TTS_VOICE=en-US-JennyNeural
TTS_RATE=-10%
TTS_PITCH=+5Hz

# ===== Development =====
DEBUG=True
```

### Get Gemini API Key (Required!)

1. Go to https://ai.google.dev/
2. Click "Get API key in Google AI Studio"
3. Sign in with Google
4. Click "Create API Key"
5. Copy and paste into `.env`

**Free tier:** 60 requests/minute (plenty for testing!)

---

## PART 10: Initialize Beat Library (Optional)

If you have beat loops:

```bash
# Scan beats directory and detect BPM
python -c "from app.services.beat_manager import BeatLibraryManager; BeatLibraryManager().scan_beats_directory()"
```

**Where to get free beats:**
- https://www.looperman.com (search "pirate" or "sea shanty")
- https://www.youtube.com/audiolibrary
- https://incompetech.com
- https://freesound.org

Save as `.wav` files in `beats/pirate-shanty/`

---

## PART 11: Verify Complete Installation

### Check all dependencies:

```bash
# Python packages
pip list | grep -E "(fastapi|beanie|celery|edge-tts|librosa|pydub)"

# System tools
ffmpeg -version
mongosh --version
redis-cli --version

# NLTK data
python -c "import nltk; print(nltk.data.find('corpora/cmudict'))"

# Environment variables
python -c "from app.config import settings; print(settings.GEMINI_API_KEY[:10])"
```

---

## PART 12: Start the Application

You need **3 separate terminal windows**:

### Terminal 1: Check Services

```bash
# Check MongoDB
sudo mongod --fork --logpath /var/log/mongodb.log --dbpath /data/db

# Check Redis
sudo service redis-server status
# If not running: sudo service redis-server start

# Verify
mongosh --eval "db.version()"
redis-cli ping
```

### Terminal 2: Start Celery Worker

```bash
cd /mnt/c/Users/sufya/OneDrive/Desktop/EmoryHack
source venv/bin/activate
celery -A app.tasks worker --loglevel=info
```

**You should see:**
```
[tasks]
  . app.tasks.cleanup_old_files
  . app.tasks.generate_song_task

[INFO] Connected to redis://localhost:6379/0
[INFO] celery@YOUR-PC ready.
```

### Terminal 3: Start FastAPI Server

```bash
cd /mnt/c/Users/sufya/OneDrive/Desktop/EmoryHack
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**You should see:**
```
INFO: Uvicorn running on http://0.0.0.0:8000
INFO: Starting Pirate Karaoke API...
INFO: Connecting to MongoDB at mongodb://localhost:27017
INFO: Successfully connected to MongoDB database: pirate_karaoke
INFO: Application startup complete.
```

---

## PART 13: Test It!

### Test 1: Health Check

Open browser: http://localhost:8000/health

**Expected:**
```json
{
  "status": "healthy",
  "service": "pirate-karaoke",
  "database": "mongodb"
}
```

### Test 2: Generate a Pirate Shanty

```bash
# Generate song for word "ship"
curl -X POST http://localhost:8000/api/generate \
  -H 'Content-Type: application/json' \
  -d '{"word": "ship"}'
```

**Expected:**
```json
{
  "job_id": "abc-123-def-456",
  "status": "processing",
  "progress": 0
}
```

### Test 3: Check Job Status

```bash
# Replace JOB_ID with the ID from Test 2
curl http://localhost:8000/api/jobs/abc-123-def-456
```

**Keep checking every few seconds until:**
```json
{
  "job_id": "abc-123-def-456",
  "status": "completed",
  "progress": 100,
  "result": {
    "word": "ship",
    "lyrics": "Verse 1:\nOn a ship we sail (arr!)...",
    "audio_url": "/outputs/song_abc123.mp3",
    "timings": [...],
    "duration": 30.5,
    "bpm": 95.0
  }
}
```

### Test 4: Download Song

Open browser: http://localhost:8000/outputs/song_abc123.mp3

Or download:
```bash
wget http://localhost:8000/outputs/song_abc123.mp3
```

---

## Troubleshooting

### MongoDB Connection Error

```bash
# Check if running
ps aux | grep mongod

# Start manually
sudo mongod --fork --logpath /var/log/mongodb.log --dbpath /data/db

# Check logs
tail -f /var/log/mongodb.log
```

### Redis Connection Error

```bash
# Start Redis
sudo service redis-server start

# Check if listening
netstat -an | grep 6379

# Test connection
redis-cli ping
```

### Celery Import Errors

```bash
# Make sure venv is activated
source venv/bin/activate

# Reinstall requirements
pip install -r requirements.txt

# Check if modules are importable
python -c "from app.tasks import generate_song_task"
```

### ModuleNotFoundError

```bash
# Always activate venv first!
source venv/bin/activate

# Reinstall specific package
pip install <package-name>
```

### Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>

# Or use different port
uvicorn app.main:app --port 8001
```

### Aeneas Installation Fails

Aeneas is optional. If it fails:
```bash
# Edit requirements.txt
nano requirements.txt

# Comment out the line:
# aeneas==1.7.3

# The app will use fallback word timing (still works!)
```

---

## Next Steps

1. ✅ Test with various words: "treasure", "ocean", "parrot"
2. 📥 Download free pirate-themed beats
3. 🎨 Build a frontend (React recommended)
4. 🚀 Deploy to cloud (Railway.app or Render.com)

---

## Quick Command Reference

```bash
# Start MongoDB
sudo mongod --fork --logpath /var/log/mongodb.log --dbpath /data/db

# Start Redis
sudo service redis-server start

# Activate Python venv
source venv/bin/activate

# Start Celery worker
celery -A app.tasks worker --loglevel=info

# Start FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Generate song
curl -X POST http://localhost:8000/api/generate \
  -H 'Content-Type: application/json' \
  -d '{"word": "ship"}'

# Check job status
curl http://localhost:8000/api/jobs/{JOB_ID}
```

---

## 🏴‍☠️ Arr! You're Ready to Make Some Shanties!

If you get stuck, check:
- **MongoDB logs:** `tail -f /var/log/mongodb.log`
- **FastAPI logs:** In Terminal 3
- **Celery logs:** In Terminal 2

Built with ❤️ for preschool pirates everywhere!
