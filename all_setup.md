# 🏴‍☠️ Pirate Karaoke Backend - Windows Setup Guide

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Option A: WSL2 Setup (Recommended)](#option-a-wsl2-setup-recommended)
3. [Option B: Native Windows Setup](#option-b-native-windows-setup)
4. [MongoDB Setup for Windows](#mongodb-setup-for-windows)
5. [Redis Setup for Windows](#redis-setup-for-windows)
6. [Python Environment Setup](#python-environment-setup)
7. [Application Configuration](#application-configuration)
8. [Running the Application](#running-the-application)
9. [Testing](#testing)
10. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Downloads
- **Python 3.10+** - https://www.python.org/downloads/
- **MongoDB 6.0+** - https://www.mongodb.com/try/download/community
- **Redis** - https://github.com/microsoftarchive/redis/releases
- **Git** - https://git-scm.com/download/win
- **Visual Studio Build Tools** - https://visualstudio.microsoft.com/downloads/ (for some Python packages)

### System Requirements
- **OS**: Windows 10/11 (64-bit)
- **RAM**: 4GB minimum (8GB recommended)
- **Storage**: 10GB free space
- **Internet**: Required for Gemini API and Edge TTS

---

## Option A: WSL2 Setup (Recommended)

WSL2 provides better compatibility with Linux tools and is easier to set up.

### Step 1: Install WSL2

Open **PowerShell as Administrator** and run:

```powershell
# Enable WSL
wsl --install

# This will:
# - Enable WSL feature
# - Install Ubuntu (default)
# - Restart your computer (required)
```

**After restart**, Ubuntu will open automatically. Set up your username and password.

### Step 2: Update Ubuntu

```bash
sudo apt update && sudo apt upgrade -y
```

### Step 3: Install Dependencies in WSL2

```bash
# Install Python and system dependencies
sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    ffmpeg \
    libsndfile1 \
    rubberband-cli \
    espeak-ng \
    git

# Verify installations
python3 --version  # Should be 3.10+
ffmpeg -version
```

### Step 4: Install MongoDB in WSL2

```bash
# Import MongoDB public key
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -

# Add MongoDB repository
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list

# Update and install
sudo apt update
sudo apt install -y mongodb-org

# Create data directory
sudo mkdir -p /data/db
sudo chown -R $USER /data/db

# Start MongoDB
sudo mongod --fork --logpath /var/log/mongodb.log

# Verify
mongosh --eval "db.version()"
```

### Step 5: Install Redis in WSL2

```bash
# Install Redis
sudo apt install -y redis-server

# Start Redis
sudo service redis-server start

# Verify
redis-cli ping  # Should return "PONG"
```

### Step 6: Access Your Project Files

Your Windows files are accessible at `/mnt/c/`:

```bash
# Navigate to your project
cd /mnt/c/Users/sufya/OneDrive/Desktop/EmoryHack

# List files
ls -la
```

### Step 7: Continue to [Python Environment Setup](#python-environment-setup)

---

## Option B: Native Windows Setup

If you prefer not to use WSL2, you can run everything natively on Windows.

### Step 1: Install Python

1. Download Python 3.11 from https://www.python.org/downloads/
2. **IMPORTANT**: Check "Add Python to PATH" during installation
3. Install with default settings
4. Verify:

```cmd
python --version
pip --version
```

### Step 2: Install FFmpeg

**Method 1: Using Chocolatey (Recommended)**

1. Install Chocolatey (PowerShell as Administrator):
```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

2. Install FFmpeg:
```powershell
choco install ffmpeg
```

**Method 2: Manual Installation**

1. Download FFmpeg from https://www.gyan.dev/ffmpeg/builds/
2. Extract to `C:\ffmpeg`
3. Add to PATH:
   - Open "Environment Variables"
   - Add `C:\ffmpeg\bin` to PATH
4. Verify:
```cmd
ffmpeg -version
```

### Step 3: Install Visual Studio Build Tools

Some Python packages require C++ compilers.

1. Download from https://visualstudio.microsoft.com/downloads/
2. Select "Build Tools for Visual Studio 2022"
3. Install with "Desktop development with C++" workload
4. Restart computer after installation

---

## MongoDB Setup for Windows

### Installation

1. **Download MongoDB Community Server**
   - Go to https://www.mongodb.com/try/download/community
   - Select Windows version
   - Download MSI installer

2. **Run Installer**
   - Choose "Complete" installation
   - ✅ Check "Install MongoDB as a Service"
   - ✅ Check "Run service as Network Service user"
   - Leave data directory as default: `C:\Program Files\MongoDB\Server\6.0\data`
   - Leave log directory as default: `C:\Program Files\MongoDB\Server\6.0\log`

3. **Verify Installation**

Open **Command Prompt** and run:

```cmd
# Check if MongoDB service is running
sc query MongoDB

# Should show "STATE: 4 RUNNING"
```

4. **Test MongoDB Connection**

```cmd
# Connect to MongoDB shell
mongosh

# You should see:
# Current Mongosh Log ID: ...
# Connecting to: mongodb://127.0.0.1:27017/
# Using MongoDB: 6.0.x

# Test a command:
db.version()

# Exit
exit
```

### MongoDB Compass (Optional GUI)

1. Download from https://www.mongodb.com/try/download/compass
2. Install and connect to `mongodb://localhost:27017`
3. You can view your `pirate_karaoke` database here

### Troubleshooting MongoDB on Windows

**If MongoDB service won't start:**

```cmd
# Check logs
type "C:\Program Files\MongoDB\Server\6.0\log\mongod.log"

# Create data directory if missing
mkdir "C:\Program Files\MongoDB\Server\6.0\data"

# Start MongoDB manually
"C:\Program Files\MongoDB\Server\6.0\bin\mongod.exe" --dbpath "C:\Program Files\MongoDB\Server\6.0\data"
```

---

## Redis Setup for Windows

Redis doesn't have official Windows support, but we have options:

### Option 1: Redis for Windows (Easiest)

1. **Download Redis**
   - Go to https://github.com/microsoftarchive/redis/releases
   - Download `Redis-x64-3.0.504.msi` (latest version)

2. **Install Redis**
   - Run the MSI installer
   - ✅ Check "Add to PATH"
   - Choose default port: 6379
   - ✅ Check "Start Redis Server"

3. **Verify Redis**

```cmd
# Test Redis
redis-cli ping

# Should return: PONG
```

4. **Start Redis (if not running)**

```cmd
# Start Redis server
redis-server

# Keep this terminal open
```

### Option 2: Docker Desktop (Alternative)

1. **Install Docker Desktop**
   - Download from https://www.docker.com/products/docker-desktop
   - Install and restart

2. **Run Redis in Docker**

```cmd
# Pull and run Redis
docker run -d -p 6379:6379 --name redis redis:7

# Verify
docker ps
redis-cli ping
```

### Option 3: Memurai (Redis Alternative for Windows)

1. Download from https://www.memurai.com/get-memurai
2. Install as Windows Service
3. Works exactly like Redis

---

## Python Environment Setup

### Navigate to Project Directory

Open **Command Prompt** or **PowerShell**:

```cmd
# Navigate to your project
cd C:\Users\sufya\OneDrive\Desktop\EmoryHack

# Or if using PowerShell:
cd ~\OneDrive\Desktop\EmoryHack
```

### Create Virtual Environment

```cmd
# Create virtual environment
python -m venv venv

# Activate virtual environment
# For Command Prompt:
venv\Scripts\activate

# For PowerShell:
venv\Scripts\Activate.ps1
```

**If PowerShell gives execution policy error:**

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Install Python Dependencies

```cmd
# Upgrade pip
python -m pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt
```

**Common Installation Issues:**

If `aeneas` fails to install:

```cmd
# Install pre-built wheel
pip install aeneas --use-pep517

# Or skip aeneas for now (karaoke timing won't work)
# Edit requirements.txt and comment out aeneas
```

### Download NLTK Data

```cmd
python -c "import nltk; nltk.download('cmudict')"
```

---

## Application Configuration

### 1. Create .env File

```cmd
# Copy example file
copy .env.example .env

# Open in Notepad
notepad .env
```

### 2. Configure Environment Variables

Edit `.env` with these settings:

```env
# ===== Gemini API (REQUIRED) =====
GEMINI_API_KEY=your_gemini_api_key_here
# Get free key at: https://ai.google.dev/

# ===== Redis =====
REDIS_URL=redis://localhost:6379/0

# ===== MongoDB =====
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=pirate_karaoke

# ===== Application Settings =====
SAMPLE_RATE=24000
MAX_CONCURRENT_JOBS=3
CACHE_EXPIRY_DAYS=7

# ===== Directories (Windows paths) =====
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

### 3. Get Gemini API Key (FREE)

1. Go to https://ai.google.dev/
2. Click "Get API key in Google AI Studio"
3. Sign in with Google account
4. Click "Create API Key"
5. Copy and paste into `.env` file

### 4. Create Beat Directory

```cmd
# Create directory structure
mkdir beats\pirate-shanty
mkdir outputs
mkdir temp
```

### 5. Download Pirate Beats (Optional)

Download free pirate-themed beats from:
- https://www.looperman.com (search "sea shanty" or "pirate")
- https://www.youtube.com/audiolibrary
- https://incompetech.com

Save WAV files to `beats\pirate-shanty\`

### 6. Initialize Beat Library

```cmd
python -c "from app.services.beat_manager import BeatLibraryManager; BeatLibraryManager().scan_beats_directory()"
```

---

## Running the Application

You need **3 separate Command Prompt windows**:

### Terminal 1: Verify Services

```cmd
# Check MongoDB
mongosh --eval "db.version()"

# Check Redis
redis-cli ping

# If either isn't running, start them:
# MongoDB is usually auto-started as a service
# For Redis:
redis-server
```

### Terminal 2: Start Celery Worker

```cmd
# Navigate to project
cd C:\Users\sufya\OneDrive\Desktop\EmoryHack

# Activate virtual environment
venv\Scripts\activate

# Start Celery worker
celery -A app.tasks worker --loglevel=info --pool=solo

# Note: --pool=solo is required for Windows
```

**You should see:**
```
 -------------- celery@YOUR-PC v5.3.4
---- **** -----
--- * ***  * -- Windows-10.0.19045
-- * - **** ---
- ** ---------- [config]
- ** ---------- .> app:         pirate_karaoke
- ** ---------- .> transport:   redis://localhost:6379/0
- ** ---------- .> results:     redis://localhost:6379/0
- *** --- * --- .> concurrency: 1 (solo)
-- ******* ----
--- ***** -----

[tasks]
  . app.tasks.cleanup_old_files
  . app.tasks.generate_song_task

[2024-11-15 01:00:00,000: INFO/MainProcess] Connected to redis://localhost:6379/0
[2024-11-15 01:00:00,000: INFO/MainProcess] celery@YOUR-PC ready.
```

### Terminal 3: Start FastAPI Server

```cmd
# Navigate to project
cd C:\Users\sufya\OneDrive\Desktop\EmoryHack

# Activate virtual environment
venv\Scripts\activate

# Start FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**You should see:**
```
INFO:     Will watch for changes in these directories: ['C:\\Users\\sufya\\OneDrive\\Desktop\\EmoryHack']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Starting Pirate Karaoke API...
INFO:     Connecting to MongoDB at mongodb://localhost:27017
INFO:     Successfully connected to MongoDB database: pirate_karaoke
INFO:     MongoDB connected and ready
INFO:     Application startup complete.
```

---

## Testing

### 1. Open Browser

Navigate to: http://localhost:8000

You should see:
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

### 2. Test Health Endpoint

http://localhost:8000/health

```json
{
  "status": "healthy",
  "service": "pirate-karaoke",
  "database": "mongodb"
}
```

### 3. Generate a Pirate Shanty

**Using PowerShell:**

```powershell
# Generate song for word "ship"
$body = @{
    word = "ship"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/generate" -Method Post -Body $body -ContentType "application/json"
```

**Using curl (if installed):**

```cmd
curl -X POST http://localhost:8000/api/generate -H "Content-Type: application/json" -d "{\"word\": \"ship\"}"
```

**Using Postman (Recommended for Windows):**

1. Download Postman: https://www.postman.com/downloads/
2. Create new POST request
3. URL: `http://localhost:8000/api/generate`
4. Headers: `Content-Type: application/json`
5. Body (raw JSON):
```json
{
  "word": "ship"
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

### 4. Poll Job Status

```powershell
# Replace JOB_ID with the ID from step 3
Invoke-RestMethod -Uri "http://localhost:8000/api/jobs/abc-123-def-456"
```

**Keep polling every few seconds until status is "completed"**

### 5. Download Generated Song

Open browser: `http://localhost:8000/outputs/song_xxxxx.mp3`

Or use PowerShell:
```powershell
Invoke-WebRequest -Uri "http://localhost:8000/outputs/song_xxxxx.mp3" -OutFile "shanty.mp3"
```

---

## Troubleshooting

### MongoDB Connection Error

**Error:**
```
pymongo.errors.ServerSelectionTimeoutError: localhost:27017
```

**Fix:**

```cmd
# Check if MongoDB service is running
sc query MongoDB

# If not running, start it
net start MongoDB

# Or start manually
"C:\Program Files\MongoDB\Server\6.0\bin\mongod.exe"

# Check Windows Services
services.msc
# Find "MongoDB Server" and start it
```

### Redis Connection Error

**Error:**
```
redis.exceptions.ConnectionError: Error connecting to Redis
```

**Fix:**

```cmd
# Start Redis server
redis-server

# Or if using Docker
docker start redis

# Check if Redis is listening
netstat -an | findstr 6379
```

### Celery Pool Error on Windows

**Error:**
```
ValueError: not enough values to unpack (expected 3, got 0)
```

**Fix:**

Always use `--pool=solo` on Windows:

```cmd
celery -A app.tasks worker --loglevel=info --pool=solo
```

### Aeneas Installation Fails

**Error:**
```
ERROR: Failed building wheel for aeneas
```

**Fix:**

Aeneas is difficult on Windows. You have two options:

**Option 1: Skip aeneas (karaoke timing won't work perfectly)**

Edit `requirements.txt`:
```
# aeneas==1.7.3  # Comment this out
```

Then the app uses fallback timing (evenly distributed words).

**Option 2: Use WSL2** (recommended for aeneas)

### ModuleNotFoundError

**Error:**
```
ModuleNotFoundError: No module named 'xxx'
```

**Fix:**

```cmd
# Make sure virtual environment is activated
venv\Scripts\activate

# Reinstall requirements
pip install -r requirements.txt
```

### Port Already in Use

**Error:**
```
ERROR: [Errno 10048] error while attempting to bind on address ('0.0.0.0', 8000)
```

**Fix:**

```cmd
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID)
taskkill /F /PID <PID>

# Or use different port
uvicorn app.main:app --port 8001
```

### Permission Denied Errors

**Fix:**

Run Command Prompt or PowerShell **as Administrator**:
1. Right-click Command Prompt
2. Select "Run as administrator"

---

## Production Deployment

### Option 1: Use WSL2 + Docker

1. Set up WSL2 (see Option A above)
2. Install Docker Desktop for Windows
3. Use docker-compose.yml:

```yaml
version: '3.8'

services:
  mongodb:
    image: mongo:6.0
    ports:
      - "27017:27017"
    volumes:
      - mongo-data:/data/db

  redis:
    image: redis:7
    ports:
      - "6379:6379"

  web:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - mongodb
      - redis

  worker:
    build: .
    command: celery -A app.tasks worker --loglevel=info
    depends_on:
      - mongodb
      - redis

volumes:
  mongo-data:
```

Run:
```cmd
docker-compose up -d
```

### Option 2: Cloud Deployment

Use free cloud services:
- **MongoDB**: MongoDB Atlas (free M0 cluster)
- **Redis**: Redis Cloud (30MB free)
- **Hosting**: Railway.app or Render.com

Update `.env`:
```env
MONGODB_URL=mongodb+srv://user:pass@cluster.mongodb.net/
REDIS_URL=redis://default:pass@redis-xxxxx.cloud.redislabs.com:12345
```

---

## Windows-Specific Tips

### 1. Use PowerShell ISE for Better Terminal

PowerShell ISE provides better formatting and error messages.

### 2. Windows Defender Exclusions

Add your project folder to Windows Defender exclusions for better performance:

1. Open Windows Security
2. Virus & threat protection
3. Manage settings
4. Add exclusion
5. Add folder: `C:\Users\sufya\OneDrive\Desktop\EmoryHack`

### 3. Auto-Start Services on Boot

**MongoDB:**
- Already configured as Windows Service (auto-starts)

**Redis:**
```cmd
# Install as Windows service (if using Redis for Windows)
redis-server --service-install
redis-server --service-start
```

### 4. Batch Scripts for Easy Starting

Create `start_app.bat`:

```batch
@echo off
echo Starting Pirate Karaoke Backend...

REM Start Redis (if not running as service)
start "Redis" cmd /k redis-server

REM Wait 2 seconds
timeout /t 2

REM Start Celery Worker
start "Celery" cmd /k "cd /d %~dp0 && venv\Scripts\activate && celery -A app.tasks worker --loglevel=info --pool=solo"

REM Wait 2 seconds
timeout /t 2

REM Start FastAPI Server
start "FastAPI" cmd /k "cd /d %~dp0 && venv\Scripts\activate && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

echo All services started!
echo.
echo MongoDB: http://localhost:27017
echo Redis: http://localhost:6379
echo FastAPI: http://localhost:8000
echo.
pause
```

Double-click `start_app.bat` to start everything!

---

## 🎉 Success!

If you've completed all steps, you should now have:

✅ MongoDB running on Windows
✅ Redis running on Windows
✅ Python virtual environment activated
✅ Celery worker processing tasks
✅ FastAPI server responding to requests
✅ Pirate shanties being generated!

### Next Steps

1. Test with various words: "ship", "treasure", "sail", "ocean"
2. Add more pirate-themed beats to `beats\pirate-shanty\`
3. Build a frontend (React recommended)
4. Deploy to cloud (MongoDB Atlas + Railway)

---

## 📚 Windows-Specific Resources

- [Python on Windows](https://docs.python.org/3/using/windows.html)
- [MongoDB on Windows](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-windows/)
- [Redis on Windows](https://redis.io/docs/getting-started/installation/install-redis-on-windows/)
- [WSL2 Documentation](https://docs.microsoft.com/en-us/windows/wsl/)

---

## 🏴‍☠️ Arr! Happy Shanty Making on Windows! 🏴‍☠️

Built with ❤️ for Windows pirates everywhere!
