#!/usr/bin/env python3
"""
Test dynamic theme-based beat generation

Tests the PirateBeatGenerator with various theme words
to verify different instruments and moods are applied.
"""
import sys
from pathlib import Path

# Setup path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.pirate_beat_generator import PirateBeatGenerator
from app.themes.theme_config import get_theme_info
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def test_beat_generation():
    """Test beat generation with various theme words"""
    print("🎵 THEME-BASED BEAT GENERATION TEST")
    print("=" * 70)
    print()

    # Test words from different themes
    test_words = [
        ("ship", "Nautical theme - should have accordion + waves"),
        ("treasure", "Treasure theme - should have bells/chimes"),
        ("adventure", "Adventure theme - should have fiddle + accordion"),
        ("sea", "Nature theme - should have waves + flute"),
        ("crew", "Crew theme - should have hand claps"),
        ("mystery", "Mysterious theme - should have ambient + bells"),
    ]

    # Create output directory
    output_dir = Path("test_beats")
    output_dir.mkdir(exist_ok=True)

    # Initialize generator
    beat_gen = PirateBeatGenerator()

    print("📊 Theme Analysis:")
    print("-" * 70)
    for word, description in test_words:
        theme_info = get_theme_info(word)
        print(f"\n🎯 Word: '{word}'")
        print(f"   {description}")
        print(f"   Theme: {theme_info['theme']}")
        print(f"   Mood: {theme_info['mood']}")
        print(f"   Energy: {theme_info['energy']:.2f}")
        print(f"   Instruments: {', '.join(theme_info['instruments'])}")

    print()
    print("=" * 70)
    print()

    # Generate beats
    print("🎼 Generating Test Beats...")
    print("-" * 70)
    print()

    for word, description in test_words:
        print(f"Generating beat for '{word}'... ", end='', flush=True)

        try:
            theme_info = get_theme_info(word)

            # Generate 10-second test beat
            output_path = str(output_dir / f"{word}_beat.wav")

            beat_path = beat_gen.generate_beat(
                word=word,
                duration=10.0,  # 10 seconds for testing
                bpm=95,  # Standard shanty tempo
                energy=theme_info['energy'],
                output_path=output_path
            )

            print(f"✅ Generated: {beat_path}")

        except Exception as e:
            print(f"❌ FAILED: {e}")
            logger.error(f"Error generating beat for '{word}': {e}", exc_info=True)

    print()
    print("=" * 70)
    print("🎉 TEST COMPLETE!")
    print()
    print(f"📁 Test beats saved to: {output_dir.absolute()}")
    print()
    print("📝 Next Steps:")
    print("   1. Listen to the generated WAV files")
    print("   2. Verify different instruments for different themes")
    print("   3. Check that energy levels vary appropriately")
    print("   4. Restart Celery and test with real song generation:")
    print("      curl -X POST http://localhost:8000/api/generate \\")
    print("        -H 'Content-Type: application/json' \\")
    print("        -d '{\"word\":\"ship\"}'")
    print()


if __name__ == "__main__":
    try:
        test_beat_generation()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test cancelled by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Test failed: {e}", exc_info=True)
        print(f"\n❌ ERROR: {e}")
        sys.exit(1)
