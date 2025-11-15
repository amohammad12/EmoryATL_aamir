"""
Vocal generation service using Bark TTS (Expressive Singing AI)
"""
import asyncio
import uuid
import logging
import numpy as np
import scipy.io.wavfile as wavfile
from pathlib import Path
from pydub import AudioSegment
from transformers import AutoProcessor, BarkModel
import torch
from typing import Optional
from app.config import settings

logger = logging.getLogger(__name__)


class BarkModelCache:
    """Singleton cache for Bark model to avoid reloading"""
    _instance = None
    _model = None
    _processor = None
    _device = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_model_and_processor(self):
        """Load and cache Bark model and processor"""
        if self._model is None or self._processor is None:
            logger.info(f"Loading Bark model: {settings.BARK_MODEL}")

            # Load processor
            self._processor = AutoProcessor.from_pretrained(settings.BARK_MODEL)

            # Load model
            self._model = BarkModel.from_pretrained(
                settings.BARK_MODEL,
                torch_dtype=torch.float16 if settings.BARK_USE_GPU else torch.float32
            )

            # Move to GPU if available and enabled
            if settings.BARK_USE_GPU and torch.cuda.is_available():
                self._device = "cuda"
                self._model = self._model.to(self._device)
                logger.info("Bark model loaded on GPU (CUDA)")
            else:
                self._device = "cpu"
                self._model = self._model.to(self._device)
                logger.info("Bark model loaded on CPU")

            logger.info("Bark model and processor loaded successfully")

        return self._model, self._processor, self._device


