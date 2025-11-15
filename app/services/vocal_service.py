"""
Vocal generation service using Edge TTS (100% FREE!)
"""
import edge_tts
import asyncio
import uuid
import logging
from pathlib import Path
from app.config import settings

logger = logging.getLogger(__name__)


class VocalGenerator:
    """Generate vocals using Microsoft Edge TTS (Free!)"""

    def __init__(self):
        """Initialize Edge TTS with kid-friendly voice"""
        self.voice = settings.TTS_VOICE  # Default: en-US-JennyNeural
        self.rate = settings.TTS_RATE    # Default: -10% (slightly slower)
        self.pitch = settings.TTS_PITCH  # Default: +5Hz (slightly higher)

    async def generate_vocals_async(
        self,
        lyrics: str,
        output_path: str = None
    ) -> str:
        """
        Generate vocals using Edge TTS (async)

        Args:
            lyrics: The lyrics text
            output_path: Optional output path (generates unique if not provided)

        Returns:
            Path to generated audio file
        """
        try:
            # Generate unique filename if not provided
            if output_path is None:
                filename = f"vocals_{uuid.uuid4()}.mp3"
                output_path = str(settings.TEMP_DIR / filename)

            logger.info(f"Generating vocals with Edge TTS to {output_path}")

            # Add SSML markers for pirate shanty rhythm
            formatted_lyrics = self._add_shanty_rhythm(lyrics)

            # Generate speech with Edge TTS
            communicate = edge_tts.Communicate(
                formatted_lyrics,
                self.voice,
                rate=self.rate,
                pitch=self.pitch
            )

            # Save audio
            await communicate.save(output_path)

            logger.info(f"Vocals generated successfully: {output_path}")

            return output_path

        except Exception as e:
            logger.error(f"Error generating vocals: {e}")
            raise

    def generate_vocals(self, lyrics: str, output_path: str = None) -> str:
        """
        Synchronous wrapper for vocal generation

        Args:
            lyrics: The lyrics text
            output_path: Optional output path

        Returns:
            Path to generated audio file
        """
        return asyncio.run(self.generate_vocals_async(lyrics, output_path))

    def _add_shanty_rhythm(self, lyrics: str) -> str:
        """
        Clean and format lyrics for TTS
        Removes structure labels and formats pirate vocalizations

        Args:
            lyrics: Raw lyrics text

        Returns:
            Cleaned lyrics ready for TTS
        """
        import re

        # Remove structure labels (Verse 1:, Chorus:, etc.)
        cleaned = re.sub(r'Verse \d+:\s*', '', lyrics)
        cleaned = re.sub(r'Chorus:\s*', '', cleaned)

        # Remove parentheses from pirate vocalizations but keep the words
        cleaned = cleaned.replace('(arr!)', 'arr!')
        cleaned = cleaned.replace('(Arr!)', 'Arr!')
        cleaned = cleaned.replace('(yo-ho!)', 'yo-ho!')
        cleaned = cleaned.replace('(Yo-ho!)', 'Yo-ho!')
        cleaned = cleaned.replace('(ahoy!)', 'ahoy!')
        cleaned = cleaned.replace('(Ahoy!)', 'Ahoy!')
        cleaned = cleaned.replace('(avast!)', 'avast!')
        cleaned = cleaned.replace('(Avast!)', 'Avast!')

        # Clean up excessive blank lines
        cleaned = re.sub(r'\n\s*\n\s*\n', '\n\n', cleaned)

        logger.debug(f"Cleaned lyrics for TTS:\n{cleaned}")

        return cleaned.strip()
