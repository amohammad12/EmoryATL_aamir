#!/bin/bash
# Pre-flight checklist before running Pirate Karaoke

echo "🏴‍☠️ PIRATE KARAOKE - PRE-FLIGHT CHECKLIST"
echo "=========================================="
echo ""

ERRORS=0

# Check 1: Redis
echo "1️⃣ Checking Redis..."
if redis-cli ping > /dev/null 2>&1; then
    echo "   ✅ Redis is running"
else
    echo "   ❌ Redis is NOT running"
    echo "      Fix: sudo service redis-server start"
    ERRORS=$((ERRORS + 1))
fi

# Check 2: Virtual environment
echo ""
echo "2️⃣ Checking virtual environment..."
if [ -f "venv/bin/activate" ]; then
    echo "   ✅ Virtual environment exists"
else
    echo "   ❌ Virtual environment NOT found"
    echo "      Fix: python3 -m venv venv"
    ERRORS=$((ERRORS + 1))
fi

# Check 3: .env file
echo ""
echo "3️⃣ Checking .env configuration..."
if [ -f ".env" ]; then
    echo "   ✅ .env file exists"

    # Check Gemini API key
    if grep -q "GEMINI_API_KEY=AIza" .env; then
        echo "   ✅ Gemini API key configured"
    else
        echo "   ❌ Gemini API key missing or incorrect"
        echo "      Fix: Add your Gemini API key to .env"
        ERRORS=$((ERRORS + 1))
    fi

    # Check MongoDB URL
    if grep -q "MONGODB_URL=mongodb+srv://" .env; then
        echo "   ✅ MongoDB Atlas URL configured"
    else
        echo "   ❌ MongoDB URL missing or incorrect"
        echo "      Fix: Add your MongoDB Atlas URL to .env"
        ERRORS=$((ERRORS + 1))
    fi

    # Check Redis URL
    if grep -q "REDIS_URL=redis://" .env; then
        echo "   ✅ Redis URL configured"
    else
        echo "   ❌ Redis URL missing"
        ERRORS=$((ERRORS + 1))
    fi
else
    echo "   ❌ .env file NOT found"
    echo "      Fix: cp .env.example .env and configure it"
    ERRORS=$((ERRORS + 1))
fi

# Check 4: FFmpeg
echo ""
echo "4️⃣ Checking FFmpeg..."
if command -v ffmpeg > /dev/null 2>&1; then
    echo "   ✅ FFmpeg installed"
else
    echo "   ❌ FFmpeg NOT installed"
    echo "      Fix: sudo apt install -y ffmpeg"
    ERRORS=$((ERRORS + 1))
fi

# Check 5: Directories
echo ""
echo "5️⃣ Checking project directories..."
if [ -d "beats" ] && [ -d "outputs" ] && [ -d "temp" ]; then
    echo "   ✅ All directories exist (beats/, outputs/, temp/)"
else
    echo "   ⚠️  Some directories missing (will be created automatically)"
fi

# Check 6: Python packages (in venv)
echo ""
echo "6️⃣ Checking Python packages..."
source venv/bin/activate 2>/dev/null
if python -c "import fastapi, beanie, celery, edge_tts, librosa" 2>/dev/null; then
    echo "   ✅ Critical Python packages installed"
else
    echo "   ❌ Some Python packages missing"
    echo "      Fix: source venv/bin/activate && pip install -r requirements.txt"
    ERRORS=$((ERRORS + 1))
fi

# Summary
echo ""
echo "=========================================="
if [ $ERRORS -eq 0 ]; then
    echo "✅ ALL CHECKS PASSED!"
    echo ""
    echo "🚀 You're ready to run the application!"
    echo ""
    echo "Next steps:"
    echo "1. Terminal 1: celery -A app.tasks worker --loglevel=info"
    echo "2. Terminal 2: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
    echo "3. Browser: http://localhost:8000"
    exit 0
else
    echo "❌ FOUND $ERRORS ISSUE(S)"
    echo ""
    echo "⚠️  Fix the issues above before running the app!"
    echo ""
    echo "Then run: python test_setup.py"
    exit 1
fi
