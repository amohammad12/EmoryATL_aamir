"""
Lyrics generation service using Gemini API for pirate-themed sea shanties
"""
import google.generativeai as genai
from typing import List, Dict
import logging
from app.config import settings

logger = logging.getLogger(__name__)


class LyricsGenerator:
    """Generate pirate-themed sea shanty lyrics for kids using Gemini"""

    def __init__(self):
        """Initialize Gemini API"""
        genai.configure(api_key=settings.GEMINI_API_KEY)
        # Use the latest stable Gemini 2.5 Flash model (fast and free!)
        self.model = genai.GenerativeModel('models/gemini-2.5-flash')

    def generate_pirate_shanty(
        self,
        word: str,
        rhymes: List[str]
    ) -> Dict[str, any]:
        """
        Generate simple, cute educational song lyrics for preschool kids

        Args:
            word: Main theme word
            rhymes: List of rhyming words to incorporate

        Returns:
            Dictionary with lyrics, structure, word_count, estimated_duration
        """
        try:
            logger.info(f"Generating kids song for word '{word}' with rhymes: {rhymes}")

            prompt = f"""
You are a gentle, caring preschool teacher creating SOFT, EDUCATIONAL songs for 3-5 year olds.

TOPIC: {word}

CRITICAL RULES - READ CAREFULLY:
1. ✅ GENTLE & SMOOTH - Use soft, flowing words that sound sweet when sung
2. ✅ EDUCATIONAL - Teach kids what "{word}" is in a loving, nurturing way
3. ✅ SIMPLE STORY - Tell one clear idea that makes sense to little children
4. ✅ NATURAL LANGUAGE - Write like you're talking to a young child, not performing
5. ✅ CALM TONE - Soothing and peaceful, like a lullaby or gentle nursery rhyme

ABSOLUTELY FORBIDDEN WORDS (NEVER USE THESE):
❌ arr, ahoy, yo-ho, avast, matey, shiver, timbers
❌ ANY pirate-related words or sounds
❌ ANY harsh or loud exclamations
❌ ship, sail, sea, ocean, boat, treasure, captain, crew

SONG STRUCTURE:
✅ Write exactly 4-6 gentle lines
✅ Each line teaches something sweet about "{word}"
✅ Use words a 3-year-old knows: happy, soft, pretty, nice, love, play, fun
✅ Make it peaceful and comforting
✅ Optional: You may use these words if they fit gently: {', '.join(rhymes[:2])}

TONE EXAMPLES:
✅ GOOD (gentle): "The butterfly is soft and light, it dances in the air"
❌ BAD (harsh): "The butterfly goes whoosh and zoom, it's wild everywhere"

WRITE A GENTLE SONG ABOUT "{word}":
            """

            # Generate lyrics with Gemini
            response = self.model.generate_content(prompt)
            lyrics = response.text.strip()

            logger.info(f"Generated lyrics (raw):\n{lyrics}")

            # CRITICAL: Remove any pirate words that slipped through
            lyrics = self._remove_pirate_words(lyrics)

            logger.info(f"Generated lyrics (cleaned):\n{lyrics}")

            # Parse and validate
            word_count = len(lyrics.split())
            estimated_duration = self._estimate_duration(lyrics)

            return {
                "lyrics": lyrics,
                "word_count": word_count,
                "estimated_duration": estimated_duration,
                "word": word,
                "rhymes_used": rhymes
            }

        except Exception as e:
            logger.error(f"Error generating lyrics: {e}")
            raise

    def _remove_pirate_words(self, lyrics: str) -> str:
        """
        Remove pirate exclamations and harsh sounds from lyrics

        This is a safety net - the Gemini prompt should prevent these,
        but we remove them here just in case they slip through.

        Args:
            lyrics: The raw lyrics

        Returns:
            Cleaned lyrics without pirate exclamations
        """
        import re

        # ONLY remove pirate-specific exclamations and sounds
        # We don't remove nautical words here because they might be legitimate topics
        pirate_exclamations = [
            # Pirate exclamations and sounds
            r'\barr+!?\b', r'\bahoy!?\b', r'\byo-ho+!?\b', r'\bavast!?\b',
            r'\bmatey!?\b', r'\bshiver\s+me\s+timbers!?\b', r'\bblimey!?\b',

            # In parentheses
            r'\(arr+!?\)', r'\(ahoy!?\)', r'\(yo-ho+!?\)', r'\(avast!?\)',
            r'\(matey!?\)', r'\(blimey!?\)',

            # Standalone anywhere in line
            r'arr+!?', r'ahoy!?', r'yo-ho+!?', r'avast!?',

            # Common pirate phrases
            r'\bshiver\s+me\s+timbers', r'\bwalk\s+the\s+plank',
            r'\bpirate\s+treasure', r'\bpirate\s+ship',
        ]

        cleaned = lyrics
        for pattern in pirate_exclamations:
            cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)

        # Remove extra whitespace and empty lines that result from removals
        cleaned = re.sub(r'\n\s*\n+', '\n', cleaned)  # Multiple blank lines to one
        cleaned = re.sub(r' +', ' ', cleaned)  # Multiple spaces to one
        cleaned = re.sub(r' \n', '\n', cleaned)  # Space before newline
        cleaned = re.sub(r'\n ', '\n', cleaned)  # Space after newline
        cleaned = cleaned.strip()

        return cleaned

    def _estimate_duration(self, lyrics: str) -> float:
        """
        Estimate song duration based on word count

        Args:
            lyrics: The lyrics text

        Returns:
            Estimated duration in seconds (target: 30 seconds)
        """
        word_count = len(lyrics.split())
        # Kids songs: ~60-80 words per minute
        # For shanties, slightly slower: ~50-60 words per minute
        words_per_second = 1.0  # 60 words per minute
        duration = word_count / words_per_second

        # Add buffer for musical pauses
        duration *= 1.2

        logger.info(f"Estimated duration: {duration:.1f}s for {word_count} words")

        return duration
