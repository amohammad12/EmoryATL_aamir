"""
Background Music Service - Manages custom background tracks
"""
import random
import logging
from pathlib import Path
from typing import Optional
from pydub import AudioSegment

from app.config import settings

logger = logging.getLogger(__name__)


class BackgroundMusicManager:
    """Manages selection and trimming of custom background music tracks"""

    def __init__(self):
        """Initialize background music manager"""
        self.music_dir = settings.BACKGROUND_MUSIC_DIR
        self.supported_formats = ['.mp3', '.wav', '.m4a', '.ogg', '.flac']

    def get_available_tracks(self) -> list[Path]:
        """
        Get list of available background music tracks

        Returns:
            List of Path objects for available tracks
        """
        tracks = []

        if not self.music_dir.exists():
            logger.warning(f"Background music directory not found: {self.music_dir}")
            return tracks

        for ext in self.supported_formats:
            tracks.extend(self.music_dir.glob(f'*{ext}'))

        logger.info(f"Found {len(tracks)} background music tracks")
        return tracks

    def select_random_track(self) -> Optional[Path]:
        """
        Randomly select a background music track

        Returns:
            Path to selected track, or None if no tracks available
        """
        tracks = self.get_available_tracks()

        if not tracks:
            logger.error("No background music tracks found!")
            return None

        selected = random.choice(tracks)
        logger.info(f"Selected background track: {selected.name}")
        return selected

    def trim_to_duration(
        self,
        track_path: Path,
        target_duration: float,
        fade_out_duration: float = 1.0
    ) -> AudioSegment:
        """
        Load and trim background track to target duration

        Args:
            track_path: Path to music track
            target_duration: Target duration in seconds
            fade_out_duration: Duration of fade-out in seconds (default: 1.0)

        Returns:
            AudioSegment trimmed to target duration
        """
        try:
            # Load audio file
            logger.info(f"Loading background track: {track_path.name}")

            # Detect format from extension
            file_format = track_path.suffix[1:]  # Remove the dot
            if file_format == 'm4a':
                file_format = 'mp4'  # pydub uses 'mp4' for m4a

            background = AudioSegment.from_file(str(track_path), format=file_format)

            # Get duration in milliseconds
            target_ms = int(target_duration * 1000)
            fade_out_ms = int(fade_out_duration * 1000)

            # If track is shorter than target, loop it
            if len(background) < target_ms:
                logger.info(f"Track is shorter than target. Looping...")
                times_to_loop = (target_ms // len(background)) + 1
                background = background * times_to_loop

            # Trim to exact duration
            trimmed = background[:target_ms]

            # Apply fade-out at the end
            if fade_out_ms > 0 and len(trimmed) > fade_out_ms:
                trimmed = trimmed.fade_out(fade_out_ms)

            logger.info(f"Trimmed track to {target_duration:.2f}s with {fade_out_duration}s fade-out")
            return trimmed

        except Exception as e:
            logger.error(f"Error processing background track: {e}")
            raise

    def get_random_background(
        self,
        target_duration: float,
        fade_out_duration: float = 1.0
    ) -> Optional[AudioSegment]:
        """
        Get a random background track trimmed to target duration

        Args:
            target_duration: Target duration in seconds
            fade_out_duration: Duration of fade-out in seconds

        Returns:
            AudioSegment ready to mix, or None if no tracks available
        """
        try:
            # Select random track
            track_path = self.select_random_track()

            if not track_path:
                logger.warning("No background tracks available")
                return None

            # Trim to duration
            background = self.trim_to_duration(
                track_path,
                target_duration,
                fade_out_duration
            )

            return background

        except Exception as e:
            logger.error(f"Error getting random background: {e}")
            return None

    def validate_tracks(self) -> dict:
        """
        Validate all background tracks

        Returns:
            Dictionary with validation results
        """
        tracks = self.get_available_tracks()

        results = {
            'total_tracks': len(tracks),
            'valid_tracks': [],
            'invalid_tracks': [],
            'missing_directory': not self.music_dir.exists()
        }

        if results['missing_directory']:
            logger.error(f"Background music directory missing: {self.music_dir}")
            return results

        for track in tracks:
            try:
                # Try to load the track
                file_format = track.suffix[1:]
                if file_format == 'm4a':
                    file_format = 'mp4'

                audio = AudioSegment.from_file(str(track), format=file_format)

                results['valid_tracks'].append({
                    'name': track.name,
                    'duration': len(audio) / 1000,  # Convert to seconds
                    'format': track.suffix,
                    'size_mb': track.stat().st_size / (1024 * 1024)
                })

            except Exception as e:
                results['invalid_tracks'].append({
                    'name': track.name,
                    'error': str(e)
                })

        logger.info(f"Validation: {len(results['valid_tracks'])} valid, "
                   f"{len(results['invalid_tracks'])} invalid")

        return results
