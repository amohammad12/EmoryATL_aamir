#!/usr/bin/env python3
"""
Test different Bark voice presets to find the best teacher voice
"""
import os
os.environ['BARK_USE_GPU'] = 'True'

from app.services.vocal_service import VocalGenerator
from app.config import settings

# Sample pirate rhyme for testing
TEST_LYRICS = """
On a ship we sail the sea,
Looking for treasure, arr, you and me!
With a yo-ho-ho and a bottle of fun,
We're pirate friends beneath the sun!
"""

# Available Bark voice presets
VOICE_PRESETS = [
    ("v2/en_speaker_0", "Male - Deep"),
    ("v2/en_speaker_1", "Male - Medium"),
    ("v2/en_speaker_2", "Male - Young"),
    ("v2/en_speaker_3", "Female - Older"),
    ("v2/en_speaker_5", "Female - Clear"),
    ("v2/en_speaker_6", "Female - Young (Current)"),
    ("v2/en_speaker_7", "Female - Warm"),
    ("v2/en_speaker_8", "Female - Bright"),
    ("v2/en_speaker_9", "Female - Soft"),
]

def test_voice(voice_preset, description):
    """Test a single voice preset"""
    print(f"\n{'='*60}")
    print(f"Testing: {voice_preset} - {description}")
    print(f"{'='*60}")

    try:
        # Update settings
        settings.BARK_VOICE_PRESET = voice_preset

        # Generate vocals
        gen = VocalGenerator()
        output_path = f"test_voice_{voice_preset.replace('/', '_')}.mp3"
        gen.generate_vocals(TEST_LYRICS, output_path)

        print(f"✅ Generated: {output_path}")
        print(f"   Listen to this voice and see if it sounds like a teacher!")

    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Test all voice presets"""
    print("🎤 Bark Voice Preset Tester")
    print("Testing different voices to find the best teacher sound...")
    print("\nThis will generate multiple MP3 files for comparison.")
    print("Listen to each one and pick your favorite!\n")

    input("Press Enter to start testing voices...")

    for voice_preset, description in VOICE_PRESETS:
        test_voice(voice_preset, description)

    print("\n" + "="*60)
    print("✅ All voices tested!")
    print("="*60)
    print("\nGenerated files:")
    print("- test_voice_v2_en_speaker_0.mp3 (Male - Deep)")
    print("- test_voice_v2_en_speaker_1.mp3 (Male - Medium)")
    print("- test_voice_v2_en_speaker_2.mp3 (Male - Young)")
    print("- test_voice_v2_en_speaker_3.mp3 (Female - Older)")
    print("- test_voice_v2_en_speaker_5.mp3 (Female - Clear)")
    print("- test_voice_v2_en_speaker_6.mp3 (Female - Young) ← Current")
    print("- test_voice_v2_en_speaker_7.mp3 (Female - Warm)")
    print("- test_voice_v2_en_speaker_8.mp3 (Female - Bright)")
    print("- test_voice_v2_en_speaker_9.mp3 (Female - Soft)")
    print("\n🎧 Listen to each file and pick the best teacher voice!")
    print("📝 Then update BARK_VOICE_PRESET in your .env file\n")

if __name__ == "__main__":
    main()
