# 🎤 ElevenLabs + Bark Hybrid TTS Setup Guide

Your system now uses **ElevenLabs as primary** with **Bark as automatic fallback** for the best voice quality!

---

## ✅ What's Been Set Up

### 1. **Hybrid Architecture**
- **Primary:** ElevenLabs (professional teacher voice)
- **Fallback:** Bark (expressive voice with optimizations)
- **Auto-switching:** If ElevenLabs fails, automatically uses Bark

### 2. **Files Modified**
- ✅ `requirements.txt` - Added elevenlabs package
- ✅ `app/config.py` - Added all TTS settings
- ✅ `app/services/vocal_service.py` - New hybrid implementation
- ✅ `.env.example` - Updated with all settings
- ✅ Backup created: `vocal_service_bark_only.py.backup`

### 3. **Packages Installed**
- ✅ `elevenlabs==2.23.0`
- ✅ All dependencies

---

## 🔧 Final Setup Steps

### Step 1: Update Your `.env` File

**Add these settings to your `.env` file** (after line 27, before the Bark settings):

```bash
# TTS Provider Settings
TTS_PROVIDER=elevenlabs
TTS_FALLBACK_TO_BARK=True

# ElevenLabs TTS Settings (Primary)
ELEVENLABS_VOICE_ID=EXAVITQu4vr4xnSDxMaL
ELEVENLABS_MODEL=eleven_multilingual_v2
ELEVENLABS_STABILITY=0.5
ELEVENLABS_SIMILARITY=0.75
ELEVENLABS_STYLE=0.0
ELEVENLABS_BOOST=True
```

Your `.env` should look like this:
```bash
# API Keys
GEMINI_API_KEY=AIzaSy...  # Your existing Gemini key
ELEVENLABS_API_KEY=b3edd...  # Your existing ElevenLabs key

...

# TTS Provider Settings
TTS_PROVIDER=elevenlabs
TTS_FALLBACK_TO_BARK=True

# ElevenLabs TTS Settings (Primary)
ELEVENLABS_VOICE_ID=EXAVITQu4vr4xnSDxMaL
ELEVENLABS_MODEL=eleven_multilingual_v2
ELEVENLABS_STABILITY=0.5
ELEVENLABS_SIMILARITY=0.75
ELEVENLABS_STYLE=0.0
ELEVENLABS_BOOST=True

# Bark TTS Settings (Fallback)
BARK_MODEL=suno/bark
BARK_VOICE_PRESET=v2/en_speaker_9
...
```

### Step 2: Restart Celery Worker

```bash
# Press Ctrl+C in your Celery terminal
cd /mnt/c/Users/sufya/OneDrive/Desktop/EmoryHack
source venv/bin/activate
celery -A app.tasks worker --loglevel=info
```

**Expected logs:**
```
[INFO] ElevenLabs TTS initialized successfully
[INFO] Bark TTS initialized successfully
[INFO] VocalGenerator initialized: Primary=elevenlabs, Fallback=True
```

---

## 🎯 How It Works

### Flow Diagram

```
Generate Song Request
      ↓
[Try ElevenLabs TTS]
      ↓
  Success? ━━━━━━┓
   ↓ Yes        ↓ No
   │       [Fallback to Bark]
   │             ↓
   └─────────→ [Mix with Beat]
                 ↓
           [Final MP3]
```

### Automatic Fallback Scenarios

**Bark is used when:**
1. ❌ ElevenLabs API key is invalid
2. ❌ ElevenLabs API quota exceeded
3. ❌ ElevenLabs API is down/timeout
4. ❌ Network issues prevent API call
5. ⚙️ `TTS_PROVIDER=bark` in `.env`

---

## 🎤 Voice Configuration

### ElevenLabs Voices (Primary)

**Current Voice:** `EXAVITQu4vr4xnSDxMaL` (Bella - Young, warm teacher)

**Other Great Options:**
| Voice ID | Name | Description | Best For |
|----------|------|-------------|----------|
| `EXAVITQu4vr4xnSDxMaL` | Bella | Young, warm female | ⭐ Current - Perfect for kids |
| `21m00Tcm4TlvDq8ikWAM` | Rachel | Calm, mature female | Professional narration |
| `ThT5KcBeYPX3keUQqHPh` | Dorothy | Pleasant, friendly | Storytelling |
| `pNInz6obpgDQGcFmaJgB` | Adam | Warm male | Alternative |

**To change voice:** Update `ELEVENLABS_VOICE_ID` in `.env`

### Voice Settings Explained

```bash
ELEVENLABS_STABILITY=0.5     # 0-1: Higher = more consistent
ELEVENLABS_SIMILARITY=0.75   # 0-1: Higher = closer to original
ELEVENLABS_STYLE=0.0         # 0-1: Exaggeration of style
ELEVENLABS_BOOST=True        # Speaker boost for clarity
```

**For more expressive (current is balanced):**
```bash
ELEVENLABS_STABILITY=0.3
ELEVENLABS_SIMILARITY=0.6
ELEVENLABS_STYLE=0.5
```

---

## 🧪 Testing

### Test 1: Generate with ElevenLabs

```bash
# Make sure Celery is running with new settings
# Then in browser console:

fetch('http://localhost:8000/api/generate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ word: 'ocean' })
})
.then(r => r.json())
.then(d => console.log('Job ID:', d.job_id));
```

**Watch Celery logs - you should see:**
```
[INFO] VocalGenerator initialized: Primary=elevenlabs, Fallback=True
[INFO] Generating vocals with ElevenLabs...
[INFO] ElevenLabs vocals generated successfully
```

