"""
Hybrid vocal generation service using ElevenLabs (primary) + Bark (fallback)
"""
import asyncio
import uuid
import logging
import numpy as np
import scipy.io.wavfile as wavfile
from pathlib import Path
from pydub import AudioSegment
from typing import Optional
import io

from app.config import settings

logger = logging.getLogger(__name__)

# Try to import ElevenLabs
try:
    from elevenlabs import ElevenLabs
    ELEVENLABS_AVAILABLE = True
except ImportError:
    ELEVENLABS_AVAILABLE = False
    logger.warning("ElevenLabs not available - will use Bark only")

# Try to import Bark
try:
    from transformers import AutoProcessor, BarkModel
    import torch
    BARK_AVAILABLE = True
except ImportError:
    BARK_AVAILABLE = False
    logger.warning("Bark not available")


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
        if not BARK_AVAILABLE:
            raise ImportError("Bark dependencies not installed")

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
    """
    Hybrid TTS generator using ElevenLabs as primary and Bark as fallback
    """

    def __init__(self):
        """Initialize TTS providers"""
        self.provider = settings.TTS_PROVIDER
        self.fallback_enabled = settings.TTS_FALLBACK_TO_BARK

        # Initialize ElevenLabs if available and configured
        self.elevenlabs_client = None
        self.elevenlabs_available = False
        if ELEVENLABS_AVAILABLE and settings.ELEVENLABS_API_KEY:
            try:
                self.elevenlabs_client = ElevenLabs(api_key=settings.ELEVENLABS_API_KEY)
                self.elevenlabs_available = True
                logger.info("ElevenLabs TTS initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize ElevenLabs: {e}")
                if not self.fallback_enabled:
                    raise

        # Initialize Bark if needed
        self.bark_model = None
        self.bark_processor = None
        self.bark_device = None

        if BARK_AVAILABLE and (self.provider == "bark" or self.fallback_enabled or not self.elevenlabs_available):
            try:
                cache = BarkModelCache()
                self.bark_model, self.bark_processor, self.bark_device = cache.get_model_and_processor()
                logger.info("Bark TTS initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Bark: {e}")
                if not self.elevenlabs_available:
                    raise

        logger.info(f"VocalGenerator initialized: Primary={self.provider}, Fallback={self.fallback_enabled}")

    async def generate_vocals_async(
        self,
        lyrics: str,
        output_path: str = None
    ) -> str:
        """
        Generate vocals using TTS (async wrapper)

        Args:
            lyrics: The lyrics text
            output_path: Optional output path (generates unique if not provided)

        Returns:
            Path to generated audio file (MP3)
        """
        # Run in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.generate_vocals, lyrics, output_path)

    def generate_vocals(self, lyrics: str, output_path: str = None) -> str:
        """
        Synchronous vocal generation with automatic fallback

        Args:
            lyrics: The lyrics text
            output_path: Optional output path

        Returns:
            Path to generated audio file (MP3)
        """
        # Generate unique filename if not provided
        if output_path is None:
            filename = f"vocals_{uuid.uuid4()}.mp3"
            output_path = str(settings.TEMP_DIR / filename)

        # Ensure output is MP3
        if not output_path.endswith('.mp3'):
            output_path = output_path.replace('.wav', '.mp3')

        # Clean lyrics
        cleaned_lyrics = self._clean_lyrics(lyrics)

        # Try primary provider
        try:
            if self.provider == "elevenlabs" and self.elevenlabs_available:
                logger.info("Generating vocals with ElevenLabs...")
                return self._generate_with_elevenlabs(cleaned_lyrics, output_path)
            elif self.provider == "bark" and self.bark_model:
                logger.info("Generating vocals with Bark...")
                return self._generate_with_bark(cleaned_lyrics, output_path)
            else:
                raise ValueError(f"Provider '{self.provider}' not available")

        except Exception as e:
            logger.error(f"Primary TTS provider failed: {e}")

            # Try fallback
            if self.fallback_enabled:
                logger.warning("Falling back to alternative TTS provider...")
                try:
                    if self.provider == "elevenlabs" and self.bark_model:
                        logger.info("Falling back to Bark...")
                        return self._generate_with_bark(cleaned_lyrics, output_path)
                    elif self.provider == "bark" and self.elevenlabs_available:
                        logger.info("Falling back to ElevenLabs...")
                        return self._generate_with_elevenlabs(cleaned_lyrics, output_path)
                except Exception as fallback_error:
                    logger.error(f"Fallback also failed: {fallback_error}")
                    raise Exception(f"Both TTS providers failed. Primary: {e}, Fallback: {fallback_error}")
            else:
                raise

    def _generate_with_elevenlabs(self, lyrics: str, output_path: str) -> str:
        """Generate vocals using ElevenLabs API (v2 SDK)"""
        try:
            # Format lyrics for better rhythm and musicality
            formatted_lyrics = self._format_for_elevenlabs(lyrics)

            # Generate audio using v2 client API
            response = self.elevenlabs_client.text_to_speech.convert(
                text=formatted_lyrics,
                voice_id=settings.ELEVENLABS_VOICE_ID,
                model_id=settings.ELEVENLABS_MODEL,
                voice_settings={
                    "stability": settings.ELEVENLABS_STABILITY,
                    "similarity_boost": settings.ELEVENLABS_SIMILARITY,
                    "style": settings.ELEVENLABS_STYLE,
                    "use_speaker_boost": settings.ELEVENLABS_BOOST
                }
            )

            # Collect audio bytes from generator
            audio_bytes = b''
            for chunk in response:
                audio_bytes += chunk

            # Convert to AudioSegment
            audio = AudioSegment.from_file(io.BytesIO(audio_bytes), format="mp3")

            # Apply post-processing
            audio = self._enhance_audio(audio)

            # Export as MP3
            audio.export(output_path, format="mp3", bitrate="192k")

            logger.info(f"ElevenLabs vocals generated successfully: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"ElevenLabs generation failed: {e}")
            raise

    def _generate_with_bark(self, lyrics: str, output_path: str) -> str:
        """Generate vocals using Bark (with chunking optimization)"""
        try:
            # Format lyrics for teacher-style reading
            formatted_lyrics = self._format_for_bark(lyrics)

            # Split into chunks for better quality
            chunks = self._split_into_chunks(formatted_lyrics, max_length=200)

            logger.info(f"Split lyrics into {len(chunks)} chunks for Bark")

            # Generate audio for each chunk
            audio_segments = []
            sample_rate = self.bark_model.generation_config.sample_rate

            for i, chunk in enumerate(chunks):
                logger.debug(f"Generating chunk {i+1}/{len(chunks)}")

                # Prepare inputs
                inputs = self.bark_processor(
                    chunk,
                    voice_preset=settings.BARK_VOICE_PRESET,
                    return_tensors="pt"
                )

                # Move inputs to same device as model
                inputs = {k: v.to(self.bark_device) for k, v in inputs.items()}

                # Generate audio
                with torch.no_grad():
                    audio_array = self.bark_model.generate(
                        **inputs,
                        semantic_temperature=settings.BARK_SEMANTIC_TEMP,
                        coarse_temperature=settings.BARK_COARSE_TEMP,
                        fine_temperature=settings.BARK_FINE_TEMP,
                        do_sample=True
                    )

                # Convert to numpy array
                audio_array = audio_array.cpu().numpy().squeeze()

                # Convert to AudioSegment
                if audio_array.dtype != np.int16:
                    audio_array = np.clip(audio_array, -1.0, 1.0)
                    audio_array = (audio_array * 32767).astype(np.int16)

                # Create temporary file
                temp_chunk_wav = str(settings.TEMP_DIR / f"chunk_{i}_{uuid.uuid4()}.wav")
                wavfile.write(temp_chunk_wav, rate=sample_rate, data=audio_array)

                # Load as AudioSegment
                chunk_audio = AudioSegment.from_wav(temp_chunk_wav)

                # Add pause between chunks
                if i < len(chunks) - 1:
                    silence = AudioSegment.silent(duration=300)
                    chunk_audio = chunk_audio + silence

                audio_segments.append(chunk_audio)

                # Cleanup
                Path(temp_chunk_wav).unlink(missing_ok=True)

            # Concatenate all chunks
            final_audio = sum(audio_segments)

            # Apply post-processing
            final_audio = self._enhance_audio(final_audio)

            # Resample if needed
            if sample_rate != settings.SAMPLE_RATE:
                final_audio = final_audio.set_frame_rate(settings.SAMPLE_RATE)

            # Export as MP3
            final_audio.export(output_path, format="mp3", bitrate="192k")

            logger.info(f"Bark vocals generated successfully: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Bark generation failed: {e}")
            raise

    def _clean_lyrics(self, lyrics: str) -> str:
        """Clean lyrics for TTS"""
        import re

        # Remove structure labels
        cleaned = re.sub(r'Verse \d+:\s*', '', lyrics)
        cleaned = re.sub(r'Chorus:\s*', '', cleaned)
        cleaned = re.sub(r'Bridge:\s*', '', cleaned)
        cleaned = re.sub(r'Outro:\s*', '', cleaned)

        # Remove parentheses from pirate vocalizations
        pirate_words = ['arr', 'Arr', 'yo-ho', 'Yo-ho', 'ahoy', 'Ahoy',
                       'avast', 'Avast', 'heave', 'Heave', 'shiver']

        for word in pirate_words:
            cleaned = cleaned.replace(f'({word}!)', f'{word}!')
            cleaned = cleaned.replace(f'({word.capitalize()}!)', f'{word.capitalize()}!')

        # Clean up excessive blank lines
        cleaned = re.sub(r'\n\s*\n\s*\n', '\n\n', cleaned)

        return cleaned.strip()

    def _format_for_elevenlabs(self, lyrics: str) -> str:
        """Format lyrics for ElevenLabs with musical/rhythmic cues"""
        import re

        # Add pauses at line breaks for rhythm
        formatted = re.sub(r'\n', ',\n', lyrics)

        # Add emphasis to rhyming words at end of lines (simple heuristic)
        # This helps ElevenLabs emphasize the rhymes
        lines = formatted.split('\n')
        enhanced_lines = []

        for line in lines:
            line = line.strip()
            if line:
                # Add slight pause at end of each line for rhythm
                if not line.endswith('!') and not line.endswith('?'):
                    line = line.rstrip(',') + '.'
                enhanced_lines.append(line)

        return '\n'.join(enhanced_lines)

    def _format_for_bark(self, lyrics: str) -> str:
        """Format lyrics for Bark with simple teacher prompt"""
        return f"[Teacher reading a fun pirate story to children]\n{lyrics}"

    def _split_into_chunks(self, text: str, max_length: int = 200) -> list:
        """Split text into smaller chunks for Bark"""
        # Remove context prompt for chunking
        if text.startswith('['):
            context_end = text.find(']')
            context = text[:context_end+1]
            text_body = text[context_end+1:].strip()
        else:
            context = ""
            text_body = text

        # Split by lines
        lines = [line.strip() for line in text_body.split('\n') if line.strip()]

        chunks = []
        current_chunk = ""

        for line in lines:
            if len(current_chunk) + len(line) + 2 > max_length and current_chunk:
                chunk_with_context = f"{context}\n{current_chunk}".strip() if context else current_chunk
                chunks.append(chunk_with_context)
                current_chunk = line
            else:
                if current_chunk:
                    current_chunk += "\n" + line
                else:
                    current_chunk = line

        # Add the last chunk
        if current_chunk:
            chunk_with_context = f"{context}\n{current_chunk}".strip() if context else current_chunk
            chunks.append(chunk_with_context)

        return chunks

    def _enhance_audio(self, audio: AudioSegment) -> AudioSegment:
        """Apply audio enhancements"""
        # Normalize
        audio = audio.normalize()

        # Gentle compression
        audio = audio.compress_dynamic_range(
            threshold=-20.0,
            ratio=4.0,
            attack=5.0,
            release=50.0
        )

        # Boost volume
        audio = audio + 2

        # High-pass filter
        audio = audio.high_pass_filter(80)

        return audio
