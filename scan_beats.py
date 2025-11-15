#!/usr/bin/env python3
"""
Beat Library Scanner

Scans the beats directory and auto-detects BPM for all WAV files.
Creates a catalog.json file with metadata for beat matching.

Usage:
    python scan_beats.py
"""
import sys
import logging
from pathlib import Path

# Setup path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.beat_manager import BeatLibraryManager
from app.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    """Scan beats directory and create catalog"""
    print("🎵 PIRATE KARAOKE BEAT SCANNER")
    print("=" * 60)
    print()

    # Initialize beat manager
    beat_manager = BeatLibraryManager()

    # Check if beats directory exists
    beats_dir = settings.BEATS_DIR
    pirate_dir = beats_dir / "pirate-shanty"

    print(f"📁 Beats directory: {beats_dir}")
    print(f"📁 Pirate shanty beats: {pirate_dir}")
    print()

    # Create directories if they don't exist
    beats_dir.mkdir(exist_ok=True)
    pirate_dir.mkdir(exist_ok=True)

    # Check for WAV files
    wav_files = list(pirate_dir.glob("*.wav"))

    if not wav_files:
        print("⚠️  WARNING: No WAV files found in beats/pirate-shanty/")
        print()
        print("📝 To add beats:")
        print("   1. Download pirate/sea shanty instrumentals (see FREE_INSTRUMENTALS_GUIDE.md)")
        print("   2. Convert to WAV format (44.1kHz recommended)")
        print("   3. Place in: beats/pirate-shanty/")
        print("   4. Run this script again")
        print()
        print("💡 TIP: Check FREE_INSTRUMENTALS_GUIDE.md for sources!")
        return

    print(f"✅ Found {len(wav_files)} WAV file(s) to analyze")
    print()

    # Scan directory
    print("🔍 Analyzing beats and detecting BPM...")
    print("-" * 60)
    beat_manager.scan_beats_directory()
    print("-" * 60)
    print()

    # Show catalog summary
    catalog = beat_manager.list_all_beats()

    print("📊 CATALOG SUMMARY")
    print("=" * 60)

    total_beats = 0
    for genre, beats in catalog.items():
        print(f"\n🎼 Genre: {genre}")
        print(f"   Beats: {len(beats)}")
        total_beats += len(beats)

        for beat in beats:
            print(f"   • {beat['filename']}")
            print(f"     BPM: {beat['bpm']:.1f}")
            print(f"     Duration: {beat['duration']:.1f}s")

    print()
    print("=" * 60)
    print(f"✅ Total beats in catalog: {total_beats}")
    print(f"💾 Catalog saved to: {beat_manager.catalog_file}")
    print()

    if total_beats > 0:
        print("🎉 SUCCESS! Beat library ready!")
        print()
        print("📝 Next steps:")
        print("   1. Restart your Celery worker (if running)")
        print("   2. Generate a new song")
        print("   3. It will automatically include background music!")
        print()
    else:
        print("⚠️  No beats were cataloged successfully")
        print("   Check that your WAV files are valid")
        print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Scan cancelled by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error during beat scanning: {e}", exc_info=True)
        print(f"\n❌ ERROR: {e}")
        sys.exit(1)
