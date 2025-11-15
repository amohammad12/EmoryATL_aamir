"""
Configuration package for Pirate Karaoke App
"""
# Export theme config
from .theme_config import (
    Theme,
    Mood,
    get_theme_for_word,
    get_instruments_for_theme,
    get_mood_for_theme,
    get_energy_for_mood,
    get_theme_info
)

__all__ = [
    'Theme',
    'Mood',
    'get_theme_for_word',
    'get_instruments_for_theme',
    'get_mood_for_theme',
    'get_energy_for_mood',
    'get_theme_info'
]
