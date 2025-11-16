# Quick Start: Add Your Custom Background Music

## 🎵 3 Simple Steps

### 1. Add Your 4 Music Tracks

Copy your 4 music files into this folder:
```
background_music/
```

**Supported formats:** `.mp3`, `.wav`, `.m4a`, `.ogg`, `.flac`

### 2. Restart Backend

```bash
uvicorn app.main:app --reload
```

### 3. Generate a Song

That's it! The system will now:
- Randomly pick one of your 4 tracks
- Trim it to match the vocals length
- Mix it with the vocals

---

## 📋 What Files to Add

You need **exactly 4 tracks**. Examples:

```
background_music/
├── happy_music.mp3
├── upbeat_instrumental.mp3
├── nursery_tune.mp3
└── cheerful_melody.mp3
```

**Tips:**
- Instrumental only (no vocals)
- Upbeat and kid-friendly
- Any length (will auto-trim)
- Consistent volume across all 4

---

## ⚙️ Optional: Adjust Volume

**File:** `app/config.py` (line 26)

```python
INSTRUMENTAL_VOLUME: float = 0.4  # 0.0-1.0

# 0.3 = Quieter background
# 0.5 = Louder background
```

---

## ✅ Test It

```bash
# 1. Check your tracks are there:
ls background_music/

# 2. Start backend:
uvicorn app.main:app --reload

# 3. Generate a song
# 4. Check logs - should show:
[INFO] Using custom background music...
[INFO] Selected background track: happy_music.mp3
```

---

## 🆘 Troubleshooting

**No tracks found?**
- Check files are in `background_music/` folder
- Verify format: `.mp3`, `.wav`, `.m4a`
- Restart backend

**Background too loud/quiet?**
- Adjust `INSTRUMENTAL_VOLUME` in `app/config.py`
- Restart backend

---

That's it! For detailed info, see [CUSTOM_MUSIC_SETUP.md](CUSTOM_MUSIC_SETUP.md)
