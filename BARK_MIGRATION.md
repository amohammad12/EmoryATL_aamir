# 🎵 Bark TTS Migration Guide

This guide explains the migration from Microsoft Edge TTS to Bark (Suno) for expressive singing vocals in the Pirate Sea Shanty Karaoke Backend.

## 🎯 What Changed?

### Overview
We've replaced **Microsoft Edge TTS** (cloud-based speech synthesis) with **Bark by Suno** (local AI model with singing capabilities) to create actual singing pirate shanties instead of spoken vocals.

### Key Improvements
- ✨ **Actual Singing**: Bark can produce musical vocalizations and singing
- 🎭 **Expressiveness**: Much more natural prosody and emotion
- 🎵 **Musical Notation**: Support for musical symbols and singing cues
- 🎤 **Voice Variety**: Multiple voice presets to choose from
- 🆓 **Still Free**: Open-source model (but requires GPU)

---

## 📋 Files Modified

### Core Implementation
1. **`requirements.txt`** - Replaced `edge-tts` with Bark dependencies
2. **`app/services/vocal_service.py`** - Complete rewrite with `BarkVocalGenerator`
3. **`app/config.py`** - Updated TTS configuration settings
4. **`.env.example`** - New Bark environment variables

### Documentation & Scripts
5. **`README.md`** - Updated features and architecture
6. **`app/tasks.py`** - Updated comment
7. **`setup.sh`** - Updated description
8. **`preflight_check.sh`** - Updated package check

---

## 🔧 Technical Changes

### Dependency Changes

**Removed:**
```
edge-tts==6.1.9
```

**Added:**
```
transformers>=4.31.0
accelerate>=0.20.0
torch>=2.0.0
optimum>=1.12.0
```

### Configuration Changes

**Before (Edge TTS):**
```python
TTS_VOICE: str = "en-US-JennyNeural"
TTS_RATE: str = "-10%"
TTS_PITCH: str = "+5Hz"
```

**After (Bark TTS):**
```python
BARK_MODEL: str = "suno/bark"
BARK_VOICE_PRESET: str = "v2/en_speaker_6"
BARK_TEMPERATURE: float = 0.7
BARK_USE_GPU: bool = True
BARK_SINGING_MODE: bool = True
BARK_SEMANTIC_TEMP: float = 0.8
BARK_COARSE_TEMP: float = 0.7
BARK_FINE_TEMP: float = 0.5
```

### Code Architecture Changes

**New Components:**
1. **`BarkModelCache`** - Singleton pattern to cache the model and avoid reloading
2. **GPU Support** - Automatic CUDA detection and FP16 optimization
3. **Singing Mode** - Special prompt formatting with musical notation (♪)
4. **Audio Conversion** - NumPy → WAV → MP3 pipeline

**VocalGenerator Methods:**
- `__init__()` - Now loads Bark model from cache
- `generate_vocals_async()` - Wraps sync generation in thread pool
- `_generate_vocals_sync()` - Core Bark inference method
- `_format_for_singing()` - **NEW** - Adds musical notation for singing
- `_add_shanty_rhythm()` - Enhanced for Bark compatibility

---

## 🚀 Installation & Setup

### Prerequisites

1. **GPU Required** (highly recommended):
   - NVIDIA GPU with CUDA support
   - At least 4GB VRAM
   - CUDA 11.8+ and cuDNN installed

2. **Disk Space**:
   - ~2-3GB for Bark model download

### Step 1: Update Dependencies

```bash
# Activate your virtual environment
source venv/bin/activate

# Install new requirements
pip install -r requirements.txt

# Verify installation
python -c "import transformers, torch; print('Bark dependencies installed!')"
```

### Step 2: Verify GPU Access

```bash
# Check CUDA availability
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"
python -c "import torch; print(f'GPU name: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"None\"}')"
```

**Expected Output:**
```
CUDA available: True
GPU name: NVIDIA GeForce RTX 3090 (or your GPU model)
```

### Step 3: Update Environment Variables

