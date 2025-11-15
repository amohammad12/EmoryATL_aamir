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
        self.model = genai.GenerativeModel('gemini-pro')

    def generate_pirate_shanty(
        self,
        word: str,
        rhymes: List[str]
    ) -> Dict[str, any]:
        """
        Generate pirate-themed sea shanty lyrics for preschool kids

        Args:
            word: Main theme word
            rhymes: List of rhyming words to incorporate

        Returns:
            Dictionary with lyrics, structure, word_count, estimated_duration
        """
        try:
            logger.info(f"Generating pirate shanty for word '{word}' with rhymes: {rhymes}")

            prompt = f"""
You are a songwriter for kids.
You specialize in pirate-themed sea shanties.
A song should include pirate-themed objects and ideas.
Incorporate additional information in the song to teach kids about the topic.

Make it very short, simple in vocabulary, and incorporate rhyming.
Add pirate vocalizations in parentheses.
For example: (arr!), (yo-ho!), (ahoy!), and (avast!)

Remember: this is for kids. No mature themes, alcohol references, violence.

REQUIREMENTS:
- Main theme word: "{word}"
- Use ONLY these rhyming words: {', '.join(rhymes)}
- Keep it to about 30 seconds when sung
- Simple vocabulary (ages 3-5)
- Include pirate vocalizations in parentheses like (arr!), (yo-ho!)
- Teach something educational about the word

Output only a song in this format:
Verse 1:
[2 lines]

Chorus:
[2 lines with pirate vocalization]

Verse 2:
[2 lines]

Chorus:
[2 lines with pirate vocalization]

Generate the pirate sea shanty now:
            """

            # Generate lyrics with Gemini
            response = self.model.generate_content(prompt)
            lyrics = response.text.strip()

            logger.info(f"Generated lyrics:\n{lyrics}")

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

        # Add buffer for musical pauses and pirate vocalizations
        duration *= 1.2

        logger.info(f"Estimated duration: {duration:.1f}s for {word_count} words")

        return duration
