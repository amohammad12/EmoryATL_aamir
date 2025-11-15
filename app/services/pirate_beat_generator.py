"""
Pirate Beat Generator - Dynamic theme-based instrumental generation
Synthesizes pirate-themed beats using pure Python (100% free!)
"""
import numpy as np
import soundfile as sf
import uuid
import logging
from pathlib import Path
from typing import Optional, List
from app.config import settings
from app.themes.theme_config import get_theme_info

logger = logging.getLogger(__name__)


class PirateBeatGenerator:
    """Generate pirate-themed instrumental beats programmatically"""

    def __init__(self):
        """Initialize beat generator"""
        self.sample_rate = settings.SAMPLE_RATE
        self.temp_dir = settings.TEMP_DIR
        self.temp_dir.mkdir(exist_ok=True)

    def generate_beat(
        self,
        word: str,
        duration: float,
        bpm: float,
        energy: float = 0.6,
        output_path: Optional[str] = None
    ) -> str:
        """
        Generate themed pirate beat

        Args:
            word: Theme word (e.g., "ship", "treasure")
            duration: Length in seconds
            bpm: Tempo in beats per minute
            energy: Energy level 0.0-1.0 (affects intensity)
            output_path: Optional output path

        Returns:
            Path to generated WAV file
        """
        try:
            logger.info(f"Generating pirate beat: word='{word}', duration={duration}s, bpm={bpm}, energy={energy:.2f}")

            # Get theme info
            theme_info = get_theme_info(word)
            instruments = theme_info['instruments']

            logger.info(f"Theme: {theme_info['theme']}, Mood: {theme_info['mood']}, Instruments: {instruments}")

            # Generate time array
            samples = int(self.sample_rate * duration)
            t = np.linspace(0, duration, samples)

            # Initialize mix
            mix = np.zeros(samples)

            # Generate drums (always present)
            if "drums" in instruments or "light_drums" in instruments:
                intensity = 1.0 if "drums" in instruments else 0.7
                kick, snare, hihat = self._generate_drums(duration, bpm, energy, intensity)
                mix += kick * 0.45 + snare * 0.35 + hihat * 0.25

            # Generate accordion (for nautical, adventure, crew themes)
            if "accordion" in instruments:
                accordion = self._generate_accordion(duration, bpm, t)
                mix += accordion * 0.40

            # Generate bells/chimes (for treasure, mysterious themes)
            if "bells" in instruments or "chimes" in instruments:
                bells = self._generate_bells(duration, bpm, t)
                mix += bells * 0.35

            # Generate fiddle (for adventure, crew themes)
            if "fiddle" in instruments:
                fiddle = self._generate_fiddle(duration, bpm, t, energy)
                mix += fiddle * 0.38

            # Generate waves (for nautical, nature themes)
            if "waves" in instruments:
                waves = self._generate_waves(duration, t)
                mix += waves * 0.25

            # Generate flute (for nature theme)
            if "flute" in instruments:
                flute = self._generate_flute(duration, bpm, t)
                mix += flute * 0.30

            # Generate hand claps (for crew theme)
            if "hand_claps" in instruments:
                claps = self._generate_hand_claps(duration, bpm)
                mix += claps * 0.30

            # Generate ambient (for mysterious theme)
            if "ambient" in instruments:
                ambient = self._generate_ambient(duration, t)
                mix += ambient * 0.20

            # Normalize mix
            max_val = np.max(np.abs(mix))
            if max_val > 0:
                mix = mix / max_val * 0.85  # Leave headroom

            # Apply energy-based compression (louder for high energy)
            mix = mix * (0.7 + (energy * 0.3))

            # Save as stereo WAV
            stereo_mix = np.stack([mix, mix], axis=1)

            if output_path is None:
                filename = f"beat_{word}_{uuid.uuid4().hex[:8]}.wav"
                output_path = str(self.temp_dir / filename)

            sf.write(output_path, stereo_mix, self.sample_rate)

            logger.info(f"Beat generated successfully: {output_path}")

            return output_path

        except Exception as e:
            logger.error(f"Error generating beat: {e}")
            raise

    def _generate_drums(self, duration: float, bpm: float, energy: float, intensity: float = 1.0):
        """Generate drum patterns (kick, snare, hi-hat)"""
        samples = int(self.sample_rate * duration)
        beat_interval = 60.0 / bpm

        kick = np.zeros(samples)
        snare = np.zeros(samples)
        hihat = np.zeros(samples)

        # Generate pattern
        num_beats = int(duration / beat_interval)

        for i in range(num_beats):
            beat_start = int(i * beat_interval * self.sample_rate)

            # Kick on beats 1 and 3 (sea shanty feel)
            if i % 4 in [0, 2]:
                kick_length = int(0.15 * self.sample_rate)
                if beat_start + kick_length < samples:
                    kick_t = np.linspace(0, 0.15, kick_length)
                    # Deep kick
                    kick_wave = np.sin(2 * np.pi * 55 * kick_t) * np.exp(-25 * kick_t)
                    kick[beat_start:beat_start+kick_length] += kick_wave * intensity

            # Snare on beats 2 and 4
            if i % 4 in [1, 3]:
                snare_length = int(0.08 * self.sample_rate)
                if beat_start + snare_length < samples:
                    snare_t = np.linspace(0, 0.08, snare_length)
                    # Snare = tone + noise
                    snare_tone = np.sin(2 * np.pi * 200 * snare_t)
                    snare_noise = np.random.randn(snare_length) * 0.8
                    snare_wave = (snare_tone + snare_noise) * np.exp(-60 * snare_t)
                    snare[beat_start:beat_start+snare_length] += snare_wave * intensity * 0.8

            # Hi-hat on every beat (more for higher energy)
            if energy > 0.5 or i % 2 == 0:
                hihat_length = int(0.04 * self.sample_rate)
                if beat_start + hihat_length < samples:
                    # Hi-hat = high-freq noise
                    hihat_wave = np.random.randn(hihat_length) * 0.4 * np.exp(-150 * np.linspace(0, 0.04, hihat_length))
                    hihat[beat_start:beat_start+hihat_length] += hihat_wave * intensity * (0.5 + energy * 0.5)

        return kick, snare, hihat

    def _generate_accordion(self, duration: float, bpm: float, t: np.ndarray) -> np.ndarray:
        """Generate accordion-like sound with vibrato"""
        # Accordion plays simple chord progression
        # Use multiple harmonics for richer sound

        beat_interval = 60.0 / bpm
        num_bars = int(duration / (beat_interval * 4))

        # Simple pirate shanty chord progression (in A minor)
        # Am - F - C - G pattern
        root_freqs = [220, 175, 262, 196]  # A, F, C, G

        accordion = np.zeros(len(t))

        for bar in range(num_bars):
            bar_start_time = bar * beat_interval * 4
            bar_start_sample = int(bar_start_time * self.sample_rate)
            chord_duration = beat_interval * 4  # One bar per chord
            chord_samples = int(chord_duration * self.sample_rate)

            if bar_start_sample + chord_samples < len(t):
                chord_t = t[bar_start_sample:bar_start_sample+chord_samples] - bar_start_time

                # Get root frequency for this bar
                root = root_freqs[bar % len(root_freqs)]

                # Generate chord (root + 5th + octave) with harmonics
                chord = np.zeros(len(chord_t))
                for harmonic, amp in [(1, 1.0), (1.5, 0.6), (2, 0.4)]:  # Root, 5th, octave
                    freq = root * harmonic
                    # Add vibrato (typical accordion wobble)
                    vibrato = 1 + 0.015 * np.sin(2 * np.pi * 5.5 * chord_t)
                    chord += amp * np.sin(2 * np.pi * freq * chord_t * vibrato)

                # Envelope (gentle attack and release)
                envelope = np.ones(len(chord_t))
                attack_samples = int(0.1 * self.sample_rate)
                release_samples = int(0.2 * self.sample_rate)
                envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
                envelope[-release_samples:] = np.linspace(1, 0, release_samples)

                accordion[bar_start_sample:bar_start_sample+chord_samples] += chord * envelope * 0.3

        return accordion

    def _generate_bells(self, duration: float, bpm: float, t: np.ndarray) -> np.ndarray:
        """Generate bell/chime sounds for treasure theme"""
        beat_interval = 60.0 / bpm
        bells = np.zeros(len(t))

        # Ring bells on certain beats
        num_beats = int(duration / beat_interval)

        for i in range(num_beats):
            # Ring on beats 1 and 3
            if i % 4 in [0, 2]:
                bell_start_time = i * beat_interval
                bell_start_sample = int(bell_start_time * self.sample_rate)
                bell_duration = 0.8  # Long decay
                bell_samples = int(bell_duration * self.sample_rate)

                if bell_start_sample + bell_samples < len(t):
                    bell_t = t[bell_start_sample:bell_start_sample+bell_samples] - bell_start_time

                    # Bell = multiple sine waves with different decay rates
                    bell = (
                        np.sin(2 * np.pi * 523 * bell_t) * np.exp(-8 * bell_t) +  # C5
                        np.sin(2 * np.pi * 659 * bell_t) * np.exp(-10 * bell_t) * 0.7 +  # E5
                        np.sin(2 * np.pi * 784 * bell_t) * np.exp(-12 * bell_t) * 0.5  # G5
                    )

                    bells[bell_start_sample:bell_start_sample+bell_samples] += bell * 0.25

        return bells

    def _generate_fiddle(self, duration: float, bpm: float, t: np.ndarray, energy: float) -> np.ndarray:
        """Generate fiddle-like melody"""
        beat_interval = 60.0 / bpm
        fiddle = np.zeros(len(t))

        # Simple maritime melody (in A minor pentatonic: A C D E G)
        melody_notes = [220, 262, 294, 330, 392]  # A3, C4, D4, E4, G4

        num_beats = int(duration / beat_interval)

        for i in range(num_beats):
            # Play a note on each beat (more frequent for high energy)
            if energy > 0.6 or i % 2 == 0:
                note_start_time = i * beat_interval
                note_start_sample = int(note_start_time * self.sample_rate)
                note_duration = beat_interval * 0.6  # Slightly detached
                note_samples = int(note_duration * self.sample_rate)

                if note_start_sample + note_samples < len(t):
                    note_t = t[note_start_sample:note_start_sample+note_samples] - note_start_time

                    # Pick a note from melody
                    freq = melody_notes[i % len(melody_notes)]

                    # Fiddle = sawtooth-ish (multiple harmonics)
                    note = np.zeros(len(note_t))
                    for h in range(1, 6):
                        note += np.sin(2 * np.pi * freq * h * note_t) / h

                    # Envelope
                    envelope = np.exp(-4 * note_t)

                    fiddle[note_start_sample:note_start_sample+note_samples] += note * envelope * 0.15

        return fiddle

    def _generate_waves(self, duration: float, t: np.ndarray) -> np.ndarray:
        """Generate ocean wave ambience"""
        # Low-frequency noise modulated slowly
        waves = np.random.randn(len(t)) * 0.15

        # Apply low-pass filter effect (simple moving average)
        window_size = int(self.sample_rate * 0.1)  # 100ms window
        waves = np.convolve(waves, np.ones(window_size)/window_size, mode='same')

        # Modulate with slow sine wave (like waves rolling)
        modulation = 0.5 + 0.5 * np.sin(2 * np.pi * 0.3 * t)
        waves *= modulation

        return waves * 0.4

    def _generate_flute(self, duration: float, bpm: float, t: np.ndarray) -> np.ndarray:
        """Generate flute-like sound for nature theme"""
        beat_interval = 60.0 / bpm
        flute = np.zeros(len(t))

        # High, gentle melody
        melody_notes = [523, 587, 659, 698, 784]  # C5, D5, E5, F5, G5

        num_measures = int(duration / (beat_interval * 4))

        for measure in range(num_measures):
            for beat in range(4):
                note_start_time = measure * beat_interval * 4 + beat * beat_interval
                note_start_sample = int(note_start_time * self.sample_rate)
                note_duration = beat_interval * 0.8
                note_samples = int(note_duration * self.sample_rate)

                if note_start_sample + note_samples < len(t):
                    note_t = t[note_start_sample:note_start_sample+note_samples] - note_start_time

                    # Pick note
                    freq = melody_notes[(measure * 4 + beat) % len(melody_notes)]

                    # Flute = mostly fundamental with little harmonics
                    note = (
                        np.sin(2 * np.pi * freq * note_t) * 1.0 +
                        np.sin(2 * np.pi * freq * 2 * note_t) * 0.3 +
                        np.sin(2 * np.pi * freq * 3 * note_t) * 0.1
                    )

                    # Gentle envelope
                    envelope = np.ones(len(note_t))
                    attack = int(0.05 * self.sample_rate)
                    release = int(0.1 * self.sample_rate)
                    envelope[:attack] = np.linspace(0, 1, attack)
                    envelope[-release:] = np.linspace(1, 0, release)

                    flute[note_start_sample:note_start_sample+note_samples] += note * envelope * 0.12

        return flute

    def _generate_hand_claps(self, duration: float, bpm: float) -> np.ndarray:
        """Generate hand clap sounds for crew theme"""
        samples = int(self.sample_rate * duration)
        claps = np.zeros(samples)

        beat_interval = 60.0 / bpm
        num_beats = int(duration / beat_interval)

        for i in range(num_beats):
            # Claps on beats 2 and 4 (with kick/snare pattern)
            if i % 4 in [1, 3]:
                clap_start = int(i * beat_interval * self.sample_rate)
                clap_length = int(0.05 * self.sample_rate)

                if clap_start + clap_length < samples:
                    # Clap = short noise burst with specific spectrum
                    clap_wave = np.random.randn(clap_length) * 0.6
                    # Apply envelope
                    clap_wave *= np.exp(-80 * np.linspace(0, 0.05, clap_length))
                    claps[clap_start:clap_start+clap_length] += clap_wave

        return claps

    def _generate_ambient(self, duration: float, t: np.ndarray) -> np.ndarray:
        """Generate mysterious ambient pad"""
        # Very low frequency drone with slow modulation
        ambient = (
            np.sin(2 * np.pi * 55 * t) * 0.3 +  # A1
            np.sin(2 * np.pi * 82.5 * t) * 0.2 +  # E2
            np.sin(2 * np.pi * 110 * t) * 0.15  # A2
        )

        # Slow LFO modulation
        lfo = 0.7 + 0.3 * np.sin(2 * np.pi * 0.2 * t)
        ambient *= lfo

        return ambient * 0.15
