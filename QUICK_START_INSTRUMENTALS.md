# 🎵 Quick Start: Add Background Music to Your Pirate Songs

## ✅ What's Already Set Up

Your app **already has background music support built in**!

- ✅ BPM detection (automatically detects vocal tempo)
- ✅ Beat matching (finds closest BPM instrumental)
- ✅ Audio mixing (combines vocals + instrumental)
- ✅ Volume balancing (vocals louder, beat softer)
- ✅ Automatic looping (repeats beat to match vocal length)

All you need: **Add some beat files!**

---

## 🚀 Fastest Way to Test (2 minutes)

### Option 1: Use Test Beat (Already Done!)

You already have a test beat ready! Just restart Celery:

```bash
# Stop current Celery (Ctrl+C in Terminal 1)
# Then restart:
source venv/bin/activate
celery -A app.tasks worker --loglevel=info
```

Now generate a song - it will automatically include background music!

```bash
# In your browser or curl:
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{"word":"treasure"}'
```

### Option 2: Download Real Pirate Beats

For better quality, download free beats:

**Easiest source: Pixabay**
1. Go to: https://pixabay.com/music/
2. Search: "sea shanty" or "pirate"
3. Download 2-3 tracks (free, no sign-up!)
4. Convert to WAV and add them:

```bash
# Convert MP3 to WAV
ffmpeg -i ~/Downloads/pirate_music.mp3 -ar 44100 -ac 2 beats/pirate-shanty/pirate_90bpm.wav

# Scan the new beat
python scan_beats.py

# Restart Celery
celery -A app.tasks worker --loglevel=info
```

---

## 📊 What's in Your Beats Library Right Now

```json
{
  "pirate-shanty": [
    {
      "filename": "test_beat_95bpm.wav",
      "bpm": 95.7,
      "duration": 10.0
    }
  ]
}
```

You have **1 beat** at **95.7 BPM** ready to use!

---

## 🎯 How It Works

When you generate a song, the system:

1. **Generates vocals** → Edge TTS creates spoken lyrics
2. **Detects vocal BPM** → Librosa analyzes tempo (~90-100 BPM typical)
3. **Finds matching beat** → Searches catalog for closest BPM (±15 tolerance)
4. **Loops beat** → Repeats 10s beat to match 35s vocals
5. **Mixes audio** → Combines with balanced volumes
6. **Saves result** → Final song in `outputs/` folder

**Example logs you'll see:**
```
[INFO] Detected BPM: 92.3 from vocals
[INFO] Finding instrumental for 92.3 BPM, genre: pirate-shanty
[INFO] Selected beat: test_beat_95bpm.wav at 95.7 BPM
[INFO] Mixing vocals with instrumental
[INFO] Mixed audio saved to outputs/song_abc123.mp3
```

---

## ⚙️ Adjust Volumes (Optional)

Edit your `.env` file:

```bash
# Make vocals louder
VOCALS_VOLUME=0.9

# Make beat quieter
INSTRUMENTAL_VOLUME=0.4
```

Default settings:
- Vocals: 80% (0.8) - clear and prominent
- Instrumental: 50% (0.5) - background support

---

## 🎵 Recommended Beat Specs for Kids

- **BPM**: 85-105 (slow to moderate)
- **Style**: Folk, acoustic, nautical
- **Instruments**: Accordion, fiddle, guitar
- **Mood**: Happy, bouncy, fun (not scary!)
- **Length**: 5+ seconds (will loop)
- **Format**: WAV, 44.1kHz, stereo

---

## 🔍 Troubleshooting

### "No instrumental found, using vocals only"

**Problem**: No beats in library
**Fix**: Add at least one WAV file to `beats/pirate-shanty/` and run `python scan_beats.py`

### "Closest beat is 20 BPM away, exceeds tolerance"

**Problem**: Your beat BPM too different from vocals
**Fix**: Download beats closer to 90-100 BPM, or add more variety

### Beat sounds too loud/quiet

**Problem**: Volume imbalance
**Fix**: Adjust `VOCALS_VOLUME` and `INSTRUMENTAL_VOLUME` in `.env`

---

## 📚 More Information

- **Full guide**: See `FREE_INSTRUMENTALS_GUIDE.md`
- **Free sources**: Pixabay, FreeSoundEffects, YouTube Audio Library
- **Beat scanner**: `python scan_beats.py`
- **Test beat generator**: `python generate_test_beat.py`

---

## 🎉 You're Ready!

Your pirate karaoke app will now automatically add background music to every song!

Just restart Celery and generate a song to test it out.

**Happy sailing!** 🏴‍☠️🎵
