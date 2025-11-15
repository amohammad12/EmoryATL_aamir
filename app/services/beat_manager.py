"""
Beat library manager for organizing and selecting pirate-themed instrumental loops
"""
import json
import librosa
import logging
from pathlib import Path
from typing import Dict, List, Optional
from app.config import settings

logger = logging.getLogger(__name__)


class BeatLibraryManager:
    """Manage pre-made beat loops library"""

    def __init__(self, beats_dir: str = None):
        """
        Initialize beat library manager

        Args:
            beats_dir: Directory containing beat files (defaults to settings.BEATS_DIR)
        """
        self.beats_dir = Path(beats_dir) if beats_dir else settings.BEATS_DIR
        self.beats_dir.mkdir(exist_ok=True)

        # Create pirate-shanty subdirectory
        self.pirate_dir = self.beats_dir / "pirate-shanty"
        self.pirate_dir.mkdir(exist_ok=True)

        self.catalog_file = self.beats_dir / "catalog.json"
        self.catalog = self._load_catalog()

    def _load_catalog(self) -> Dict:
        """
        Load beat catalog from JSON

        Returns:
            Dictionary of beat metadata
        """
        if self.catalog_file.exists():
            try:
                with open(self.catalog_file, 'r') as f:
                    catalog = json.load(f)
                    logger.info(f"Loaded beat catalog with {sum(len(beats) for beats in catalog.values())} beats")
                    return catalog
            except Exception as e:
                logger.error(f"Error loading catalog: {e}")
                return {}
        return {}

    def _save_catalog(self):
        """Save beat catalog to JSON"""
        try:
            with open(self.catalog_file, 'w') as f:
                json.dump(self.catalog, f, indent=2)
            logger.info(f"Saved beat catalog to {self.catalog_file}")
        except Exception as e:
            logger.error(f"Error saving catalog: {e}")

    def scan_beats_directory(self):
        """
        Scan directory and auto-detect BPM for all beats
        """
        logger.info("Scanning beats directory...")

        for genre_dir in self.beats_dir.iterdir():
            if not genre_dir.is_dir() or genre_dir.name.startswith('.') or genre_dir.name == '__pycache__':
                continue

            genre = genre_dir.name
            if genre not in self.catalog:
                self.catalog[genre] = []

            # Scan for WAV files
            for beat_file in genre_dir.glob("*.wav"):
                # Check if already in catalog
                if any(b['filename'] == beat_file.name for b in self.catalog[genre]):
                    logger.debug(f"Skipping already cataloged beat: {beat_file.name}")
                    continue

                # Detect BPM
                try:
                    logger.info(f"Analyzing {beat_file.name}...")
                    y, sr = librosa.load(str(beat_file))
                    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

                    beat_info = {
                        'filename': beat_file.name,
                        'path': str(beat_file.absolute()),
                        'bpm': float(tempo),
                        'duration': len(y) / sr
                    }

                    self.catalog[genre].append(beat_info)
                    duration_sec = float(len(y) / sr)
                    logger.info(f"Added {beat_file.name}: {tempo:.1f} BPM, {duration_sec:.1f}s")

                except Exception as e:
                    logger.error(f"Error processing {beat_file}: {e}")

        self._save_catalog()
        total_beats = sum(len(beats) for beats in self.catalog.values())
        logger.info(f"Catalog updated: {total_beats} beats across {len(self.catalog)} genres")

    def find_closest_beat(
        self,
        target_bpm: float,
        genre: str = "pirate-shanty",
        tolerance: float = 15.0
    ) -> Optional[Dict]:
        """
        Find beat with closest BPM to target

        Args:
            target_bpm: Target BPM to match
            genre: Preferred genre (default: pirate-shanty)
            tolerance: Maximum BPM difference allowed

        Returns:
            Beat metadata dictionary or None if no suitable beat found
        """
        logger.info(f"Finding beat for {target_bpm} BPM in genre '{genre}'")

        # Try preferred genre first
        if genre in self.catalog and self.catalog[genre]:
            beats = self.catalog[genre]
        else:
            # Fall back to any genre
            logger.warning(f"Genre '{genre}' not found, searching all genres")
            all_beats = []
            for g in self.catalog.values():
                all_beats.extend(g)

            if not all_beats:
                logger.error("No beats found in catalog!")
                return None

            beats = all_beats

        # Find closest match
        closest = min(
            beats,
            key=lambda b: abs(b['bpm'] - target_bpm)
        )

        # Check tolerance
        bpm_diff = abs(closest['bpm'] - target_bpm)
        if bpm_diff <= tolerance:
            logger.info(f"Found beat: {closest['filename']} ({closest['bpm']:.1f} BPM, diff: {bpm_diff:.1f})")
            return closest
        else:
            logger.warning(f"Closest beat is {bpm_diff:.1f} BPM away, exceeds tolerance of {tolerance}")
            return None

    def get_beat_path(self, genre: str, bpm: float) -> Optional[str]:
        """
        Get path to beat file

        Args:
            genre: Music genre
            bpm: Target BPM

        Returns:
            Path to beat file or None
        """
        beat = self.find_closest_beat(bpm, genre)
        return beat['path'] if beat else None

    def list_all_beats(self) -> Dict[str, List[Dict]]:
        """
        List all beats in catalog

        Returns:
            Complete catalog dictionary
        """
        return self.catalog

    def add_beat_manual(
        self,
        filepath: str,
        genre: str,
        bpm: float
    ):
        """
        Manually add a beat to catalog

        Args:
            filepath: Path to beat file
            genre: Genre/category
            bpm: BPM of the beat
        """
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

        logger.info(f"Manually added beat: {beat_info['filename']} at {bpm} BPM")
