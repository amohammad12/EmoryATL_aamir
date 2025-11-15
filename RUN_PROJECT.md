# 🏴‍☠️ HOW TO RUN PIRATE KARAOKE PROJECT

## 📋 PRE-FLIGHT CHECKLIST

Before running the application, verify everything is ready:

### ✅ Step 1: Verify All Services

Run these commands to check everything:

```bash
# Check Redis is running
redis-cli ping
# Should return: PONG

# Check FFmpeg is installed
ffmpeg -version
# Should show version

# Check Python virtual environment exists
ls venv/bin/activate
# Should show the file exists

# Check .env file is configured
cat .env | grep -E "GEMINI_API_KEY|MONGODB_URL"
# Should show your API keys (not "your_gemini_api_key_here")
```

---

### ✅ Step 2: Start Redis (if not running)

```bash
# Start Redis
sudo service redis-server start

# Verify it's running
redis-cli ping
```

**Expected output:** `PONG`

---

### ✅ Step 3: Verify Setup (IMPORTANT!)

Run the complete setup test:

```bash
cd /mnt/c/Users/sufya/OneDrive/Desktop/EmoryHack
source venv/bin/activate
python test_setup.py
```

**This will check:**
- ✅ Environment variables configured
- ✅ All Python packages installed
- ✅ NLTK data downloaded
- ✅ FFmpeg working
- ✅ Redis connection
- ✅ MongoDB Atlas connection
- ✅ Directories exist
- ✅ App can initialize

**You MUST see this at the end:**
```
✅ ALL TESTS PASSED!

🎉 Your Pirate Karaoke app is ready!
```

**If any tests fail, fix them before continuing!**

---

## 🚀 RUNNING THE APPLICATION

You need **2 separate terminal windows** running at the same time.

### 🖥️ Terminal 1: Start Celery Worker

**Purpose:** Processes background tasks (song generation)

```bash
# Open WSL terminal
wsl

# Navigate to project
cd /mnt/c/Users/sufya/OneDrive/Desktop/EmoryHack

# Activate virtual environment
source venv/bin/activate

# Start Celery worker
celery -A app.tasks worker --loglevel=info
```

**✅ SUCCESS LOOKS LIKE:**
```
 -------------- celery@your-pc v5.5.3
---- **** -----
--- * ***  * -- Linux...
-- * - **** ---

[config]
.> app:         pirate_karaoke
.> transport:   redis://localhost:6379/0
.> results:     redis://localhost:6379/0

[tasks]
  . app.tasks.cleanup_old_files
  . app.tasks.generate_song_task

[INFO] Connected to redis://localhost:6379/0
[INFO] celery@your-pc ready.
```

**⚠️ KEEP THIS TERMINAL OPEN AND RUNNING!**

---

### 🖥️ Terminal 2: Start FastAPI Server

**Purpose:** Web server that handles API requests

**Open a NEW terminal window:**

```bash
# Open WSL terminal (new window)
wsl

# Navigate to project
cd /mnt/c/Users/sufya/OneDrive/Desktop/EmoryHack

# Activate virtual environment
source venv/bin/activate

# Start FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**✅ SUCCESS LOOKS LIKE:**
```
INFO: Will watch for changes in these directories: ['/mnt/c/Users/sufya/OneDrive/Desktop/EmoryHack']
INFO: Uvicorn running on http://0.0.0.0:8000
INFO: Started server process [12345]
INFO: Waiting for application startup.
INFO: Starting Pirate Karaoke API...
INFO: Connecting to MongoDB at mongodb+srv://...
INFO: Successfully connected to MongoDB database: pirate_karaoke
INFO: MongoDB connected and ready
INFO: Application startup complete.
```

**⚠️ KEEP THIS TERMINAL OPEN AND RUNNING TOO!**

---

## 🧪 TESTING THE APPLICATION

### Test 1: Health Check

**Open your browser and go to:**
```
http://localhost:8000
```

**Expected response:**
```json
{
  "message": "Ahoy! Welcome to Pirate Karaoke API",
  "version": "1.0.0",
  "database": "MongoDB",
  "endpoints": {
    "generate": "POST /api/generate",
    "job_status": "GET /api/jobs/{job_id}",
    "cache": "GET /api/cache/{word}"
  }
}
```

**Also test:**
```
http://localhost:8000/health
```

**Expected:**
```json
{
  "status": "healthy",
  "service": "pirate-karaoke",
  "database": "mongodb"
}
```

---

### Test 2: Generate Your First Pirate Shanty! 🏴‍☠️

**Open a 3rd terminal** or use browser tools:

#### Option A: Using curl (in terminal)

```bash
# Generate a song for the word "ship"
curl -X POST http://localhost:8000/api/generate \
  -H 'Content-Type: application/json' \
  -d '{"word": "ship"}'
