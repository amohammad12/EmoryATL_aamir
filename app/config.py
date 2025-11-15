"""
Configuration management for Pirate Karaoke App
"""
from pydantic_settings import BaseSettings
from pathlib import Path
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Gemini API
    GEMINI_API_KEY: str

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

    # Edge TTS Settings
    TTS_VOICE: str = "en-US-JennyNeural"
    TTS_RATE: str = "-10%"
    TTS_PITCH: str = "+5Hz"

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
