# Custom Background Music Setup Guide

## ✨ Overview

Your project is now configured to use **your own custom background music tracks** instead of auto-generated beats!

### How It Works:
1. You add 4 music tracks to the `background_music/` folder
2. System randomly selects one track for each song generation
3. Automatically trims the track to match the vocal length
4. Applies a smooth fade-out at the end
5. Mixes it with the vocals to create the final song

---

## 📁 Folder Structure

```
EmoryHack/
├── background_music/          ← ADD YOUR TRACKS HERE
│   ├── README.md              (instructions)
│   ├── track1.mp3             ← Your track #1
│   ├── track2.mp3             ← Your track #2
│   ├── track3.mp3             ← Your track #3
│   └── track4.mp3             ← Your track #4
├── app/
├── outputs/
└── ...
```

---

## 🎵 Adding Your Music

### Step 1: Get Your Tracks Ready

**Requirements:**
- **Number**: 4 tracks (can be the same track duplicated if you only have 1)
- **Format**: MP3, WAV, M4A, OGG, or FLAC
- **Length**: Any length (will be auto-trimmed)
- **Style**: Instrumental, upbeat, kid-friendly
- **No vocals**: Background music only (vocals will clash)

**Recommended:**
- Instrumental nursery rhyme style
- Upbeat and happy
- 90-120 BPM
- Clean, clear audio
- Consistent volume across all 4 tracks

### Step 2: Copy Tracks to Folder

```bash
# Windows (PowerShell or Command Prompt)
cd C:\Users\sufya\OneDrive\Desktop\EmoryHack\background_music

# Then copy your files:
# - Drag and drop your 4 tracks into this folder
# OR use copy command:
copy "C:\path\to\your\music\track1.mp3" .
copy "C:\path\to\your\music\track2.mp3" .
copy "C:\path\to\your\music\track3.mp3" .
copy "C:\path\to\your\music\track4.mp3" .
```

**Naming:**
- You can name them anything: `track1.mp3`, `happy_song.mp3`, `music_01.wav`, etc.
- The system will find all supported audio files automatically

### Step 3: Verify Setup

```bash
# List files in folder
cd background_music
ls
# OR on Windows:
dir

# Should show:
# README.md
# track1.mp3
# track2.mp3
# track3.mp3
# track4.mp3
```

---

## ⚙️ Configuration

### Settings (Already Configured)

**File:** `app/config.py`

```python
# Background Music Settings
USE_CUSTOM_BACKGROUND_MUSIC: bool = True  # ✅ Enabled
BACKGROUND_MUSIC_FADE_OUT: float = 1.0    # 1 second fade-out
```

### Adjust Volume (Optional)

**File:** `app/config.py` (line 26)

```python
# Control background music volume
INSTRUMENTAL_VOLUME: float = 0.4  # 0.0-1.0 (default: 0.4)

# Examples:
# 0.3 = Quieter background (more focus on vocals)
# 0.5 = Louder background (more energetic)
# 0.2 = Very quiet background
```

### Adjust Fade-Out (Optional)

**File:** `app/config.py` (line 32)

```python
BACKGROUND_MUSIC_FADE_OUT: float = 1.0  # seconds

# Examples:
# 0.5 = Quick fade (0.5 seconds)
# 2.0 = Long fade (2 seconds)
# 0.0 = No fade (abrupt end)
```

---

## 🚀 How It Works

### Generation Flow:

```
1. User enters word: "cat"
   ↓
2. Lyrics generated (4-6 lines)
   ↓
3. Vocals generated (15-20 seconds)
   ↓
4. System randomly picks 1 of your 4 tracks
   ↓
5. Track trimmed to 15-20 seconds (matches vocals)
   ↓
6. Fade-out applied to last 1 second
   ↓
7. Mixed with vocals (background at 40% volume)
   ↓
8. Final song ready! 🎵
```

### Example:

**Your track:** 3 minutes long
**Vocals duration:** 18 seconds

**Result:**
- First 17 seconds of your track (normal)
- Last 1 second (fade out)
- Total: 18 seconds
- Mixed with vocals

**If track is too short:**
- Track loops until it matches vocal length
- Fade-out applied to end

---

## 🧪 Testing

### Test the Setup:

```bash
# 1. Make sure you have 4 tracks in background_music/

# 2. Restart backend
uvicorn app.main:app --reload

# 3. Generate a song
# - Go to frontend: http://localhost:5173
# - Enter word: "cat"
# - Click "♫ Play ♫"

# 4. Check logs
# Should see:
[INFO] Using custom background music for 'cat'...
[INFO] Found 4 background music tracks
[INFO] Selected background track: track2.mp3
[INFO] Trimmed track to 18.50s with 1.0s fade-out
[INFO] Custom background music saved: ...
```