```bash
# Copy the new .env.example if you haven't customized your .env
cp .env.example .env

# Or manually update your existing .env with these new settings:
cat >> .env << 'EOF'

# Bark TTS Settings
BARK_MODEL=suno/bark
BARK_VOICE_PRESET=v2/en_speaker_6
BARK_TEMPERATURE=0.7
BARK_USE_GPU=True
BARK_SINGING_MODE=True
BARK_SEMANTIC_TEMP=0.8
BARK_COARSE_TEMP=0.7
BARK_FINE_TEMP=0.5
EOF
```

### Step 4: Test Bark Installation

Create a test script to verify Bark is working:

```bash
cat > test_bark.py << 'EOF'
#!/usr/bin/env python3
"""Test Bark TTS installation"""

import torch
from transformers import AutoProcessor, BarkModel

print("🎵 Testing Bark TTS Installation...")
print(f"✓ PyTorch version: {torch.__version__}")
print(f"✓ CUDA available: {torch.cuda.is_available()}")

if torch.cuda.is_available():
    print(f"✓ GPU: {torch.cuda.get_device_name(0)}")

print("\n📥 Loading Bark model (this will download ~2-3GB on first run)...")
processor = AutoProcessor.from_pretrained("suno/bark")
model = BarkModel.from_pretrained(
    "suno/bark",
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
)

if torch.cuda.is_available():
    model = model.to("cuda")
    print("✓ Model loaded on GPU")
else:
    print("⚠ Model loaded on CPU (will be slower)")

print("\n🎤 Generating test audio...")
inputs = processor("♪ Yo-ho-ho and a bottle of rum! ♪", voice_preset="v2/en_speaker_6")

if torch.cuda.is_available():
    inputs = {k: v.to("cuda") for k, v in inputs.items()}

with torch.no_grad():
    audio = model.generate(**inputs)

print("✅ Success! Bark is working correctly.")
print("\nYou can now run the full application.")
EOF

chmod +x test_bark.py
python test_bark.py
```

### Step 5: Start the Application

```bash
# Terminal 1: Start MongoDB
sudo systemctl start mongod  # Linux
# or
brew services start mongodb-community  # macOS

# Terminal 2: Start Redis
redis-server

# Terminal 3: Start Celery Worker
source venv/bin/activate
celery -A app.tasks worker --loglevel=info

# Terminal 4: Start FastAPI Server
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 6: Test Full Pipeline

```bash
# Generate a pirate shanty
curl -X POST http://localhost:8000/api/generate \
  -H 'Content-Type: application/json' \
  -d '{"word": "treasure"}'

# Save the job_id from response, then check status
curl http://localhost:8000/api/jobs/YOUR_JOB_ID

# Listen to the generated singing shanty!
# Download from: http://localhost:8000/outputs/song_xxxxx.mp3
```

---

## 🎛️ Configuration Options

### Voice Presets

Bark supports multiple voice presets. Test different ones to find the best for kids:

```python
# Kid-friendly voices (female):
BARK_VOICE_PRESET=v2/en_speaker_6  # Default - young female, clear
BARK_VOICE_PRESET=v2/en_speaker_9  # Alternative female voice

# Other voices:
BARK_VOICE_PRESET=v2/en_speaker_0  # Male voice
BARK_VOICE_PRESET=v2/en_speaker_1  # Male voice 2
# ... up to v2/en_speaker_9
```

### Temperature Settings

Control expressiveness vs. consistency:

```python
# More consistent (robotic):
BARK_SEMANTIC_TEMP=0.5
BARK_COARSE_TEMP=0.5
BARK_FINE_TEMP=0.3

# More expressive (varied):
BARK_SEMANTIC_TEMP=0.9
BARK_COARSE_TEMP=0.8
BARK_FINE_TEMP=0.7

# Recommended (balanced):
BARK_SEMANTIC_TEMP=0.8  # Current default
BARK_COARSE_TEMP=0.7    # Current default
BARK_FINE_TEMP=0.5      # Current default
```

### Singing Mode

Toggle between speaking and singing:

```python
# Singing mode (adds ♪ symbols and [singing] context)
BARK_SINGING_MODE=True   # Default

# Speaking mode (more natural speech)
BARK_SINGING_MODE=False
```

---

## ⚡ Performance Optimization

### Generation Speed

**GPU (Recommended):**
- First generation: 15-30 seconds (model loading)
- Subsequent generations: 5-15 seconds
- Model stays cached in memory

**CPU (Fallback):**
- First generation: 60-120 seconds
- Subsequent generations: 30-60 seconds
- Not recommended for production

### GPU Memory Optimization

If you encounter GPU memory issues:

```python
# In config.py or .env:
BARK_USE_GPU=True

