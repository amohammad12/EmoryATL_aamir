#!/bin/bash

echo "========================================="
echo "  Pirate Karaoke Backend Setup Script"
echo "  (MongoDB + Redis + Bark TTS)"
echo "========================================="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.10+ first."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip first."
    exit 1
fi

echo "✅ pip3 found"

# 1. Install system dependencies
echo ""
echo "📦 Step 1: Installing system dependencies..."
echo "   (You may need to enter your password for sudo)"

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    sudo apt-get update
    sudo apt-get install -y ffmpeg libsndfile1 rubberband-cli espeak-ng
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    if command -v brew &> /dev/null; then
        brew install ffmpeg libsndfile rubberband espeak-ng
    else
        echo "⚠️  Homebrew not found. Please install ffmpeg, libsndfile, rubberband, and espeak-ng manually."
    fi
else
    echo "⚠️  Unknown OS. Please install ffmpeg, libsndfile, rubberband, and espeak-ng manually."
fi

echo "✅ System dependencies installed"

# 2. Create virtual environment (optional but recommended)
echo ""
echo "🐍 Step 2: Creating virtual environment..."

if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
source venv/bin/activate
echo "✅ Virtual environment activated"

# 3. Install Python dependencies
echo ""
echo "📚 Step 3: Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Python packages installed"

# 4. Download NLTK data
echo ""
echo "📖 Step 4: Downloading NLTK data..."
python3 -c "import nltk; nltk.download('cmudict')"

echo "✅ NLTK data downloaded"

# 5. Create .env file if it doesn't exist
echo ""
echo "⚙️  Step 5: Setting up environment configuration..."

if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✅ Created .env file from .env.example"
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env and configure:"
    echo "   1. GEMINI_API_KEY=your_key_here (get free at https://ai.google.dev/)"
    echo "   2. MONGODB_URL=mongodb://localhost:27017 (or your MongoDB connection string)"
else
    echo "✅ .env file already exists"
fi

# 6. Initialize beat library
echo ""
echo "🎵 Step 6: Initializing beat library..."

python3 -c "from app.services.beat_manager import BeatLibraryManager; BeatLibraryManager().scan_beats_directory()"

echo "✅ Beat library initialized"

# Done!
echo ""
echo "========================================="
echo "  ✅ Setup Complete!"
echo "========================================="
echo ""
echo "📋 IMPORTANT: Before running the app, you need:"
echo ""
echo "1️⃣  MongoDB running locally:"
echo "   - Install MongoDB: https://www.mongodb.com/docs/manual/installation/"
echo "   - Start MongoDB:"
echo "     Linux: sudo systemctl start mongod"
echo "     macOS: brew services start mongodb-community"
echo "     Windows: net start MongoDB"
echo ""
echo "2️⃣  Redis running locally:"
echo "   - Install Redis: https://redis.io/download"
echo "   - Start Redis:"
echo "     Linux/macOS: redis-server"
echo "     Windows: Download from https://github.com/microsoftarchive/redis/releases"
echo ""
echo "3️⃣  Add your Gemini API key to .env file"
echo "   - Get free key at: https://ai.google.dev/"
echo "   - Edit .env and set: GEMINI_API_KEY=your_key_here"
echo ""
echo "4️⃣  Add pirate-themed beat files to beats/pirate-shanty/ directory"
echo "   - Free beats at: Looperman.com, YouTube Audio Library, Incompetech"
echo ""
echo "========================================="
echo "  🚀 RUNNING THE APPLICATION"
echo "========================================="
echo ""
echo "Terminal 1 - Start Celery worker:"
echo "  source venv/bin/activate"
echo "  celery -A app.tasks worker --loglevel=info"
echo ""
echo "Terminal 2 - Start FastAPI server:"
echo "  source venv/bin/activate"
echo "  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "Terminal 3 - Test the API:"
echo "  curl -X POST http://localhost:8000/api/generate \\"
echo "    -H 'Content-Type: application/json' \\"
echo "    -d '{\"word\": \"ship\"}'"
echo ""
echo "🏴‍☠️ Arr! Ye be ready to make pirate shanties! 🏴‍☠️"
echo ""