class VocalGenerator:
    """Generate expressive singing vocals using Bark TTS"""

    def __init__(self):
        """Initialize Bark TTS with cached model"""
        self.voice_preset = settings.BARK_VOICE_PRESET
        self.singing_mode = settings.BARK_SINGING_MODE
        self.sample_rate = settings.SAMPLE_RATE

        # Get cached model, processor, and device
        cache = BarkModelCache()
        self.model, self.processor, self.device = cache.get_model_and_processor()

        logger.info(f"VocalGenerator initialized with voice: {self.voice_preset} on device: {self.device}")

    async def generate_vocals_async(
        self,
        lyrics: str,
        output_path: str = None
    ) -> str:
        """
        Generate vocals using Bark TTS (async wrapper)

        Args:
            lyrics: The lyrics text
            output_path: Optional output path (generates unique if not provided)

        Returns:
            Path to generated audio file (MP3)
        """
        # Run in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._generate_vocals_sync, lyrics, output_path)

    def generate_vocals(self, lyrics: str, output_path: str = None) -> str:
        """
        Synchronous vocal generation

        Args:
            lyrics: The lyrics text
            output_path: Optional output path

        Returns:
            Path to generated audio file (MP3)
        """
        return self._generate_vocals_sync(lyrics, output_path)

    def _generate_vocals_sync(self, lyrics: str, output_path: Optional[str] = None) -> str:
        """
        Internal synchronous generation method

        Args:
            lyrics: The lyrics text
            output_path: Optional output path

        Returns:
            Path to generated MP3 file
        """
        try:
            # Generate unique filename if not provided
            if output_path is None:
                filename = f"vocals_{uuid.uuid4()}.mp3"
                output_path = str(settings.TEMP_DIR / filename)

            # Ensure output is MP3
            if not output_path.endswith('.mp3'):
                output_path = output_path.replace('.wav', '.mp3')

            logger.info(f"Generating vocals with Bark TTS to {output_path}")

            # Format lyrics for singing mode
            formatted_lyrics = self._format_for_singing(lyrics)

            logger.debug(f"Formatted lyrics: {formatted_lyrics[:200]}...")

            # Prepare inputs
            inputs = self.processor(
                formatted_lyrics,
                voice_preset=self.voice_preset,
                return_tensors="pt"
            )

            # Move inputs to same device as model
            inputs = {k: v.to(self.device) for k, v in inputs.items()}

            # Generate audio with optimized parameters
            with torch.no_grad():
                audio_array = self.model.generate(
                    **inputs,
                    semantic_temperature=settings.BARK_SEMANTIC_TEMP,
                    coarse_temperature=settings.BARK_COARSE_TEMP,
                    fine_temperature=settings.BARK_FINE_TEMP,
                    do_sample=True
                )

            # Convert to numpy array
            audio_array = audio_array.cpu().numpy().squeeze()

            # Get sample rate from model config
            sample_rate = self.model.generation_config.sample_rate

            # Save as WAV first (temporary)
            temp_wav = output_path.replace('.mp3', '_temp.wav')

            # Ensure audio is in correct format for WAV
            if audio_array.dtype != np.int16:
                # Normalize to [-1, 1] then convert to int16
                audio_array = np.clip(audio_array, -1.0, 1.0)
                audio_array = (audio_array * 32767).astype(np.int16)

            wavfile.write(temp_wav, rate=sample_rate, data=audio_array)

            # Convert WAV to MP3 using pydub
            audio_segment = AudioSegment.from_wav(temp_wav)

            # Resample to target sample rate if needed
            if sample_rate != settings.SAMPLE_RATE:
                audio_segment = audio_segment.set_frame_rate(settings.SAMPLE_RATE)

            # Export as MP3
            audio_segment.export(output_path, format="mp3", bitrate="192k")

            # Clean up temporary WAV file
            Path(temp_wav).unlink(missing_ok=True)

            logger.info(f"Vocals generated successfully: {output_path}")

            return output_path

        except Exception as e:
            logger.error(f"Error generating vocals with Bark: {e}", exc_info=True)
            raise

    def _format_for_singing(self, lyrics: str) -> str:
        """
        Format lyrics for Bark's singing mode
        Adds musical notations and structures lyrics for singing

        Args:
            lyrics: Raw lyrics text

        Returns:
            Formatted lyrics ready for Bark singing
        """
        import re

        # First, clean the lyrics (remove structure labels)
        cleaned = self._add_shanty_rhythm(lyrics)

        if not self.singing_mode:
            # If not singing mode, return cleaned lyrics as-is
            return cleaned

        # Add singing indicators for Bark
        # Bark understands musical notations in the text
        lines = cleaned.split('\n')
        formatted_lines = []

        for line in lines:
            line = line.strip()
            if not line:
                formatted_lines.append('')
                continue

            # Add musical notation for shanty lines
            # The ♪ symbol helps Bark understand it should be sung
            if any(word in line.lower() for word in ['arr', 'yo-ho', 'ahoy', 'avast', 'heave']):
                # Pirate exclamations - make them energetic
                formatted_line = f"♪ {line} ♪"
            elif line.endswith('!'):
                # Exclamatory lines - sung with emphasis
                formatted_line = f"♪ {line}"
            else:
                # Regular verse lines - smooth singing
                formatted_line = f"♪ {line}"

            formatted_lines.append(formatted_line)

        # Join with proper spacing
        formatted = '\n'.join(formatted_lines)

        # Add singing context at the beginning (helps Bark understand style)
        formatted = f"[singing a pirate sea shanty]\n{formatted}"

        logger.debug(f"Formatted for singing:\n{formatted}")

        return formatted

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
        cleaned = re.sub(r'Bridge:\s*', '', cleaned)
        cleaned = re.sub(r'Outro:\s*', '', cleaned)

        # Remove parentheses from pirate vocalizations but keep the words
        pirate_words = ['arr', 'Arr', 'yo-ho', 'Yo-ho', 'ahoy', 'Ahoy',
                       'avast', 'Avast', 'heave', 'Heave', 'shiver']

        for word in pirate_words:
            cleaned = cleaned.replace(f'({word}!)', f'{word}!')
            cleaned = cleaned.replace(f'({word.capitalize()}!)', f'{word.capitalize()}!')

        # Clean up excessive blank lines
        cleaned = re.sub(r'\n\s*\n\s*\n', '\n\n', cleaned)

        logger.debug(f"Cleaned lyrics for TTS:\n{cleaned}")

        return cleaned.strip()
