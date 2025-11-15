STEP 1: Install FFmpeg & System Dependencies

● FFmpeg is needed for audio mixing. Install it:

  # Update package list
  sudo apt update

  # Install FFmpeg and audio libraries
  sudo apt install -y ffmpeg libsndfile1 libsndfile1-dev rubberband-cli espeak-ng

  Verify installation:
  ffmpeg -version

  Expected output:
  ffmpeg version 4.x.x

  ---
  STEP 2: Download NLTK Data

● Download pronunciation dictionary for rhyme generation:

  # Make sure venv is activated
  source venv/bin/activate

  # Download NLTK data
  python -c "import nltk; nltk.download('cmudict')"

  Expected output:
  [nltk_data] Downloading package cmudict to /home/user/nltk_data...
  [nltk_data] Unzipping corpora/cmudict.zip.
  True

  ---
  STEP 3: Get Gemini API Key (CRITICAL!)

● Gemini API generates the pirate lyrics. 100% FREE!

  Get your free API key:

  1. Go to: https://ai.google.dev/
  2. Click: "Get API key in Google AI Studio"
  3. Sign in with your Google account
  4. Click: "Create API Key"
  5. Copy the API key (starts with AIza...)

  Add to .env file:

  # Edit .env
  nano .env

  Find this line:
  GEMINI_API_KEY=your_gemini_api_key_here

  Replace with your actual key:
  GEMINI_API_KEY=AIzaSyDxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

  Save and exit (Ctrl+X, Y, Enter)

  Verify it's set:

  cat .env | grep GEMINI_API_KEY

  Should show your API key (not "your_gemini_api_key_here")

  ---
  STEP 4: Verify Complete .env Configuration

  Check your entire .env file:

  cat .env

  Should contain:
  # Gemini API (REQUIRED)
  GEMINI_API_KEY=AIzaSyDxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

  # Redis
  REDIS_URL=redis://localhost:6379/0

  # MongoDB Atlas
  MONGODB_URL=mongodb+srv://pirate_user:password@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
  MONGODB_DB_NAME=pirate_karaoke

  # Application Settings
  SAMPLE_RATE=24000
  MAX_CONCURRENT_JOBS=3
  CACHE_EXPIRY_DAYS=7

  # Directories
  BEATS_DIR=beats
  OUTPUT_DIR=outputs
  TEMP_DIR=temp

  # Audio Settings
  VOCALS_VOLUME=1.0
  INSTRUMENTAL_VOLUME=0.4
  PIRATE_SHANTY_BPM_MIN=90
  PIRATE_SHANTY_BPM_MAX=110

  # Edge TTS Settings
  TTS_VOICE=en-US-JennyNeural
  TTS_RATE=-10%
  TTS_PITCH=+5Hz

  # Development
  DEBUG=True

  ---
  STEP 5: Test Complete Setup

● Write(test_setup.py)
  ⎿  Wrote 140 lines to test_setup.py
     """
     Test complete application setup
     """
     import asyncio
     import sys
     async def test_complete_setup():
         print("🏴‍☠️ PIRATE KARAOKE - SETUP VERIFICATION")
         print("=" * 50)
     … +130 lines (ctrl+o to expand)

● Run the complete setup test:

  # Make sure venv is activated
  source venv/bin/activate

  # Run comprehensive test
  python test_setup.py

  This will check:
  - ✅ All environment variables configured
  - ✅ All Python packages installed
  - ✅ NLTK data downloaded
  - ✅ FFmpeg installed
  - ✅ Redis connection working
  - ✅ MongoDB Atlas connection working
  - ✅ Directories exist
  - ✅ App can initialize

  ---
  STEP 6: Start the Application!

● Once all tests pass, start the app with 2 terminals:

  Terminal 1: Start Celery Worker

  cd /mnt/c/Users/sufya/OneDrive/Desktop/EmoryHack
  source venv/bin/activate
  celery -A app.tasks worker --loglevel=info

  You should see:
   -------------- celery@your-pc v5.5.3
  ---- **** -----
  [config]
  .> app:         pirate_karaoke
  .> transport:   redis://localhost:6379/0
  .> results:     redis://localhost:6379/0

  [tasks]
    . app.tasks.cleanup_old_files
    . app.tasks.generate_song_task

  [INFO] Connected to redis://localhost:6379/0
  [INFO] celery@your-pc ready.

  ✅ Leave this running!

  Terminal 2: Start FastAPI Server

  Open a new WSL terminal (type wsl in new PowerShell window), then:

  cd /mnt/c/Users/sufya/OneDrive/Desktop/EmoryHack
  source venv/bin/activate
  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

  You should see:
  INFO: Will watch for changes in these directories: ['/mnt/c/Users/sufya/OneDrive/Desktop/EmoryHack']
  INFO: Uvicorn running on http://0.0.0.0:8000
  INFO: Started server process
  INFO: Waiting for application startup.
  INFO: Starting Pirate Karaoke API...
  INFO: Connecting to MongoDB at mongodb+srv://...
  INFO: Successfully connected to MongoDB database: pirate_karaoke
  INFO: Application startup complete.

  ✅ Leave this running too!

  ---
  STEP 7: Test Your First Pirate Shanty! 🏴‍☠️

  Option 1: Browser

  Open your browser and go to:
  http://localhost:8000

  You should see:
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

  Option 2: Test with curl (in a 3rd terminal)

  # Generate a pirate shanty for the word "ship"
  curl -X POST http://localhost:8000/api/generate \
    -H 'Content-Type: application/json' \
    -d '{"word": "ship"}'

  You'll get a job ID:
  {
    "job_id": "abc-123-def-456",
    "status": "processing",
    "progress": 0
  }

  Check the status:
  curl http://localhost:8000/api/jobs/abc-123-def-456

  Keep checking every few seconds until status is "completed"!

  ---
  📋 COMPLETE CHECKLIST

  Before running the app, verify:

  # 1. Check all commands work
  redis-cli ping                    # Should return: PONG
  ffmpeg -version                   # Should show version
  mongosh --version                 # Should show version

  # 2. Verify .env has all keys
  cat .env | grep -E "GEMINI_API_KEY|MONGODB_URL|REDIS_URL"

  # 3. Test setup
  python test_setup.py              # Should pass all tests

  # 4. Verify venv is activated
  which python                      # Should point to venv/bin/python

  ---
  🎯 QUICK START COMMANDS

  Save these for easy restart:

  # In WSL Terminal 1 - Start Redis
  sudo service redis-server start

  # In WSL Terminal 2 - Start Celery
  cd /mnt/c/Users/sufya/OneDrive/Desktop/EmoryHack
  source venv/bin/activate
  celery -A app.tasks worker --loglevel=info

  # In WSL Terminal 3 - Start FastAPI
  cd /mnt/c/Users/sufya/OneDrive/Desktop/EmoryHack
  source venv/bin/activate
  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

  ---
  Run the commands step by step and let me know if you hit any issues! Once test_setup.py passes all tests, you're ready to generate pirate shanties! 🏴‍☠️⚓    