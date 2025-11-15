"""
Mood analyzer for lyrics
Analyzes lyrics text to determine mood and energy level
"""
import re
import logging
from typing import Dict
from app.themes.theme_config import Mood, MOOD_ENERGY

logger = logging.getLogger(__name__)


class MoodAnalyzer:
    """Analyze lyrics to determine mood and energy"""

    def __init__(self):
        """Initialize mood analyzer with keyword patterns"""

        # Mood indicator words
        self.mood_keywords = {
            Mood.ENERGETIC: {
                "fast", "quick", "run", "race", "hurry", "speed", "rush",
                "jump", "dance", "play", "exciting", "adventure", "bold"
            },
            Mood.PLAYFUL: {
                "fun", "silly", "giggle", "laugh", "smile", "happy",
                "bounce", "hop", "skip", "play", "joy", "cheerful",
                "yo-ho", "arr", "ahoy"
            },
            Mood.CALM: {
                "slow", "gentle", "soft", "quiet", "peaceful", "rest",
                "sleep", "calm", "easy", "relax", "drift", "float"
            },
            Mood.MYSTERIOUS: {
                "secret", "hidden", "mystery", "dark", "shadow", "whisper",
                "quiet", "sneak", "peek", "find", "search", "wonder"
            },
            Mood.ADVENTUROUS: {
                "sail", "explore", "discover", "journey", "quest", "brave",
                "bold", "hero", "adventure", "voyage", "travel", "roam"
            }
        }

    def analyze_lyrics(self, lyrics: str) -> Dict:
        """
        Analyze lyrics to determine mood and energy

        Args:
            lyrics: The lyrics text

        Returns:
            Dictionary with mood, energy, and confidence
        """
        try:
            # Clean lyrics
            lyrics_lower = lyrics.lower()

            # Count mood indicators
            mood_scores = {mood: 0 for mood in Mood}

            for mood, keywords in self.mood_keywords.items():
                for keyword in keywords:
                    # Count occurrences
                    count = len(re.findall(r'\b' + re.escape(keyword) + r'\b', lyrics_lower))
                    mood_scores[mood] += count

            # Find dominant mood
            if max(mood_scores.values()) > 0:
                dominant_mood = max(mood_scores, key=mood_scores.get)
                confidence = mood_scores[dominant_mood] / sum(mood_scores.values())
            else:
                # Default to playful if no indicators
                dominant_mood = Mood.PLAYFUL
                confidence = 0.5

            # Get energy level
            energy = MOOD_ENERGY[dominant_mood]

            # Check for exclamation marks (increase energy)
            exclamation_count = lyrics.count('!')
            if exclamation_count > 2:
                energy = min(1.0, energy + 0.1)

            logger.info(f"Lyrics mood analysis: {dominant_mood.value} (energy: {energy:.2f}, confidence: {confidence:.2f})")
            logger.debug(f"Mood scores: {dict((m.value, s) for m, s in mood_scores.items())}")

            return {
                "mood": dominant_mood,
                "energy": energy,
                "confidence": confidence,
                "mood_scores": mood_scores
            }

        except Exception as e:
            logger.error(f"Error analyzing lyrics mood: {e}")
            # Return default
            return {
                "mood": Mood.PLAYFUL,
                "energy": 0.6,
                "confidence": 0.5,
                "mood_scores": {}
            }

    def adjust_energy_for_bpm(self, base_energy: float, bpm: float) -> float:
        """
        Adjust energy based on detected BPM

        Args:
            base_energy: Base energy from mood analysis
            bpm: Detected BPM of vocals

        Returns:
            Adjusted energy level (0.0-1.0)
        """
        # Typical pirate shanty range: 85-105 BPM
        # Lower BPM = reduce energy
        # Higher BPM = increase energy

        if bpm < 90:
            adjustment = -0.1
        elif bpm > 100:
            adjustment = 0.1
        else:
            adjustment = 0.0

        adjusted = max(0.0, min(1.0, base_energy + adjustment))

        logger.debug(f"Energy adjusted for BPM {bpm}: {base_energy:.2f} → {adjusted:.2f}")

        return adjusted
