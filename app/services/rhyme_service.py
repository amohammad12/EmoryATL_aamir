"""
Rhyme generation service for kid-friendly words
"""
import pronouncing
from typing import List
import logging

logger = logging.getLogger(__name__)

# Dolch Pre-Primer and Primer sight words for preschool
PRESCHOOL_VOCAB = {
    "a", "and", "away", "big", "blue", "can", "come", "down", "find", "for",
    "funny", "go", "help", "here", "I", "in", "is", "it", "jump", "little",
    "look", "make", "me", "my", "not", "one", "play", "red", "run", "said",
    "see", "the", "three", "to", "two", "up", "we", "where", "yellow", "you",
    "all", "am", "are", "at", "ate", "be", "black", "brown", "but", "came",
    "did", "do", "eat", "four", "get", "good", "have", "he", "into", "like",
    "must", "new", "no", "now", "on", "our", "out", "please", "pretty", "ran",
    "ride", "saw", "say", "she", "so", "soon", "that", "there", "they", "this",
    "too", "under", "want", "was", "well", "went", "what", "white", "who",
    "will", "with", "yes",
    # Additional kid-friendly words (NO PIRATE THEMES)
    "cat", "dog", "sun", "moon", "star", "tree", "bird", "fish", "car",
    "hat", "ball", "book", "cup", "pig", "box", "fox", "bee", "day",
    "night", "light", "right", "bright", "sky", "fly", "try", "cry",
    "smile", "mile", "while", "file", "cake", "lake", "make", "take",
    "snow", "grow", "show", "glow", "feet", "meet", "sweet", "treat"
}


def get_kid_friendly_rhymes(word: str, count: int = 6) -> List[str]:
    """
    Get simple, age-appropriate rhyming words for preschool kids

    Args:
        word: The word to find rhymes for
        count: Number of rhymes to return (default: 6)

    Returns:
        List of kid-friendly rhyming words
    """
    # Words to exclude (pirate-related and inappropriate themes)
    EXCLUDED_WORDS = {
        "ship", "sail", "whale", "tail", "sea", "pirate", "arr", "ahoy",
        "treasure", "crew", "captain", "boat", "ocean", "wave", "shore",
        "anchor", "mast", "deck", "port", "voyage", "island", "parrot",
        "cannon", "sword", "gold", "chest", "map", "flag", "plank"
    }

    try:
        # Get all rhymes from pronouncing library
        all_rhymes = pronouncing.rhymes(word.lower())

        if not all_rhymes:
            logger.warning(f"No rhymes found for word: {word}")
            return []

        # Filter for kid-friendly words
        kid_friendly = []
        for rhyme in all_rhymes:
            # Skip excluded words
            if rhyme.lower() in EXCLUDED_WORDS:
                continue

            # Check if in preschool vocabulary (high priority)
            if rhyme.lower() in PRESCHOOL_VOCAB:
                kid_friendly.append(rhyme)
            # Also accept simple words (max 3 syllables, increased length)
            elif len(rhyme) <= 10 and rhyme.isalpha():
                # Check syllable count (relaxed to 3 syllables)
                phones = pronouncing.phones_for_word(rhyme)
                if phones and pronouncing.syllable_count(phones[0]) <= 3:
                    kid_friendly.append(rhyme)

        # Remove duplicates and the original word
        kid_friendly = list(set(kid_friendly))
        if word.lower() in kid_friendly:
            kid_friendly.remove(word.lower())

        # Sort by word length (shorter = simpler for kids)
        kid_friendly.sort(key=len)

        # Return requested count
        result = kid_friendly[:count]

        logger.info(f"Found {len(result)} kid-friendly rhymes for '{word}': {result}")

        return result

    except Exception as e:
        logger.error(f"Error finding rhymes for '{word}': {e}")
        return []


def validate_word(word: str) -> bool:
    """
    Validate if a word is appropriate for kids and can be rhymed

    Args:
        word: Word to validate

    Returns:
        True if valid, False otherwise
    """
    # Check if single word
    if not word or len(word.split()) > 1:
        return False

    # Check if alphabetic
    if not word.isalpha():
        return False

    # Check length (3-10 characters is reasonable for kids)
    if len(word) < 2 or len(word) > 10:
        return False

    # Check if it has pronunciation data (can be rhymed)
    phones = pronouncing.phones_for_word(word.lower())
    if not phones:
        return False

    return True
