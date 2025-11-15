"""
Celery tasks for async song generation
"""
from celery import Celery
import logging
from typing import Dict, Any
from app.config import settings
from app.services import (
    get_kid_friendly_rhymes,
    LyricsGenerator,
    VocalGenerator,
    AudioService,
    KaraokeGenerator,
    PirateBeatGenerator,
    MoodAnalyzer
)

logger = logging.getLogger(__name__)

# Initialize Celery
celery_app = Celery(
    'pirate_karaoke',
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)


@celery_app.task(bind=True)
def generate_song_task(self, word: str) -> Dict[str, Any]:
    """
    Background task for complete song generation pipeline

    Args:
        word: The input word to generate a shanty about

    Returns:
        Dictionary with song data (lyrics, audio_url, timings, etc.)
    """
    try:
        logger.info(f"Starting song generation for word: '{word}'")

        # Update progress: 10%
        self.update_state(state='PROGRESS', meta={'progress': 10, 'status': 'Generating rhymes...'})

        # Step 1: Generate rhyming words
        rhymes = get_kid_friendly_rhymes(word, count=6)

        if not rhymes or len(rhymes) < 2:
            raise ValueError(f"Not enough rhymes found for word '{word}'")

        logger.info(f"Found rhymes: {rhymes}")

        # Update progress: 20%
        self.update_state(state='PROGRESS', meta={'progress': 20, 'status': 'Writing pirate shanty...'})

        # Step 2: Generate lyrics with Gemini
        lyrics_gen = LyricsGenerator()
        lyrics_data = lyrics_gen.generate_pirate_shanty(word, rhymes)

        logger.info(f"Generated lyrics:\n{lyrics_data['lyrics']}")

        # Update progress: 40%
        self.update_state(state='PROGRESS', meta={'progress': 40, 'status': 'Recording vocals...'})

        # Step 3: Generate singing vocals with Bark TTS
        vocal_gen = VocalGenerator()
        vocal_path = vocal_gen.generate_vocals(lyrics_data['lyrics'])

        logger.info(f"Vocals generated: {vocal_path}")

        # Update progress: 55%
        self.update_state(state='PROGRESS', meta={'progress': 55, 'status': 'Analyzing mood and BPM...'})

        # Step 4: Analyze mood and detect BPM
        audio_service = AudioService()
        vocal_bpm = audio_service.detect_bpm(vocal_path)

        mood_analyzer = MoodAnalyzer()
        mood_analysis = mood_analyzer.analyze_lyrics(lyrics_data['lyrics'])
        energy = mood_analyzer.adjust_energy_for_bpm(mood_analysis['energy'], vocal_bpm)

        logger.info(f"Mood: {mood_analysis['mood'].value}, Energy: {energy:.2f}, BPM: {vocal_bpm:.1f}")

        # Update progress: 60%
        self.update_state(state='PROGRESS', meta={'progress': 60, 'status': 'Generating themed instrumental...'})

        # Step 5: Generate themed instrumental
        # First check if we have a pre-made beat in library
        instrumental_path = audio_service.get_instrumental(vocal_path, genre="pirate-shanty")

        if not instrumental_path:
            # No pre-made beat found, generate one dynamically!
            logger.info(f"No pre-made beat found, generating themed instrumental for '{word}'...")

            beat_gen = PirateBeatGenerator()
            instrumental_path = beat_gen.generate_beat(
                word=word,
                duration=lyrics_data['estimated_duration'] + 2,  # Add 2s buffer
                bpm=vocal_bpm,
                energy=energy
            )

            logger.info(f"Generated themed instrumental: {instrumental_path}")
        else:
            logger.info(f"Using pre-made instrumental: {instrumental_path}")

        # Update progress: 75%
        self.update_state(state='PROGRESS', meta={'progress': 75, 'status': 'Mixing vocals with instrumental...'})

        # Step 6: Mix vocals and instrumental
        final_audio_path = audio_service.mix_audio(vocal_path, instrumental_path)

        logger.info(f"Mixed audio: {final_audio_path}")

        # Update progress: 85%
        self.update_state(state='PROGRESS', meta={'progress': 85, 'status': 'Creating karaoke timings...'})

        # Step 7: Generate karaoke timings
        karaoke_gen = KaraokeGenerator()
        timings = karaoke_gen.generate_word_timings(final_audio_path, lyrics_data['lyrics'])

        logger.info(f"Generated {len(timings)} karaoke timings")

        # Update progress: 95%
        self.update_state(state='PROGRESS', meta={'progress': 95, 'status': 'Finalizing...'})

        # Step 8: Get final metadata
        duration = audio_service.get_audio_duration(final_audio_path)
        bpm = audio_service.detect_bpm(final_audio_path)

        # Build result
        result = {
            "word": word,
            "lyrics": lyrics_data['lyrics'],
            "audio_url": f"/outputs/{final_audio_path.split('/')[-1]}",
            "audio_path": final_audio_path,
            "timings": timings,
            "duration": duration,
            "bpm": bpm,
            "rhymes_used": rhymes
        }

        logger.info(f"Song generation completed successfully for '{word}'")

        return result

    except Exception as e:
        logger.error(f"Song generation failed for '{word}': {e}", exc_info=True)
        # Let Celery handle the FAILURE state automatically
        raise


@celery_app.task
def cleanup_old_files():
    """
    Periodic task to cleanup old temporary and output files
    Run this daily via celery beat
    """
    import os
    import time
    from pathlib import Path

    try:
        logger.info("Running cleanup task...")

        # Cleanup temp files older than 24 hours
        temp_dir = settings.TEMP_DIR
        cutoff_time = time.time() - (24 * 60 * 60)  # 24 hours ago

        deleted_count = 0
        for file_path in temp_dir.glob("*"):
            if file_path.is_file():
                if file_path.stat().st_mtime < cutoff_time:
                    file_path.unlink()
                    deleted_count += 1
                    logger.debug(f"Deleted old temp file: {file_path}")

        logger.info(f"Cleanup complete: deleted {deleted_count} old files")

    except Exception as e:
        logger.error(f"Cleanup task failed: {e}")
        raise