# The code automatically uses FP16 (half precision) when GPU is enabled
# This reduces memory usage by ~50%
```

### Model Caching

The `BarkModelCache` singleton ensures the model is loaded only once:
- First request loads the model (~10-20 seconds)
- All subsequent requests reuse the cached model
- Restart Celery worker to reload the model

---

## 🐛 Troubleshooting

### Issue: "CUDA out of memory"

**Solution 1:** Close other GPU applications
```bash
nvidia-smi  # Check GPU usage
# Kill processes using GPU
```

**Solution 2:** Reduce batch size (already set to 1 in our implementation)

**Solution 3:** Use CPU mode temporarily
```python
BARK_USE_GPU=False
```

### Issue: "Model loading is too slow"

**Cause:** First-time download (2-3GB)

**Solution:** Pre-download the model:
```bash
python -c "from transformers import BarkModel; BarkModel.from_pretrained('suno/bark')"
```

### Issue: "Audio quality is poor"

**Solution:** Adjust temperature settings:
```python
# For clearer, more consistent audio:
BARK_SEMANTIC_TEMP=0.6
BARK_COARSE_TEMP=0.6
BARK_FINE_TEMP=0.4
```

### Issue: "Vocals don't sound like singing"

**Solution:** Verify singing mode is enabled and check lyrics formatting:
```python
BARK_SINGING_MODE=True

# Manually test with this format:
test_lyrics = "[singing a pirate sea shanty]\n♪ Yo-ho-ho! ♪"
```

---

## 📊 Edge TTS vs Bark Comparison

| Feature | Edge TTS (Old) | Bark TTS (New) |
|---------|----------------|----------------|
| **Singing Capability** | ❌ No | ✅ Yes |
| **Expressiveness** | ⭐⭐ Basic | ⭐⭐⭐⭐⭐ Excellent |
| **Voice Quality** | ⭐⭐⭐ Good | ⭐⭐⭐⭐ Great |
| **Setup Complexity** | ⭐ Very Easy | ⭐⭐⭐ Moderate |
| **Generation Speed** | ⭐⭐⭐⭐⭐ Instant | ⭐⭐⭐ Fast (with GPU) |
| **GPU Required** | ❌ No | ✅ Yes (recommended) |
| **Disk Space** | ~0MB | ~3GB |
| **Internet Required** | ✅ Yes | ❌ No (after download) |
| **Cost** | Free | Free (open-source) |
| **Best For** | Quick speech | Musical/expressive content |

---

## 🎯 Next Steps

### 1. Voice Preset Testing

Test all voice presets to find the best for kids:

```bash
# Create a test script
cat > test_voices.py << 'EOF'
from app.services.vocal_service import VocalGenerator
from app.config import settings

test_text = "♪ Yo-ho-ho and a bottle of rum! ♪"

for i in range(10):
    settings.BARK_VOICE_PRESET = f"v2/en_speaker_{i}"
    gen = VocalGenerator()
    output = f"test_voice_{i}.mp3"
    gen.generate_vocals(test_text, output)
    print(f"Generated: {output}")
EOF

python test_voices.py
```

### 2. Performance Monitoring

Add logging to track generation times:

```python
# Already implemented in vocal_service.py
# Check logs for: "Vocals generated successfully"
```

### 3. Quality Assurance

Generate sample shanties and review:
- Voice quality and clarity
- Singing vs. speaking ratio
- Kid-friendliness
- Musical expressiveness

---

## 📚 Resources

- **Bark GitHub**: https://github.com/suno-ai/bark
- **Bark on HuggingFace**: https://huggingface.co/suno/bark
- **Transformers Docs**: https://huggingface.co/docs/transformers/model_doc/bark
- **Voice Samples**: https://suno-ai.notion.site/Bark-Examples

---

## ✅ Migration Complete!

You have successfully migrated from Edge TTS to Bark! Your pirate shanties can now be **sung** instead of just spoken.

Test it out and enjoy the musical pirate adventures! 🏴‍☠️🎵

**Questions or issues?** Check the troubleshooting section above or review the code in `app/services/vocal_service.py`.
