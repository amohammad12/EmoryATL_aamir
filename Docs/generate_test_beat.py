#!/usr/bin/env python3
"""
Generate a simple test beat for testing the instrumental mixing

Creates a basic rhythmic pattern using synthesized sounds.
This is just for testing - download real pirate beats for production!

Usage:
    python generate_test_beat.py
"""
import numpy as np
import soundfile as sf
from pathlib import Path

def generate_simple_beat(duration=10.0, bpm=95, output_path="beats/pirate-shanty/test_beat_95bpm.wav"):
    """
    Generate a simple rhythmic beat for testing

    Args:
        duration: Length in seconds
        bpm: Tempo in beats per minute
        output_path: Where to save the WAV file
    """
    print("🎵 GENERATING TEST BEAT")
    print("=" * 60)
    print(f"Duration: {duration}s")
    print(f"BPM: {bpm}")
    print(f"Output: {output_path}")
    print()

    # Audio parameters
    sample_rate = 44100
    samples = int(sample_rate * duration)

    # Create time array
    t = np.linspace(0, duration, samples)

    # Calculate beat interval
    beat_interval = 60.0 / bpm  # seconds per beat

    # Generate bass drum pattern (kick on beats 1 and 3)
    kick = np.zeros(samples)
    for i in range(int(duration / beat_interval)):
        if i % 4 in [0, 2]:  # Beats 1 and 3
            start = int(i * beat_interval * sample_rate)
            length = int(0.1 * sample_rate)  # 100ms kick

            if start + length < samples:
                # Synthesize kick drum (low frequency decay)
                kick_t = np.linspace(0, 0.1, length)
                kick_wave = np.sin(2 * np.pi * 60 * kick_t) * np.exp(-30 * kick_t)
                kick[start:start+length] += kick_wave

    # Generate hi-hat pattern (every beat)
    hihat = np.zeros(samples)
    for i in range(int(duration / beat_interval)):
        start = int(i * beat_interval * sample_rate)
        length = int(0.05 * sample_rate)  # 50ms hi-hat

        if start + length < samples:
            # Synthesize hi-hat (high frequency noise burst)
            hihat_wave = np.random.randn(length) * 0.3 * np.exp(-100 * np.linspace(0, 0.05, length))
            hihat[start:start+length] += hihat_wave

    # Generate simple bass line (root note pattern)
    bass = np.sin(2 * np.pi * 110 * t) * 0.3  # A2 note

    # Add rhythm to bass (play on beats)
    bass_envelope = np.zeros(samples)
    for i in range(int(duration / beat_interval)):
        start = int(i * beat_interval * sample_rate)
        length = int(0.4 * sample_rate)  # 400ms bass note

        if start + length < samples:
            envelope = np.exp(-5 * np.linspace(0, 0.4, length))
            bass_envelope[start:start+length] = envelope

    bass *= bass_envelope

    # Mix all elements
    mix = kick * 0.6 + hihat * 0.3 + bass * 0.4

    # Normalize
    max_val = np.max(np.abs(mix))
    if max_val > 0:
        mix = mix / max_val * 0.8  # Leave headroom

    # Ensure stereo (duplicate to both channels)
    stereo_mix = np.stack([mix, mix], axis=1)

    # Create output directory if needed
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Save as WAV
    sf.write(str(output_path), stereo_mix, sample_rate)

    print(f"✅ Test beat generated!")
    print(f"💾 Saved to: {output_path}")
    print()
    print("📝 Next steps:")
    print("   1. Run: python scan_beats.py")
    print("   2. Generate a song to test mixing!")
    print()
    print("⚠️  NOTE: This is a basic test beat.")
    print("   For better results, download real pirate beats!")
    print("   See: FREE_INSTRUMENTALS_GUIDE.md")
    print()


if __name__ == "__main__":
    try:
        # Generate a 10-second test beat at 95 BPM (typical shanty tempo)
        generate_simple_beat(
            duration=10.0,
            bpm=95,
            output_path="beats/pirate-shanty/test_beat_95bpm.wav"
        )

        print("🎉 Done! Test beat ready for mixing.")

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
