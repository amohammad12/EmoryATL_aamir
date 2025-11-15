"""
Services for Pirate Karaoke App
"""
from .rhyme_service import get_kid_friendly_rhymes
from .lyrics_service import LyricsGenerator
from .vocal_service import VocalGenerator
from .beat_manager import BeatLibraryManager
from .audio_service import AudioService
from .karaoke_service import KaraokeGenerator

__all__ = [
    "get_kid_friendly_rhymes",
    "LyricsGenerator",
    "VocalGenerator",
    "BeatLibraryManager",
    "AudioService",
    "KaraokeGenerator",
]
