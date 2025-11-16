"""
MongoDB models using Beanie ODM for Pirate Karaoke App
"""
from beanie import Document
from pydantic import Field, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
import bcrypt


class Job(Document):
    """Model for tracking async song generation jobs"""

    job_id: str = Field(..., description="Unique job identifier")
    word: str = Field(..., description="Input word for song generation")
    status: str = Field(default="pending", description="Job status: pending, processing, completed, failed")
    progress: int = Field(default=0, description="Progress percentage (0-100)")
    error: Optional[str] = Field(default=None, description="Error message if failed")
    result: Optional[Dict[str, Any]] = Field(default=None, description="Result data if completed")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "jobs"  # Collection name
        indexes = [
            "job_id",
            "word",
            "status",
        ]

    class Config:
        json_schema_extra = {
            "example": {
                "job_id": "123e4567-e89b-12d3-a456-426614174000",
                "word": "ship",
                "status": "processing",
                "progress": 50
            }
        }


class SongCache(Document):
    """Model for caching generated songs"""

    word: str = Field(..., description="Input word (unique)", unique=True)
    lyrics: str = Field(..., description="Generated lyrics")
    audio_url: str = Field(..., description="URL to audio file")
    timings: List[Dict[str, Any]] = Field(..., description="Karaoke word timings")
    duration: float = Field(..., description="Song duration in seconds")
    bpm: float = Field(..., description="Beats per minute")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "song_cache"  # Collection name
        indexes = [
            "word",
        ]

    class Config:
        json_schema_extra = {
            "example": {
                "word": "ship",
                "lyrics": "Verse 1:\\nOn a ship we sail (arr!)\\n...",
                "audio_url": "/outputs/song_123.mp3",
                "timings": [
                    {"word": "On", "start": 0.0, "end": 0.3},
                    {"word": "a", "start": 0.3, "end": 0.5}
                ],
                "duration": 30.5,
                "bpm": 95.0
            }
        }


class User(Document):
    """Model for user accounts"""

    username: str = Field(..., description="Unique username", unique=True)
    email: EmailStr = Field(..., description="User email address", unique=True)
    password_hash: str = Field(..., description="Hashed password")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = Field(default=None)

    class Settings:
        name = "users"
        indexes = [
            "username",
            "email",
        ]

    def verify_password(self, password: str) -> bool:
        """Verify password against stored hash"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password for storage"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')


class UserLibrary(Document):
    """Model for user's saved songs library"""

    user_id: str = Field(..., description="User identifier (username)")
    title: str = Field(..., description="Song title")
    lyrics: str = Field(..., description="Song lyrics")
    audio_url: str = Field(..., description="URL to audio file")
    timings: List[Dict[str, Any]] = Field(..., description="Karaoke word timings")
    duration: Optional[float] = Field(default=None, description="Song duration in seconds")
    bpm: Optional[float] = Field(default=None, description="Beats per minute")
    added_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "user_library"  # Collection name
        indexes = [
            "user_id",
            "added_at",
        ]

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "john_doe",
                "title": "The Ship Song",
                "lyrics": "Verse 1:\\nOn a ship we sail (arr!)\\n...",
                "audio_url": "/outputs/song_123.mp3",
                "timings": [
                    {"word": "On", "start": 0.0, "end": 0.3},
                    {"word": "a", "start": 0.3, "end": 0.5}
                ],
                "duration": 30.5,
                "bpm": 95.0
            }
        }