```

**Response:**
```json
{
  "job_id": "abc-123-def-456",
  "status": "processing",
  "progress": 0
}
```

**Copy the `job_id` and check status:**
```bash
# Replace with your actual job_id
curl http://localhost:8000/api/jobs/abc-123-def-456
```

**Keep checking every 5-10 seconds** until you see:
```json
{
  "job_id": "abc-123-def-456",
  "status": "completed",
  "progress": 100,
  "result": {
    "word": "ship",
    "lyrics": "Verse 1:\nOn a ship we sail the sea (arr!)...",
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

#### Option B: Using Browser + Postman/Thunder Client

1. Download **Postman** or **Thunder Client** (VS Code extension)
2. Create new **POST** request
3. URL: `http://localhost:8000/api/generate`
4. Headers: `Content-Type: application/json`
5. Body (raw JSON):
   ```json
   {
     "word": "ship"
   }
   ```
6. Send request
7. Copy `job_id` from response
8. Create new **GET** request to `http://localhost:8000/api/jobs/{job_id}`
9. Keep sending until `status` is `"completed"`

---

### Test 3: Download the Generated Song

Once job is completed, open browser:

```
http://localhost:8000/outputs/song_abc123.mp3
```

Replace `song_abc123.mp3` with the actual filename from `audio_url` in the response.

**🎵 You should hear a pirate shanty!**

---

## 📊 WHAT TO WATCH

### Terminal 1 (Celery) - You'll see:
```
[INFO] Task app.tasks.generate_song_task[abc-123] received
[INFO] Generating rhymes for word: ship
[INFO] Generated 8 rhyming words
[INFO] Generating pirate lyrics with Gemini...
[INFO] Lyrics generated successfully
[INFO] Generating vocals with Edge TTS...
[INFO] Vocals generated: 25.3s
[INFO] Detecting BPM: 95.2
[INFO] Generating karaoke timings...
[INFO] Task app.tasks.generate_song_task[abc-123] succeeded
```

### Terminal 2 (FastAPI) - You'll see:
```
INFO: 127.0.0.1:12345 - "POST /api/generate HTTP/1.1" 200 OK
INFO: 127.0.0.1:12345 - "GET /api/jobs/abc-123 HTTP/1.1" 200 OK
```

---

## ❓ TROUBLESHOOTING

### Problem: "Connection refused" on port 8000

**Solution:**
```bash
# Check if FastAPI is running
ps aux | grep uvicorn

# If not, start it in Terminal 2
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Problem: Celery not processing jobs

**Solution:**
```bash
# Check if Celery is running
ps aux | grep celery

# Check if Redis is running
redis-cli ping

# Restart Redis if needed
sudo service redis-server restart

# Restart Celery in Terminal 1
celery -A app.tasks worker --loglevel=info
```

### Problem: "MongoDB connection failed"

**Solution:**
```bash
# Test connection manually
python -c "import asyncio; from motor.motor_asyncio import AsyncIOMotorClient; asyncio.run(AsyncIOMotorClient('YOUR_MONGODB_URL').admin.command('ping'))"

# Check .env has correct URL
cat .env | grep MONGODB_URL

# Verify in MongoDB Atlas:
# 1. Cluster is active
# 2. Network access allows 0.0.0.0/0
# 3. Database user exists
```

### Problem: "Gemini API error"

**Solution:**
```bash
# Check API key is set
cat .env | grep GEMINI_API_KEY

# Verify API key is valid at: https://ai.google.dev/
# Check you haven't exceeded free tier: 60 requests/minute
```

### Problem: Jobs stay at "processing" forever

**Causes:**
1. Celery worker not running (check Terminal 1)
2. Redis not running (`redis-cli ping`)
3. Error in Celery worker (check Terminal 1 logs)

**Solution:**
- Look at Terminal 1 for error messages
- Restart Celery worker (Ctrl+C, then restart)
- Check `test_setup.py` passes all tests

---

## 🛑 STOPPING THE APPLICATION

**To stop the app:**

1. **Terminal 1 (Celery):** Press `Ctrl + C`
2. **Terminal 2 (FastAPI):** Press `Ctrl + C`
3. **Redis can stay running** (or stop with `sudo service redis-server stop`)

**To restart later:**
- Just run Terminal 1 and Terminal 2 commands again!
- Redis should auto-start, or `sudo service redis-server start`

---

## 📁 PROJECT STRUCTURE

```
EmoryHack/
├── app/
│   ├── main.py              # FastAPI application (Terminal 2 runs this)
│   ├── tasks.py             # Celery tasks (Terminal 1 runs this)
│   ├── config.py            # Reads .env file
│   ├── database.py          # MongoDB connection
│   ├── models.py            # Database models (Job, SongCache)
│   └── services/
│       ├── rhyme_service.py      # Generates rhyming words
│       ├── lyrics_service.py     # Gemini AI pirate lyrics
│       ├── vocal_service.py      # Edge TTS synthesis
│       ├── audio_service.py      # Audio mixing
│       └── karaoke_service.py    # Word timing
├── beats/                   # Beat loops (optional)
├── outputs/                 # Generated MP3 files
├── temp/                    # Temporary files
├── .env                     # Your API keys and config
├── requirements.txt         # Python packages
├── test_setup.py           # Setup verification script
└── RUN_PROJECT.md          # This file!
```

---

## 🎯 QUICK START COMMANDS

**Every time you want to run the app:**

```bash
# 1. Start Redis (if not running)
sudo service redis-server start

# 2. Terminal 1 - Celery Worker
cd /mnt/c/Users/sufya/OneDrive/Desktop/EmoryHack
source venv/bin/activate
celery -A app.tasks worker --loglevel=info

# 3. Terminal 2 - FastAPI Server (new terminal window)
cd /mnt/c/Users/sufya/OneDrive/Desktop/EmoryHack
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 4. Test in browser
http://localhost:8000

# 5. Generate song
curl -X POST http://localhost:8000/api/generate -H 'Content-Type: application/json' -d '{"word": "ship"}'
```

---

## 🏴‍☠️ SAMPLE WORDS TO TEST

Try generating songs for these pirate-themed words:
- `ship` - Classic sea shanty
- `treasure` - Pirate adventure
- `ocean` - Maritime theme
- `sail` - Seafaring
- `pirate` - Meta!
- `parrot` - Pirate companion
- `map` - Treasure hunting
- `gold` - Pirate treasure
- `crew` - Teamwork
- `wave` - Ocean waves

---

## 📝 API ENDPOINTS REFERENCE

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message |
| GET | `/health` | Health check |
| POST | `/api/generate` | Generate new song |
| GET | `/api/jobs/{job_id}` | Get job status |
| GET | `/api/cache/{word}` | Get cached song |
| GET | `/outputs/{filename}` | Download audio file |

---

## 🎉 SUCCESS CRITERIA

Your app is working perfectly if:

1. ✅ `test_setup.py` passes all tests
2. ✅ Terminal 1 shows "celery@your-pc ready"
3. ✅ Terminal 2 shows "Application startup complete"
4. ✅ Browser shows welcome message at `http://localhost:8000`
5. ✅ POST to `/api/generate` returns job_id
6. ✅ GET to `/api/jobs/{job_id}` shows progress
7. ✅ Job completes and you can download MP3
8. ✅ MP3 plays pirate shanty with vocals!

---

## 👥 SHARING WITH YOUR TEAMMATE

**Your friend needs to:**
1. Clone the project code
2. Get your MongoDB Atlas connection string (share via private message)
3. Get their own Gemini API key (free from https://ai.google.dev/)
4. Follow the same setup steps
5. Use the same `.env` with shared MongoDB URL

**Both of you will:**
- ✅ Share the same MongoDB database (see each other's songs)
- ✅ Run your own Redis (local task queues)
- ✅ Run your own Celery workers (process your own jobs)
- ✅ Generate songs that get stored in shared database

---

Built with ❤️ for EmoryHack! Arr! 🏴‍☠️
