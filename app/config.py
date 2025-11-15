"""
Configuration management for Pirate Karaoke App
"""
from pydantic_settings import BaseSettings
from pathlib import Path
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # API Keys
    GEMINI_API_KEY: str  # For lyrics generation
    ELEVENLABS_API_KEY: Optional[str] = None  # For vocals (optional - falls back to Bark)

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # MongoDB
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "pirate_karaoke"

    # Audio Settings
    SAMPLE_RATE: int = 24000
    VOCALS_VOLUME: float = 1.0
    INSTRUMENTAL_VOLUME: float = 0.4
    PIRATE_SHANTY_BPM_MIN: int = 90
    PIRATE_SHANTY_BPM_MAX: int = 110

    # TTS Provider Selection
    TTS_PROVIDER: str = "elevenlabs"  # Options: "elevenlabs" or "bark"
    TTS_FALLBACK_TO_BARK: bool = True  # Use Bark if ElevenLabs fails

    # ElevenLabs TTS Settings (Primary - Professional Quality)
    ELEVENLABS_VOICE_ID: str = "EXAVITQu4vr4xnSDxMaL"  # Bella - young, warm teacher voice
    ELEVENLABS_MODEL: str = "eleven_multilingual_v2"
    ELEVENLABS_STABILITY: float = 0.5  # 0-1 (higher = more consistent)
    ELEVENLABS_SIMILARITY: float = 0.75  # 0-1 (higher = closer to original voice)
    ELEVENLABS_STYLE: float = 0.0  # 0-1 (exaggeration of style)
    ELEVENLABS_BOOST: bool = True  # Speaker boost for clarity

    # Bark TTS Settings (Fallback - Expressive Quality)
    BARK_MODEL: str = "suno/bark"
    BARK_VOICE_PRESET: str = "v2/en_speaker_9"  # Warm, soft female teacher voice
    BARK_TEMPERATURE: float = 0.7  # Controls randomness/expressiveness (0.0-1.0)
    BARK_USE_GPU: bool = True  # Enable GPU acceleration
    BARK_SINGING_MODE: bool = True  # Enable teacher-style expressive reading
    BARK_SEMANTIC_TEMP: float = 0.9  # Semantic (higher = more expressive)
    BARK_COARSE_TEMP: float = 0.8  # Coarse (higher = more varied)
    BARK_FINE_TEMP: float = 0.7  # Fine (higher = more natural)

    # Directories
    BEATS_DIR: Path = Path("beats")
    OUTPUT_DIR: Path = Path("outputs")
    TEMP_DIR: Path = Path("temp")

    # Application
    MAX_CONCURRENT_JOBS: int = 3
    CACHE_EXPIRY_DAYS: int = 7
    DEBUG: bool = False

    class Config:
        env_file = ".env"
        case_sensitive = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ensure directories exist
        self.BEATS_DIR.mkdir(exist_ok=True)
        self.OUTPUT_DIR.mkdir(exist_ok=True)
        self.TEMP_DIR.mkdir(exist_ok=True)


# Global settings instance
settings = Settings()
