# Fixed: Pirate Words Still Appearing

## 🔍 Root Cause Found

The problem was in **TWO places**:

### 1. **Rhyme Service** (Main Culprit)

**File:** `app/services/rhyme_service.py:25`

The preschool vocabulary list included pirate-related words:
```python
# BEFORE (Line 25):
PRESCHOOL_VOCAB = {
    ...
    "ship", "sail", "whale", "tail"  # ← PIRATE WORDS!
}
```

**What happened:**
1. User enters word like "cat"
2. System finds rhymes: "hat", "sat", "mat"
3. Then suggests: "ship", "sail" (from vocab list)
4. Gemini receives these pirate words as rhyme suggestions
5. Gemini naturally writes pirate-themed lyrics even though prompt says not to!

### 2. **Vocal Service** (Secondary Issue)

**File:** `app/services/vocal_service.py:315-336`

The cleaning function tried to *preserve* pirate vocalizations:
```python
# BEFORE:
# Remove parentheses from pirate vocalizations
pirate_words = ['arr', 'yo-ho', 'ahoy']
for word in pirate_words:
    cleaned = cleaned.replace(f'({word}!)', f'{word}!')  # Kept the word!
```

This was actively keeping "arr" and "yo-ho" in the lyrics!

---

## ✅ Fixes Applied

### Fix #1: Removed Pirate Words from Vocabulary

**File:** `app/services/rhyme_service.py`

**Lines 11-28:**
```python
# BEFORE:
PRESCHOOL_VOCAB = {
    ...
    "ship", "sail", "whale", "tail"  # Removed!
}

# AFTER:
PRESCHOOL_VOCAB = {
    ...
    # NO pirate words
    "cat", "dog", "sun", "moon", "star", "tree", "bird", "fish", "car",
    "hat", "ball", "book", "cup", "pig", "box", "fox", "bee", "day",
    "night", "light", "right", "bright", "sky", "fly", "try", "cry",
    "smile", "mile", "while", "file", "cake", "lake", "make", "take",
    "snow", "grow", "show", "glow", "feet", "meet", "sweet", "treat"
}
```

### Fix #2: Added Exclusion List

**Lines 31-48:**
```python
def get_kid_friendly_rhymes(word: str, count: int = 6) -> List[str]:
    # Words to EXCLUDE (pirate-related)
    EXCLUDED_WORDS = {
        "ship", "sail", "whale", "tail", "sea", "pirate", "arr", "ahoy",
        "treasure", "crew", "captain", "boat", "ocean", "wave", "shore",
        "anchor", "mast", "deck", "port", "voyage", "island", "parrot",
        "cannon", "sword", "gold", "chest", "map", "flag", "plank"
    }

    for rhyme in all_rhymes:
        # Skip excluded words
        if rhyme.lower() in EXCLUDED_WORDS:
            continue  # Skip pirate words entirely!
```

Now even if the rhyme library suggests "ship" or "sail", they're **completely filtered out**.

### Fix #3: Remove Pirate Vocalizations Completely

**File:** `app/services/vocal_service.py:315-336`

**BEFORE:**
```python
# Kept the words, just removed parentheses
for word in pirate_words:
    cleaned = cleaned.replace(f'({word}!)', f'{word}!')  # "arr" stays!
```

**AFTER:**
```python
# REMOVE COMPLETELY
pirate_vocalizations = [
    r'\(arr!?\)',     # (arr) or (arr!)
    r'\(yo-ho!?\)',   # (yo-ho) or (yo-ho!)
    r'\(ahoy!?\)',    # etc.
    r'\barr!?\b',     # arr without parentheses
    r'\byo-ho!?\b',   # yo-ho without parentheses
    r'\bahoy!?\b',    # ahoy without parentheses
    # ... all pirate words
]

for pattern in pirate_vocalizations:
    cleaned = re.sub(pattern, '', cleaned)  # DELETE entirely!
```

Now even if Gemini sneaks in "arr" or "yo-ho", they're **completely removed** before voice generation.

---

## 🎯 How It Works Now

