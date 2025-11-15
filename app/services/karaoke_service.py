"""
Karaoke timing service using aeneas for word-level synchronization
"""
import uuid
import logging
from pathlib import Path
from typing import List, Dict
from aeneas.executetask import ExecuteTask
from aeneas.task import Task
from app.config import settings

logger = logging.getLogger(__name__)


class KaraokeGenerator:
    """Generate word-level timestamps for karaoke highlighting"""

    def __init__(self):
        """Initialize karaoke generator"""
        self.temp_dir = settings.TEMP_DIR

    def generate_word_timings(
        self,
        audio_path: str,
        lyrics: str
    ) -> List[Dict[str, any]]:
        """
        Generate word-by-word timestamps using aeneas forced alignment

        Args:
            audio_path: Path to audio file
            lyrics: Lyrics text

        Returns:
            List of timing dictionaries:
            [
                {"word": "cat", "start": 0.5, "end": 0.8},
                {"word": "sat", "start": 1.0, "end": 1.3},
                ...
            ]
        """
        try:
            logger.info(f"Generating karaoke timings for {audio_path}")

            # Clean lyrics for alignment
            clean_lyrics = self._clean_lyrics_for_alignment(lyrics)

            # Create temporary text file
            text_file = self.temp_dir / f"lyrics_{uuid.uuid4()}.txt"
            with open(text_file, 'w', encoding='utf-8') as f:
                f.write(clean_lyrics)

            # Create temporary sync map file
            sync_map_file = self.temp_dir / f"syncmap_{uuid.uuid4()}.json"

            # Configure aeneas task
            config_string = "task_language=eng|is_text_type=plain|os_task_file_format=json"

            # Create and execute task
            task = Task(config_string=config_string)
            task.audio_file_path_absolute = audio_path
            task.text_file_path_absolute = str(text_file)
            task.sync_map_file_path_absolute = str(sync_map_file)

            logger.info("Running aeneas forced alignment...")
            ExecuteTask(task).execute()

            # Parse sync map
            task.output_sync_map_file()

            # Extract timings
            timings = []
            for fragment in task.sync_map_leaves():
                timings.append({
                    "word": fragment.text,
                    "start": float(fragment.begin),
                    "end": float(fragment.end)
                })

            # Cleanup temporary files
            text_file.unlink(missing_ok=True)
            sync_map_file.unlink(missing_ok=True)

            logger.info(f"Generated {len(timings)} word timings")

            return timings

        except Exception as e:
            logger.error(f"Error generating karaoke timings: {e}")
            # Return fallback simple timing
            return self._generate_fallback_timings(lyrics)

    def _clean_lyrics_for_alignment(self, lyrics: str) -> str:
        """
        Clean lyrics for aeneas alignment
        Remove structure labels and pirate vocalizations

        Args:
            lyrics: Raw lyrics text

        Returns:
            Cleaned lyrics text with one word per line
        """
        # Remove structure labels
        lyrics = lyrics.replace('Verse 1:', '')
        lyrics = lyrics.replace('Verse 2:', '')
        lyrics = lyrics.replace('Chorus:', '')

        # Remove pirate vocalizations (they'll be in parentheses)
        import re
        lyrics = re.sub(r'\([^)]*\)', '', lyrics)

        # Split into words
        words = lyrics.split()

        # Join with newlines (one word per line for better alignment)
        clean_lyrics = '\n'.join(words)

        logger.debug(f"Cleaned lyrics:\n{clean_lyrics}")

        return clean_lyrics

    def _generate_fallback_timings(self, lyrics: str) -> List[Dict[str, any]]:
        """
        Generate simple fallback timings if aeneas fails
        Assumes even distribution of words over 30 seconds

        Args:
            lyrics: Lyrics text

        Returns:
            List of simple timing dictionaries
        """
        logger.warning("Using fallback timing generation")

        # Clean lyrics
        clean_lyrics = self._clean_lyrics_for_alignment(lyrics)
        words = clean_lyrics.split()

        # Assume 30 second duration
        duration = 30.0
        word_duration = duration / len(words) if words else 1.0

        timings = []
        current_time = 0.0

        for word in words:
            timings.append({
                "word": word.strip(),
                "start": current_time,
                "end": current_time + word_duration
            })
            current_time += word_duration

        logger.info(f"Generated {len(timings)} fallback timings")

        return timings