### Verify Random Selection:

Generate multiple songs and check logs - different tracks should be selected:

```
Song 1: Selected background track: track1.mp3
Song 2: Selected background track: track3.mp3
Song 3: Selected background track: track1.mp3
Song 4: Selected background track: track4.mp3
```

---

## 🔧 Troubleshooting

### "No background music tracks found"

**Problem:** System can't find your tracks

**Solution:**
```bash
# Check folder exists
ls background_music/

# Check files are there
ls background_music/*.mp3

# Should show your tracks
```

**If empty:**
- Add your 4 tracks to the folder
- Make sure they're `.mp3`, `.wav`, `.m4a`, `.ogg`, or `.flac`

### "Error processing background track"

**Problem:** Track file is corrupted or wrong format

**Solution:**
- Re-download the track
- Convert to MP3 using online converter
- Try a different track

### Background music too loud/quiet

**Solution:**

Adjust in `app/config.py`:
```python
INSTRUMENTAL_VOLUME: float = 0.3  # Make quieter (was 0.4)
# OR
INSTRUMENTAL_VOLUME: float = 0.5  # Make louder (was 0.4)
```

Restart backend after change.

### Want to use generated beats instead

**Solution:**

Change in `app/config.py`:
```python
USE_CUSTOM_BACKGROUND_MUSIC: bool = False  # Disable custom music
```

System will use auto-generated beats instead.

---

## 📊 Advanced: Validate Your Tracks

### Check Track Info:

Create a test script: `test_music.py`

```python
from app.services.background_music_service import BackgroundMusicManager

# Initialize manager
manager = BackgroundMusicManager()

# Validate all tracks
results = manager.validate_tracks()

print(f"Total tracks found: {results['total_tracks']}")
print(f"Valid tracks: {len(results['valid_tracks'])}")
print(f"Invalid tracks: {len(results['invalid_tracks'])}")

# Show details
for track in results['valid_tracks']:
    print(f"\n✅ {track['name']}")
    print(f"   Duration: {track['duration']:.2f}s")
    print(f"   Format: {track['format']}")
    print(f"   Size: {track['size_mb']:.2f} MB")

for track in results['invalid_tracks']:
    print(f"\n❌ {track['name']}")
    print(f"   Error: {track['error']}")
```

Run:
```bash
python test_music.py
```

---

## 🎨 Recommended Music Sources

### Free Instrumental Music:

1. **YouTube Audio Library** (YouTube Studio)
   - Free, no attribution required
   - Filter by "Children's Music" or "Happy"

2. **Incompetech** (incompetech.com)
   - Free with attribution
   - Search for "happy", "upbeat", "children"

3. **Bensound** (bensound.com)
   - Free with attribution
   - Look for "Happy" or "Kids" category

4. **FreePD** (freepd.com)
   - Public domain music
   - Filter by "Children's" or "Happy"

### Download Tips:
- Download as MP3 (128kbps or higher)
- Look for "instrumental" (no vocals)
- 15-30 second clips work great (will loop if needed)
- Upbeat, positive melodies

---

## 📝 Example .env Configuration

```bash
# Enable custom background music
USE_CUSTOM_BACKGROUND_MUSIC=true

# Background music volume (0.0-1.0)
INSTRUMENTAL_VOLUME=0.4

# Fade-out duration in seconds
BACKGROUND_MUSIC_FADE_OUT=1.0
```

---

## ✅ Quick Start Checklist

- [ ] Create `background_music/` folder (✅ Already done!)
- [ ] Add 4 music tracks to the folder
- [ ] Verify tracks are supported format (.mp3, .wav, etc.)
- [ ] Restart backend server
- [ ] Generate a test song
- [ ] Check logs to see which track was selected
- [ ] Listen to verify background music is present
- [ ] Adjust volume if needed in config.py

---

## 🎯 Summary

**What you need to do:**
1. Add 4 music tracks to `background_music/` folder
2. Restart backend
3. Generate songs - enjoy custom music!

**What the system does automatically:**
- Randomly picks 1 of your 4 tracks
- Trims to exact vocal length
- Adds smooth fade-out
- Mixes with vocals
- Creates final song

**No coding required!** Just add your tracks and restart. 🎉

---

## 🆘 Need Help?

If tracks aren't working:

1. Check backend logs for errors
2. Verify tracks are in `background_music/` folder
3. Ensure tracks are supported format
4. Try converting to MP3 if using other format
5. Check file permissions (should be readable)

All set! Add your 4 tracks and enjoy custom background music! 🎵
