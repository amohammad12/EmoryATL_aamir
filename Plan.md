I am creating an web app which creates rhymes with audio like a song for pre-school kids in karaoke format so they listen and sing along. It just takes one input word and generates the whole thing.

Step 1: Takes in one one input "word"

Step 2: Generate rhyming words

Step 3: Generate Vocals first

Step 4: Detect vocal tempo 

Step 5: Try to generate matched instrumental

Step 6: Mix 

Step 7: final output


Example usuage:

'''
Complete Tools & Resources for Hybrid Approach (Solution 1 + 2)

1. PYTHON LIBRARIES (All Free & Open-Source)
Complete requirements.txt
txt# ===== CORE BACKEND =====
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0
python-dotenv==1.0.0
python-multipart==0.0.6

# ===== RHYME GENERATION =====
pronouncing==0.2.0
nltk==3.8.1

# ===== LLM () =====
Gemini API key

# ===== AUDIO GENERATION =====
# Bark for vocals
git+https://github.com/suno-ai/bark.git

# MusicGen for instrumentals
audiocraft==1.3.0
torch>=2.0.0
torchaudio>=2.0.0

# ===== AUDIO PROCESSING & ANALYSIS =====
# BPM detection and audio analysis
librosa==0.10.1
soundfile==0.12.1

# Audio manipulation and mixing
pydub==0.25.1

# Scientific computing
numpy==1.26.2
scipy==1.11.4

# Time-stretching (optional but useful)
pyrubberband==0.3.0

# ===== ASYNC TASKS (Optional) =====
celery==5.3.4
redis==5.0.1

# ===== UTILITIES =====
requests==2.31.0
aiofiles==23.2.1

# ===== TIMESTAMP ALIGNMENT (Optional) =====
# For karaoke features
aeneas==1.7.3

2. FREE ROYALTY-FREE BEAT LIBRARIES
A. Direct Download Sources
Looperman (Best for Hip-Hop/Rap)

URL: https://www.looperman.com
License: Royalty-free, credit required
Formats: WAV, MP3
BPMs: Clearly labeled
Genres: Hip-Hop, Trap, Lo-fi, R&B

How to use:
bash# Create beats directory
mkdir -p beats/{hip-hop,trap,lofi,rnb}

# Download and organize by BPM
beats/
├── hip-hop/
│   ├── 80bpm_chill.wav
│   ├── 90bpm_classic.wav
│   ├── 95bpm_boom_bap.wav
│   └── 100bpm_upbeat.wav
├── trap/
│   ├── 140bpm_hard.wav
│   └── 145bpm_melodic.wav
└── lofi/
    └── 85bpm_jazzy.wav
FreeSoundEffects.com

URL: https://www.freesoundeffects.com/free-sounds/hip-hop-10041/
License: Free for commercial use
Quality: Professional
Download: Direct MP3/WAV

YouTube Audio Library

URL: https://www.youtube.com/audiolibrary
License: Some tracks are free, check individual
Filter by: Genre, BPM, mood
Download: MP3

Free Music Archive

URL: https://freemusicarchive.org
License: Various Creative Commons
Filter: By tempo and genre
Format: High-quality WAV/FLAC

Incompetech (Kevin MacLeod)

URL: https://incompetech.com/music/royalty-free/music.html
License: Free with attribution
BPM: Listed for each track
Genres: All types

BenSound

URL: https://www.bensound.com
License: Free with credit
Quality: Very high
Download: MP3/WAV


B. Programmatic Beat Generation (100% Free)
Magenta (Google)
bashpip install magenta

# Generate MIDI beats
from magenta.models.drums_rnn import drums_rnn_sequence_generator
Basic Pitch (Spotify) - Convert audio to MIDI
bashpip install basic-pitch

# Extract MIDI from audio samples
basic-pitch output_dir/ input_audio.wav

3. BPM DETECTION TOOLS
A. Librosa (Recommended - Already in requirements)
pythonimport librosa
import numpy as np

def detect_bpm(audio_path: str) -> float:
    """Detect BPM from audio file"""
    y, sr = librosa.load(audio_path)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    return float(tempo)

def detect_bpm_from_array(audio: np.ndarray, sr: int = 24000) -> float:
    """Detect BPM from numpy array"""
    tempo, _ = librosa.beat.beat_track(y=audio, sr=sr)
    return float(tempo)

# Advanced: Get beat timestamps
def get_beat_times(audio_path: str):
    """Get exact beat timestamps"""
    y, sr = librosa.load(audio_path)
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beats, sr=sr)
    return tempo, beat_times
B. Aubio (Alternative)
bashpip install aubio
pythonimport aubio
import numpy as np

def detect_bpm_aubio(audio_path: str) -> float:
    """Detect BPM using aubio"""
    source = aubio.source(audio_path)
    tempo = aubio.tempo("default", 1024, 512, source.samplerate)
    
    total_frames = 0
    while True:
        samples, read = source()
        tempo(samples)
        total_frames += read
        if read < source.hop_size:
            break
    
    return tempo.get_bpm()

4. AUDIO MANIPULATION TOOLS
A. Pydub (Already in requirements)
pythonfrom pydub import AudioSegment
from pydub.playback import play

# Load audio
beat = AudioSegment.from_wav("beat.wav")
vocals = AudioSegment.from_wav("vocals.wav")

# Adjust volume
beat = beat - 6  # Reduce by 6dB
vocals = vocals + 3  # Increase by 3dB

# Loop beat to match duration
target_duration = len(vocals)
beat_looped = beat * (target_duration // len(beat) + 1)
beat_looped = beat_looped[:target_duration]

# Mix
mixed = vocals.overlay(beat_looped)

# Export
mixed.export("output.mp3", format="mp3", bitrate="192k")
B. Pyrubberband (Time-stretching)
pythonimport pyrubberband as pyrb
import librosa

def match_tempo(audio_path: str, target_bpm: float, original_bpm: float):
    """Time-stretch audio to match target BPM"""
    y, sr = librosa.load(audio_path)
    
    # Calculate stretch rate
    rate = target_bpm / original_bpm
    
    # Stretch audio
    y_stretched = pyrb.time_stretch(y, sr, rate)
    
    return y_stretched, sr

def pitch_shift(audio: np.ndarray, sr: int, semitones: int):
    """Shift pitch without changing tempo"""
    return pyrb.pitch_shift(audio, sr, semitones)

5. BEAT LIBRARY MANAGER (Custom Tool)
Create this utility to manage your beat library:
app/utils/beat_manager.py
pythonimport os
import json
import librosa
from pathlib import Path
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class BeatLibraryManager:
    """Manage pre-made beat loops library"""
    
    def __init__(self, beats_dir: str = "beats"):
        self.beats_dir = Path(beats_dir)
        self.beats_dir.mkdir(exist_ok=True)
        self.catalog_file = self.beats_dir / "catalog.json"
        self.catalog = self._load_catalog()
    
    def _load_catalog(self) -> Dict:
        """Load beat catalog from JSON"""
        if self.catalog_file.exists():
            with open(self.catalog_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_catalog(self):
        """Save beat catalog to JSON"""
        with open(self.catalog_file, 'w') as f:
            json.dump(self.catalog, f, indent=2)
    
    def scan_beats_directory(self):
        """Scan directory and auto-detect BPM for all beats"""
        logger.info("Scanning beats directory...")
        
        for genre_dir in self.beats_dir.iterdir():
            if not genre_dir.is_dir() or genre_dir.name == '__pycache__':
                continue
            
            genre = genre_dir.name
            if genre not in self.catalog:
                self.catalog[genre] = []
            
            for beat_file in genre_dir.glob("*.wav"):
                # Check if already in catalog
                if any(b['filename'] == beat_file.name for b in self.catalog[genre]):
                    continue
                
                # Detect BPM
                try:
                    y, sr = librosa.load(str(beat_file))
                    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
                    
                    beat_info = {
                        'filename': beat_file.name,
                        'path': str(beat_file),
                        'bpm': float(tempo),
                        'duration': len(y) / sr
                    }
                    
                    self.catalog[genre].append(beat_info)
                    logger.info(f"Added {beat_file.name}: {tempo:.1f} BPM")
                    
                except Exception as e:
                    logger.error(f"Error processing {beat_file}: {e}")
        
        self._save_catalog()
        logger.info(f"Catalog updated: {sum(len(beats) for beats in self.catalog.values())} beats")
    
    def find_closest_beat(
        self, 
        target_bpm: float, 
        genre: str = "hip-hop",
        tolerance: float = 10.0
    ) -> Optional[Dict]:
        """Find beat with closest BPM to target"""
        
        if genre not in self.catalog or not self.catalog[genre]:
            # Try any genre
            all_beats = []
            for g in self.catalog.values():
                all_beats.extend(g)
            if not all_beats:
                return None
            beats = all_beats
        else:
            beats = self.catalog[genre]
        
        # Find closest match
        closest = min(
            beats, 
            key=lambda b: abs(b['bpm'] - target_bpm)
        )
        
        # Check tolerance
        if abs(closest['bpm'] - target_bpm) <= tolerance:
            return closest
        
        return None
    
    def get_beat_path(self, genre: str, bpm: float) -> Optional[str]:
        """Get path to beat file"""
        beat = self.find_closest_beat(bpm, genre)
        return beat['path'] if beat else None
    
    def list_all_beats(self) -> Dict[str, List[Dict]]:
        """List all beats in catalog"""
        return self.catalog
    
    def add_beat_manual(
        self, 
        filepath: str, 
        genre: str, 
        bpm: float
    ):
        """Manually add a beat to catalog"""
        if genre not in self.catalog:
            self.catalog[genre] = []
        
        beat_info = {
            'filename': Path(filepath).name,
            'path': filepath,
            'bpm': float(bpm),
            'duration': 0  # Will be calculated on scan
        }
        
        self.catalog[genre].append(beat_info)
        self._save_catalog()

6. DOWNLOAD SCRIPT FOR FREE BEATS
scripts/download_beats.py
python"""
Download starter pack of free beats from various sources
"""
import requests
import os
from pathlib import Path

# Free CC0 beats (public domain)
STARTER_BEATS = {
    "hip-hop": [
        {
            "url": "https://example.com/beat1.wav",  # Replace with actual URLs
            "bpm": 90,
            "name": "classic_90bpm.wav"
        },
        {
            "url": "https://example.com/beat2.wav",
            "bpm": 95,
            "name": "boom_bap_95bpm.wav"
        }
    ],
    "trap": [
        {
            "url": "https://example.com/trap1.wav",
            "bpm": 140,
            "name": "hard_140bpm.wav"
        }
    ]
}

def download_starter_beats():
    """Download starter beat pack"""
    beats_dir = Path("beats")
    beats_dir.mkdir(exist_ok=True)
    
    for genre, beats in STARTER_BEATS.items():
        genre_dir = beats_dir / genre
        genre_dir.mkdir(exist_ok=True)
        
        for beat in beats:
            output_path = genre_dir / beat['name']
            if output_path.exists():
                print(f"✓ {beat['name']} already exists")
                continue
            
            print(f"Downloading {beat['name']}...")
            try:
                response = requests.get(beat['url'], stream=True)
                response.raise_for_status()
                
                with open(output_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                print(f"✓ Downloaded {beat['name']}")
            except Exception as e:
                print(f"✗ Error downloading {beat['name']}: {e}")

if __name__ == "__main__":
    download_starter_beats()
Note: You'll need to manually find and add actual URLs from the free sources listed above.

7. UPDATED audio_service.py WITH HYBRID APPROACH
pythonimport torch
import numpy as np
from bark import generate_audio, SAMPLE_RATE as BARK_SAMPLE_RATE
from audiocraft.models import MusicGen
from pydub import AudioSegment
from scipy.io import wavfile
import librosa
import logging
import uuid
from pathlib import Path
from app.config import settings
from app.utils.beat_manager import BeatLibraryManager

logger = logging.getLogger(__name__)

class AudioService:
    """Generate and mix audio (vocals + instrumental) with BPM matching"""
    
    def __init__(self):
        self.sample_rate = settings.SAMPLE_RATE
        self.output_dir = settings.OUTPUT_DIR
        self.temp_dir = settings.TEMP_DIR
        
        # Initialize beat library manager
        self.beat_manager = BeatLibraryManager("beats")
        
        # Lazy load models
        self.musicgen_model = None
    
    def detect_bpm(self, audio: np.ndarray, sr: int = 24000) -> float:
        """
        Detect BPM from audio array
        
        Args:
            audio: Audio numpy array
            sr: Sample rate
            
        Returns:
            BPM as float
        """
        try:
            tempo, _ = librosa.beat.beat_track(y=audio, sr=sr)
            bpm = float(tempo)
            logger.info(f"Detected BPM: {bpm:.1f}")
            return bpm
        except Exception as e:
            logger.warning(f"BPM detection failed: {e}, using default 90 BPM")
            return 90.0
    
    def generate_rap_vocals(self, lyrics: str) -> np.ndarray:
        """
        Generate rap/spoken vocals using Bark
        
        Args:
            lyrics: Text lyrics to convert to speech
            
        Returns:
            Audio array
        """
        try:
            logger.info("Generating vocals with Bark...")
            
            # Split lyrics into chunks
            chunks = self._split_lyrics(lyrics)
            
            audio_chunks = []
            for i, chunk in enumerate(chunks):
                logger.info(f"Generating chunk {i+1}/{len(chunks)}")
                audio_array = generate_audio(
                    chunk,
                    history_prompt="v2/en_speaker_9"  # Rap/rhythmic voice
                )
                audio_chunks.append(audio_array)
            
            # Concatenate all chunks
            full_audio = np.concatenate(audio_chunks)
            
            logger.info(f"Vocals generated: {len(full_audio)/BARK_SAMPLE_RATE:.1f}s")
            return full_audio
            
        except Exception as e:
            logger.error(f"Error generating vocals: {e}")
            raise
    
    def generate_instrumental_matched(
        self,
        vocals: np.ndarray,
        genre: str = "hip-hop",
        use_musicgen: bool = True
    ) -> np.ndarray:
        """
        Generate instrumental matching vocal characteristics
        HYBRID: Try MusicGen first, fallback to pre-made loops
        
        Args:
            vocals: Vocals audio array
            genre: Music genre
            use_musicgen: Try MusicGen before fallback
            
        Returns:
            Instrumental audio array
        """
        # Detect vocal characteristics
        vocal_bpm = self.detect_bpm(vocals, BARK_SAMPLE_RATE)
        vocal_duration = len(vocals) / BARK_SAMPLE_RATE
        
        instrumental = None
        
        # Strategy 1: Try MusicGen with BPM specification
        if use_musicgen:
            try:
                logger.info("Attempting MusicGen generation...")
                instrumental = self._generate_with_musicgen(
                    genre, 
                    vocal_bpm, 
                    vocal_duration
                )
            except Exception as e:
                logger.warning(f"MusicGen failed: {e}, falling back to loops")
        
        # Strategy 2: Fallback to pre-made loops
        if instrumental is None:
            logger.info("Using pre-made beat loop...")
            instrumental = self._use_premade_loop(
                genre,
                vocal_bpm,
                vocal_duration
            )
        
        # Match lengths
        instrumental = self._match_length(instrumental, len(vocals))
        
        return instrumental
    
    def _generate_with_musicgen(
        self,
        genre: str,
        bpm: float,
        duration: float
    ) -> np.ndarray:
        """Generate instrumental with MusicGen"""
        
        # Lazy load model
        if self.musicgen_model is None:
            logger.info("Loading MusicGen model...")
            self.musicgen_model = MusicGen.get_pretrained('facebook/musicgen-small')
            self.musicgen_model.set_generation_params(
                duration=min(int(duration) + 2, 30)  # MusicGen max is 30s
            )
        
        # Create BPM-aware prompt
        prompt = f"{genre} instrumental beat at {int(bpm)} BPM, steady rhythm, no vocals"
        
        logger.info(f"Generating: {prompt}")
        
        # Generate
        wav = self.musicgen_model.generate([prompt])
        instrumental = wav[0].cpu().numpy().squeeze()
        
        logger.info(f"MusicGen generated {len(instrumental)/self.sample_rate:.1f}s")
        
        return instrumental
    
    def _use_premade_loop(
        self,
        genre: str,
        target_bpm: float,
        duration: float
    ) -> np.ndarray:
        """Use pre-made loop from library"""
        
        # Find closest matching beat
        beat_info = self.beat_manager.find_closest_beat(target_bpm, genre)
        
        if beat_info is None:
            raise Exception(f"No suitable beat found for {genre} at ~{target_bpm} BPM")
        
        logger.info(f"Using beat: {beat_info['filename']} ({beat_info['bpm']:.1f} BPM)")
        
        # Load beat
        beat, sr = librosa.load(beat_info['path'], sr=self.sample_rate)
        
        # Time-stretch if BPM difference is significant
        bpm_diff = abs(beat_info['bpm'] - target_bpm)
        if bpm_diff > 5:
            logger.info(f"Time-stretching from {beat_info['bpm']:.1f} to {target_bpm:.1f} BPM")
            try:
                import pyrubberband as pyrb
                rate = target_bpm / beat_info['bpm']
                beat = pyrb.time_stretch(beat, sr, rate)
            except ImportError:
                logger.warning("pyrubberband not available, skipping time-stretch")
        
        # Loop to match duration
        beat_length = len(beat) / sr
        repeats = int(np.ceil(duration / beat_length))
        beat_looped = np.tile(beat, repeats)
        
        return beat_looped
    
    def _match_length(self, instrumental: np.ndarray, target_length: int) -> np.ndarray:
        """Match instrumental length to vocals"""
        if len(instrumental) > target_length:
            return instrumental[:target_length]
        elif len(instrumental) < target_length:
            # Pad with silence
            pad_length = target_length - len(instrumental)
            return np.pad(instrumental, (0, pad_length), mode='constant')
        return instrumental
    
    def mix_audio(
        self, 
        vocals: np.ndarray, 
        instrumental: np.ndarray,
        vocals_volume: float = 1.0,
        instrumental_volume: float = 0.6
    ) -> str:
        """
        Mix vocals and instrumental, save to file
        
        Args:
            vocals: Vocals audio array
            instrumental: Instrumental audio array
            vocals_volume: Volume multiplier for vocals (0-1)
            instrumental_volume: Volume multiplier for instrumental (0-1)
            
        Returns:
            Path to output audio file
        """
        try:
            logger.info("Mixing vocals and instrumental...")
            
            # Generate unique filename
            output_filename = f"{uuid.uuid4()}.mp3"
            output_path = self.output_dir / output_filename
            
            # Save to temp WAV files
            vocals_temp = self.temp_dir / f"vocals_{uuid.uuid4()}.wav"
            inst_temp = self.temp_dir / f"inst_{uuid.uuid4()}.wav"
            
            wavfile.write(str(vocals_temp), BARK_SAMPLE_RATE, vocals)
            wavfile.write(str(inst_temp), BARK_SAMPLE_RATE, instrumental)
            
            # Load with pydub
            vocals_audio = AudioSegment.from_wav(str(vocals_temp))
            inst_audio = AudioSegment.from_wav(str(inst_temp))
            
            # Adjust volumes (convert to dB)
            vocals_db = 20 * np.log10(vocals_volume) if vocals_volume > 0 else -60
            inst_db = 20 * np.log10(instrumental_volume) if instrumental_volume > 0 else -60
            
            vocals_audio = vocals_audio + vocals_db
            inst_audio = inst_audio + inst_db
            
            # Mix
            mixed = vocals_audio.overlay(inst_audio)
            
            # Export
            mixed.export(str(output_path), format="mp3", bitrate="192k")
            
            # Cleanup
            vocals_temp.unlink()
            inst_temp.unlink()
            
            logger.info(f"Mixed audio saved: {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"Error mixing audio: {e}")
            raise
    
    def _split_lyrics(self, lyrics: str, max_chars: int = 300) -> list:
        """Split lyrics into chunks for Bark processing"""
        if "(PAUSE)" in lyrics:
            chunks = lyrics.split("(PAUSE)")
        else:
            lines = lyrics.split('\n')
            chunks = []
            current_chunk = ""
            
            for line in lines:
                if len(current_chunk) + len(line) < max_chars:
                    current_chunk += line + "\n"
                else:
                    if current_chunk:
                        chunks.append(current_chunk.strip())
                    current_chunk = line + "\n"
            
            if current_chunk:
                chunks.append(current_chunk.strip())
        
        return [chunk.strip() for chunk in chunks if chunk.strip()]
    
    def generate_complete_song(
        self,
        word: str,
        rhymes: list,
        lyrics: str,
        genre: str = "hip-hop",
        energy: str = "medium"
    ) -> dict:
        """
        Complete song generation pipeline
        
        Returns:
            dict with audio_path, bpm, duration, etc.
        """
        try:
            # 1. Generate vocals
            vocals = self.generate_rap_vocals(lyrics)
            
            # 2. Generate matched instrumental (hybrid approach)
            instrumental = self.generate_instrumental_matched(vocals, genre)
            
            # 3. Mix
            output_path = self.mix_audio(vocals, instrumental)
            
            # 4. Get metadata
            vocal_bpm = self.detect_bpm(vocals, BARK_SAMPLE_RATE)
            duration = len(vocals) / BARK_SAMPLE_RATE
            
            return {
                "audio_path": output_path,
                "bpm": vocal_bpm,
                "duration": duration,
                "word": word,
                "genre": genre
            }
            
        except Exception as e:
            logger.error(f"Song generation failed: {e}")
            raise

8. SETUP SCRIPT
scripts/setup.sh
bash#!/bin/bash

echo "=== Rhyme-to-Rap Backend Setup ==="

# 1. Install system dependencies
echo "Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y ffmpeg libsndfile1 rubberband-cli

# 2. Create directories
echo "Creating directories..."
mkdir -p beats/{hip-hop,trap,lofi,rnb}
mkdir -p outputs
mkdir -p temp

# 3. Install Python dependencies
echo "Installing Python packages..."
pip install -r requirements.txt

# 4. Download NLTK data
echo "Downloading NLTK data..."
python -c "import nltk; nltk.download('cmudict')"

# 5 Setup gemini api key

# 6. Scan beats directory
echo "Initializing beat library..."
python -c "from app.utils.beat_manager import BeatLibraryManager; BeatLibraryManager().scan_beats_directory()"

echo "=== Setup Complete! ==="
echo "Next steps:"
echo "1. Add beat WAV files to beats/ directory"
echo "2. Run: python scripts/download_beats.py (optional)"
echo "3. Start server: uvicorn app.main:app --reload"

9. QUICK START CHECKLIST
markdown□ Install Python 3.10+
□ Install ffmpeg: `sudo apt-get install ffmpeg`
□ Install rubberband: `sudo apt-get install rubberband-cli`
□ Clone/create project structure
□ Run: `pip install -r requirements.txt`
□ Download free beats from:
  □ Looperman.com
  □ YouTube Audio Library
  □ FreeSoundEffects.com
□ Organize beats in beats/{genre}/ folders
□ Run: Beat library scan
□ Test: Generate first song!
'''

