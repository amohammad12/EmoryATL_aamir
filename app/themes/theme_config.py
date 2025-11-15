"""
Theme configuration for pirate beat generation
Maps words to themes, instruments, and moods
"""
from typing import Dict, List, Set
from enum import Enum


class Theme(Enum):
    """Theme categories for pirate shanties"""
    NAUTICAL = "nautical"  # Ships, sailing, ocean
    TREASURE = "treasure"  # Gold, gems, riches
    ADVENTURE = "adventure"  # Exploration, discovery
    NATURE = "nature"  # Sea, sky, animals
    CREW = "crew"  # Pirates, sailors, friends
    MYSTERIOUS = "mysterious"  # Maps, secrets, islands


class Mood(Enum):
    """Mood/energy levels"""
    CALM = "calm"  # Gentle, peaceful
    PLAYFUL = "playful"  # Bouncy, fun
    ENERGETIC = "energetic"  # Exciting, fast
    MYSTERIOUS = "mysterious"  # Suspenseful, curious
    ADVENTUROUS = "adventurous"  # Bold, daring


# Word to theme mapping
THEME_WORDS: Dict[Theme, Set[str]] = {
    Theme.NAUTICAL: {
        "ship", "sail", "boat", "anchor", "helm", "mast", "deck",
        "port", "starboard", "voyage", "sailing", "fleet", "vessel"
    },
    Theme.TREASURE: {
        "treasure", "gold", "coin", "chest", "jewel", "gem", "ruby",
        "diamond", "pearl", "silver", "riches", "bounty", "loot"
    },
    Theme.ADVENTURE: {
        "adventure", "quest", "journey", "explore", "discover",
        "map", "compass", "island", "land", "shore", "beach"
    },
    Theme.NATURE: {
        "sea", "ocean", "wave", "water", "wind", "storm", "sky",
        "cloud", "sun", "moon", "star", "fish", "whale", "bird",
        "parrot", "crab", "dolphin"
    },
    Theme.CREW: {
        "pirate", "sailor", "crew", "captain", "mate", "friend",
        "team", "together", "help", "share", "work"
    },
    Theme.MYSTERIOUS: {
        "mystery", "secret", "hidden", "lost", "find", "search",
        "clue", "riddle", "puzzle", "key", "lock", "cave"
    }
}


# Instrument selection per theme
THEME_INSTRUMENTS: Dict[Theme, List[str]] = {
    Theme.NAUTICAL: ["accordion", "waves", "drums"],
    Theme.TREASURE: ["bells", "chimes", "drums"],
    Theme.ADVENTURE: ["fiddle", "accordion", "drums"],
    Theme.NATURE: ["waves", "flute", "light_drums"],
    Theme.CREW: ["drums", "accordion", "hand_claps"],
    Theme.MYSTERIOUS: ["bells", "light_drums", "ambient"]
}


# Default mood per theme
THEME_MOODS: Dict[Theme, Mood] = {
    Theme.NAUTICAL: Mood.ADVENTUROUS,
    Theme.TREASURE: Mood.PLAYFUL,
    Theme.ADVENTURE: Mood.ENERGETIC,
    Theme.NATURE: Mood.CALM,
    Theme.CREW: Mood.PLAYFUL,
    Theme.MYSTERIOUS: Mood.MYSTERIOUS
}


# Energy level per mood (0.0 = calm, 1.0 = very energetic)
MOOD_ENERGY: Dict[Mood, float] = {
    Mood.CALM: 0.3,
    Mood.PLAYFUL: 0.6,
    Mood.ENERGETIC: 0.9,
    Mood.MYSTERIOUS: 0.4,
    Mood.ADVENTUROUS: 0.75
}


def get_theme_for_word(word: str) -> Theme:
    """
    Determine theme category for a word

    Args:
        word: The theme word (e.g., "ship", "treasure")

    Returns:
        Theme enum value (defaults to ADVENTURE if unknown)
    """
    word_lower = word.lower().strip()

    for theme, words in THEME_WORDS.items():
        if word_lower in words:
            return theme

    # Default to adventure for unknown words
    return Theme.ADVENTURE


def get_instruments_for_theme(theme: Theme) -> List[str]:
    """Get instrument list for theme"""
    return THEME_INSTRUMENTS.get(theme, ["drums", "accordion"])


def get_mood_for_theme(theme: Theme) -> Mood:
    """Get default mood for theme"""
    return THEME_MOODS.get(theme, Mood.PLAYFUL)


def get_energy_for_mood(mood: Mood) -> float:
    """Get energy level (0.0-1.0) for mood"""
    return MOOD_ENERGY.get(mood, 0.6)


def get_theme_info(word: str) -> Dict:
    """
    Get complete theme information for a word

    Args:
        word: The theme word

    Returns:
        Dictionary with theme, instruments, mood, energy
    """
    theme = get_theme_for_word(word)
    mood = get_mood_for_theme(theme)
    energy = get_energy_for_mood(mood)
    instruments = get_instruments_for_theme(theme)

    return {
        "word": word,
        "theme": theme.value,
        "mood": mood.value,
        "energy": energy,
        "instruments": instruments
    }
