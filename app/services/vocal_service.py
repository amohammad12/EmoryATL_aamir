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
        Add SSML markers for sea shanty rhythm
        Makes it sound more musical and fun for kids

        Args:
            lyrics: Raw lyrics text

        Returns:
            SSML-formatted lyrics with pauses and emphasis
        """
        # Split into lines
        lines = lyrics.split('\n')
        formatted_lines = []

        for line in lines:
            # Skip empty lines
            if not line.strip():
                formatted_lines.append(line)
                continue

            # Add pauses after pirate vocalizations
            line = line.replace('(arr!)', '<break time="300ms"/>arr!<break time="300ms"/>')
            line = line.replace('(Arr!)', '<break time="300ms"/>Arr!<break time="300ms"/>')
            line = line.replace('(yo-ho!)', '<break time="300ms"/>yo-ho!<break time="300ms"/>')
            line = line.replace('(Yo-ho!)', '<break time="300ms"/>Yo-ho!<break time="300ms"/>')
            line = line.replace('(ahoy!)', '<break time="300ms"/>ahoy!<break time="300ms"/>')
            line = line.replace('(Ahoy!)', '<break time="300ms"/>Ahoy!<break time="300ms"/>')
            line = line.replace('(avast!)', '<break time="300ms"/>avast!<break time="300ms"/>')
            line = line.replace('(Avast!)', '<break time="300ms"/>Avast!<break time="300ms"/>')

            # Add emphasis and pitch increase for chorus sections
            if 'Chorus:' in line:
                line = line.replace('Chorus:', '<prosody pitch="+10%" volume="+20%">Chorus:</prosody>')
            elif 'Verse' in line:
                line = line.replace('Verse 1:', 'Verse 1:')
                line = line.replace('Verse 2:', 'Verse 2:')

            # Add slight pause at end of each line for better rhythm
            if line.strip() and not line.endswith('</prosody>'):
                line += '<break time="200ms"/>'

            formatted_lines.append(line)

        result = '\n'.join(formatted_lines)

        logger.debug(f"Formatted lyrics with SSML:\n{result}")

        return result
