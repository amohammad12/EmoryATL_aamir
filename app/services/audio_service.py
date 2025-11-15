"""
Audio processing service for mixing vocals and instrumentals
"""
import librosa
import soundfile as sf
import numpy as np
import uuid
import logging
from pathlib import Path
from pydub import AudioSegment
from typing import Optional
from app.config import settings
from app.services.beat_manager import BeatLibraryManager

logger = logging.getLogger(__name__)


class AudioService:
    """Handle audio processing, BPM detection, and mixing"""

    def __init__(self):
        """Initialize audio service"""
        self.sample_rate = settings.SAMPLE_RATE
        self.output_dir = settings.OUTPUT_DIR
        self.temp_dir = settings.TEMP_DIR
        self.beat_manager = BeatLibraryManager()

    def detect_bpm(self, audio_path: str) -> float:
        """
        Detect BPM from audio file

        Args:
            audio_path: Path to audio file

        Returns:
            BPM as float
        """
        try:
            y, sr = librosa.load(audio_path)
            tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
            bpm = float(tempo)

            logger.info(f"Detected BPM: {bpm:.1f} from {audio_path}")

            return bpm

        except Exception as e:
            logger.warning(f"BPM detection failed: {e}, using default 95 BPM")
            return 95.0  # Default pirate shanty tempo

    def get_audio_duration(self, audio_path: str) -> float:
        """
        Get duration of audio file in seconds

        Args:
            audio_path: Path to audio file

        Returns:
            Duration in seconds
        """
        try:
            y, sr = librosa.load(audio_path)
            duration = len(y) / sr

            logger.info(f"Audio duration: {duration:.2f}s")

            return duration

        except Exception as e:
            logger.error(f"Error getting audio duration: {e}")
            raise

    def get_instrumental(
        self,
        vocal_path: str,
        genre: str = "pirate-shanty"
    ) -> Optional[str]:
        """
        Get matching instrumental beat for vocals

        Args:
            vocal_path: Path to vocal audio file
            genre: Genre/category of beat

        Returns:
            Path to instrumental file or None
        """
        try:
            # Detect vocal BPM
            vocal_bpm = self.detect_bpm(vocal_path)

            logger.info(f"Finding instrumental for {vocal_bpm:.1f} BPM, genre: {genre}")

            # Constrain to pirate shanty tempo range
            if vocal_bpm < settings.PIRATE_SHANTY_BPM_MIN:
                logger.warning(f"Vocal BPM {vocal_bpm} too slow, using {settings.PIRATE_SHANTY_BPM_MIN}")
                vocal_bpm = settings.PIRATE_SHANTY_BPM_MIN
            elif vocal_bpm > settings.PIRATE_SHANTY_BPM_MAX:
                logger.warning(f"Vocal BPM {vocal_bpm} too fast, using {settings.PIRATE_SHANTY_BPM_MAX}")
                vocal_bpm = settings.PIRATE_SHANTY_BPM_MAX

            # Find matching beat
            beat_info = self.beat_manager.find_closest_beat(vocal_bpm, genre)

            if beat_info:
                logger.info(f"Selected beat: {beat_info['filename']} at {beat_info['bpm']:.1f} BPM")
                return beat_info['path']
            else:
                logger.warning("No suitable beat found in library")
                return None

        except Exception as e:
            logger.error(f"Error getting instrumental: {e}")
            return None

    def mix_audio(
        self,
        vocal_path: str,
        instrumental_path: str,
        output_filename: str = None
    ) -> str:
        """
        Mix vocals and instrumental tracks

        Args:
            vocal_path: Path to vocal audio file
            instrumental_path: Path to instrumental audio file
            output_filename: Optional output filename (generates unique if not provided)

        Returns:
            Path to output mixed audio file
        """
        try:
            logger.info(f"Mixing vocals ({vocal_path}) with instrumental ({instrumental_path})")

            # Generate output filename if not provided
            if output_filename is None:
                output_filename = f"song_{uuid.uuid4()}.mp3"

            output_path = self.output_dir / output_filename

            # Load audio files with pydub
            vocals = AudioSegment.from_file(vocal_path)
            instrumental = AudioSegment.from_file(instrumental_path)

            # Get vocal duration
            vocal_duration = len(vocals)

            # Loop instrumental to match vocal duration
            if len(instrumental) < vocal_duration:
                # Loop the instrumental
                repeats = (vocal_duration // len(instrumental)) + 1
                instrumental = instrumental * repeats

            # Trim instrumental to match vocal duration
            instrumental = instrumental[:vocal_duration]

            # Adjust volumes
            vocals_db = 20 * np.log10(settings.VOCALS_VOLUME) if settings.VOCALS_VOLUME > 0 else -60
            inst_db = 20 * np.log10(settings.INSTRUMENTAL_VOLUME) if settings.INSTRUMENTAL_VOLUME > 0 else -60

            vocals = vocals + vocals_db
            instrumental = instrumental + inst_db

            # Mix by overlaying
            mixed = vocals.overlay(instrumental)

            # Export as MP3
            mixed.export(str(output_path), format="mp3", bitrate="192k")

            logger.info(f"Mixed audio saved to {output_path}")

            return str(output_path)

        except Exception as e:
            logger.error(f"Error mixing audio: {e}")
            raise

    def time_stretch_beat(
        self,
        beat_path: str,
        original_bpm: float,
        target_bpm: float
    ) -> str:
        """
        Time-stretch a beat to match target BPM

        Args:
            beat_path: Path to beat file
            original_bpm: Original BPM of the beat
            target_bpm: Target BPM

        Returns:
            Path to stretched beat file
        """
        try:
            logger.info(f"Time-stretching beat from {original_bpm:.1f} to {target_bpm:.1f} BPM")

            # Load audio
            y, sr = librosa.load(beat_path)

            # Calculate stretch rate
            rate = target_bpm / original_bpm

            # Time-stretch using librosa
            y_stretched = librosa.effects.time_stretch(y, rate=rate)

            # Save stretched audio
            output_filename = f"stretched_{uuid.uuid4()}.wav"
            output_path = self.temp_dir / output_filename

            sf.write(str(output_path), y_stretched, sr)

            logger.info(f"Stretched beat saved to {output_path}")

            return str(output_path)

        except Exception as e:
            logger.error(f"Error time-stretching beat: {e}")
            raise