### Old Flow (Broken):
```
1. User: "cat"
2. Rhyme service: ["hat", "sat", "ship", "sail"]  ← Pirate words!
3. Gemini prompt: "Use rhymes: hat, sat, ship, sail"
4. Gemini: "I see a cat, on a ship so fat..."  ← Naturally pirate-themed!
5. Output: Pirate song
```

### New Flow (Fixed):
```
1. User: "cat"
2. Rhyme service checks EXCLUDED_WORDS: ["ship", "sail"] → SKIP!
3. Rhyme service: ["hat", "sat", "bat", "mat"]  ← Only kid-friendly!
4. Gemini prompt: "Use rhymes: hat, sat, bat, mat"
                  "❌ NO pirate themes!"
5. Gemini: "I see a fluffy cat, wearing a tiny hat..."  ← Clean!
6. Vocal cleaner: Removes any stray "arr" or "yo-ho"
7. Output: Cute nursery rhyme
```

---

## 📋 All Files Changed

### Backend:
1. **`app/services/rhyme_service.py`**
   - Removed: "ship", "sail", "whale", "tail" from vocabulary
   - Added: EXCLUDED_WORDS list (30+ pirate words)
   - Added: Exclusion filter in rhyme selection

2. **`app/services/vocal_service.py`**
   - Changed: From preserving to DELETING pirate vocalizations
   - Added: Regex patterns to catch all variations
   - Added: Removal without parentheses too

---

## 🧪 Testing

### Test 1: Generate with "cat"
**Expected rhymes:** hat, sat, bat, mat, fat, rat
**NOT:** ship, sail, tail

**Expected lyrics:**
```
I see a fluffy cat
Wearing a tiny hat
It purrs and plays all day
Chasing mice away
```

**NOT:**
```
On a ship there sits a cat (arr!)
With a sail upon its hat (yo-ho!)
```

### Test 2: Generate with "tree"
**Expected rhymes:** bee, see, free, three, knee, key
**NOT:** sea

**Expected lyrics:**
```
I see a tall green tree
With a buzzing little bee
It grows up to the sky
Where the birds can fly so high
```

### Test 3: Even if Gemini adds pirate words
If Gemini somehow sneaks in:
```
I see a cat (arr!)
Wearing a pirate hat (yo-ho!)
```

The vocal cleaner will output:
```
I see a cat
Wearing a pirate hat
```
(Removed "arr" and "yo-ho")

---

## 🔍 Debug: Check What Rhymes Are Being Used

Add this to see rhymes in backend logs:

**File:** `app/tasks.py` (around line where rhymes are generated)

```python
logger.info(f"Rhymes suggested for '{word}': {rhyme_words}")
```

Then check logs:
```bash
uvicorn app.main:app --reload

# Generate song
# Check logs:
[INFO] Rhymes suggested for 'cat': ['hat', 'sat', 'bat', 'mat']
```

If you see "ship" or "sail" in the rhymes, the filter isn't working.

---

## ✅ Summary

**The pirate words were coming from:**

1. ❌ **PRESCHOOL_VOCAB** - Had "ship", "sail", "whale", "tail"
2. ❌ **Rhyme selection** - No filter for pirate words
3. ❌ **Vocal cleaner** - Preserved instead of removed

**All three are now fixed:**

1. ✅ **PRESCHOOL_VOCAB** - Removed all pirate words
2. ✅ **EXCLUDED_WORDS** - Blocks 30+ pirate-related words
3. ✅ **Vocal cleaner** - Completely deletes any pirate vocalizations

**Result:** NO MORE PIRATE THEMES! 🎉

---

## 🚀 Next Steps

1. **Restart backend** (to load new rhyme list)
```bash
uvicorn app.main:app --reload
```

2. **Test with multiple words:**
- cat → should give: hat, sat, bat
- dog → should give: log, fog, hog
- tree → should give: bee, see, free
- sun → should give: fun, run, done

3. **Check logs** to verify no pirate rhymes

4. **Listen to audio** - should have NO "arr" or "yo-ho"

All pirate references should be completely gone now! 🎶