### Test 2: Test Fallback to Bark

**Temporarily disable ElevenLabs to test fallback:**

```bash
# In .env, temporarily change:
ELEVENLABS_API_KEY=invalid_key_for_testing
```

**Restart Celery and generate again:**

**Expected logs:**
```
[ERROR] Failed to initialize ElevenLabs: Invalid API key
[INFO] Bark TTS initialized successfully
[INFO] VocalGenerator initialized: Primary=elevenlabs, Fallback=True
[WARNING] Falling back to alternative TTS provider...
[INFO] Falling back to Bark...
[INFO] Split lyrics into 4 chunks for Bark
[INFO] Bark vocals generated successfully
```

**Then restore your real API key!**

### Test 3: Force Bark Only

```bash
# In .env:
TTS_PROVIDER=bark
```

This uses only Bark (no ElevenLabs calls at all).

---

## 📊 Comparison

### ElevenLabs vs Bark

| Feature | ElevenLabs | Bark (Optimized) |
|---------|-----------|------------------|
| **Quality** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Teacher-like** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Consistency** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Speed** | ⭐⭐⭐⭐⭐ (3-5s) | ⭐⭐⭐ (20-30s) |
| **Cost** | ~$0.30/song | Free |
| **Internet** | Required | Not required |
| **GPU** | Not needed | Recommended |

### When Each is Used

**ElevenLabs (Primary):**
- ✅ Best voice quality
- ✅ Fastest generation
- ✅ Most consistent
- ✅ Perfect for production

**Bark (Fallback):**
- ✅ No API costs
- ✅ Works offline
- ✅ More expressive (can sing)
- ✅ Great for development/testing

---

## 💰 ElevenLabs Pricing

### Free Tier
- **10,000 characters/month**
- ~20-30 pirate shanties
- Perfect for testing and demos

### Paid Tiers
- **Starter:** $5/month = 30,000 chars (~60 songs)
- **Creator:** $22/month = 100,000 chars (~200 songs)
- **Pro:** $99/month = 500,000 chars (~1000 songs)

**For hackathon:** Free tier is plenty! 🎉

---

## 🔧 Troubleshooting

### Issue: "ElevenLabs not available"

**Check:**
1. Is `elevenlabs` package installed? `pip list | grep elevenlabs`
2. Is API key in `.env`? `cat .env | grep ELEVENLABS_API_KEY`
3. Is API key valid? Test at https://elevenlabs.io

**Solution:** Install package or check API key

---

### Issue: "Both TTS providers failed"

**Cause:** Neither ElevenLabs nor Bark could generate audio

**Check Celery logs for:**
- ElevenLabs error message
- Bark error message

**Common fixes:**
- Invalid API key → Update `.env`
- GPU out of memory → Restart Celery
- Network issues → Check internet

---

### Issue: Voice sounds wrong

**ElevenLabs:**
- Try different `ELEVENLABS_VOICE_ID`
- Adjust `ELEVENLABS_STABILITY` (0.3-0.7)

**Bark:**
- Try different `BARK_VOICE_PRESET` (v2/en_speaker_7, v2/en_speaker_9)
- Run `python test_voices.py` to compare

---

## 📝 Configuration Cheat Sheet

### Use Only ElevenLabs (No Fallback)
```bash
TTS_PROVIDER=elevenlabs
TTS_FALLBACK_TO_BARK=False
```

### Use Only Bark (No ElevenLabs)
```bash
TTS_PROVIDER=bark
TTS_FALLBACK_TO_BARK=False
```

### Hybrid (Current - Recommended)
```bash
TTS_PROVIDER=elevenlabs
TTS_FALLBACK_TO_BARK=True
```

### Switch to Bark If Low on Credits
```bash
TTS_PROVIDER=bark
TTS_FALLBACK_TO_BARK=False
```

---

## 🎯 Best Practices

### For Development
- Use `TTS_PROVIDER=bark` to save ElevenLabs credits
- Test features without API calls

### For Demo/Production
- Use `TTS_PROVIDER=elevenlabs` for best quality
- Enable fallback for reliability

### For Hackathon Presentation
- Use ElevenLabs for the demo
- Show fallback feature if time permits

---

## ✅ Final Checklist

Before testing:
- [ ] `.env` has all TTS settings
- [ ] `ELEVENLABS_API_KEY` is set correctly
- [ ] Celery worker restarted
- [ ] Logs show "ElevenLabs TTS initialized successfully"
- [ ] Logs show "Bark TTS initialized successfully"

---

## 🚀 Quick Start Commands

```bash
# 1. Make sure .env is updated (see Step 1 above)

# 2. Restart Celery
celery -A app.tasks worker --loglevel=info

# 3. Generate a song
curl -X POST http://localhost:8000/api/generate \
  -H 'Content-Type: application/json' \
  -d '{"word": "treasure"}'

# 4. Listen to the results!
```

---

## 🎉 Success Indicators

**You'll know it's working when:**

1. ✅ Celery logs show both TTS engines initialized
2. ✅ Songs generate in **3-5 seconds** (was 20-30s with Bark only)
3. ✅ Voice quality is **dramatically better** - professional teacher voice
4. ✅ If ElevenLabs fails, Bark takes over seamlessly
5. ✅ Kids will love the warm, clear voice! 🎤

---

**Enjoy your professional-quality pirate shanty karaoke! 🏴‍☠️✨**

Questions? Check the logs or review the comparison table above!
