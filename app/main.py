"""
FastAPI application for Pirate Karaoke Backend with MongoDB
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from celery.result import AsyncResult
import logging
import uuid
from typing import Optional, Dict, Any

from app.config import settings
from app.database import connect_to_mongo, close_mongo_connection
from app.models import Job, SongCache
from app.tasks import generate_song_task
from app.services.rhyme_service import validate_word

# Configure logging
logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Pirate Karaoke API",
    description="Generate pirate-themed sea shanty karaoke songs for kids",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for outputs
app.mount("/outputs", StaticFiles(directory=str(settings.OUTPUT_DIR)), name="outputs")


# Pydantic models
class GenerateRequest(BaseModel):
    """Request model for song generation"""
    word: str


class JobResponse(BaseModel):
    """Response model for job status"""
    job_id: str
    status: str
    progress: Optional[int] = 0
    error: Optional[str] = None
    result: Optional[Dict[str, Any]] = None


class SongResponse(BaseModel):
    """Response model for song data"""
    word: str
    lyrics: str
    audio_url: str
    timings: list
    duration: float
    bpm: float


# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Initialize MongoDB connection on startup"""
    logger.info("Starting Pirate Karaoke API...")
    await connect_to_mongo()
    logger.info("MongoDB connected and ready")


@app.on_event("shutdown")
async def shutdown_event():
    """Close MongoDB connection on shutdown"""
    logger.info("Shutting down Pirate Karaoke API...")
    await close_mongo_connection()


# API endpoints
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Ahoy! Welcome to Pirate Karaoke API",
        "version": "1.0.0",
        "database": "MongoDB",
        "endpoints": {
            "generate": "POST /api/generate",
            "job_status": "GET /api/jobs/{job_id}",
            "cache": "GET /api/cache/{word}"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "pirate-karaoke", "database": "mongodb"}


@app.post("/api/generate", response_model=JobResponse)
async def generate_song(request: GenerateRequest):
    """
    Start async song generation

    Args:
        request: GenerateRequest with word field

    Returns:
        JobResponse with job_id for polling
    """
    try:
        word = request.word.strip().lower()

        # Validate word
        if not validate_word(word):
            raise HTTPException(
                status_code=400,
                detail="Invalid word. Please provide a single, simple English word."
            )

        logger.info(f"Received generation request for word: '{word}'")

        # Check cache first
        cached_song = await SongCache.find_one(SongCache.word == word)

        if cached_song:
            logger.info(f"Found cached song for '{word}'")
            return JobResponse(
                job_id="cached",
                status="completed",
                progress=100,
                result={
                    "word": cached_song.word,
                    "lyrics": cached_song.lyrics,
                    "audio_url": cached_song.audio_url,
                    "timings": cached_song.timings,
                    "duration": cached_song.duration,
                    "bpm": cached_song.bpm
                }
            )

        # Start Celery task FIRST to get task ID
        task = generate_song_task.delay(word)
        job_id = task.id  # Use Celery task ID as job_id

        # Save job to MongoDB with Celery task ID
        job = Job(
            job_id=job_id,
            word=word,
            status="processing",
            progress=0
        )
        await job.insert()

        logger.info(f"Created job {job_id} for word '{word}'")

        return JobResponse(
            job_id=job_id,
            status="processing",
            progress=0
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in generate_song: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/jobs/{job_id}", response_model=JobResponse)
async def get_job_status(job_id: str):
    """
    Get job status by ID

    Args:
        job_id: Job identifier

    Returns:
        JobResponse with current status and result if completed
    """
    try:
        # Handle cached responses
        if job_id == "cached":
            raise HTTPException(status_code=400, detail="Cached response, no job to poll")

        # Get job from MongoDB
        job = await Job.find_one(Job.job_id == job_id)

        if not job:
            raise HTTPException(status_code=404, detail="Job not found")

        # Check if we need to update from Celery
        if job.status == "processing":
            # Try to get Celery task result
            task = AsyncResult(job_id, app=generate_song_task.app)

            if task.state == 'PENDING':
                job.progress = 0
            elif task.state == 'PROGRESS':
                if task.info:
                    job.progress = task.info.get('progress', 0)
            elif task.state == 'SUCCESS':
                job.status = "completed"
                job.progress = 100
                job.result = task.result

                # Cache the result
                if task.result and 'word' in task.result:
                    # Check if already cached
                    existing_cache = await SongCache.find_one(SongCache.word == task.result['word'])

                    if not existing_cache:
                        cache_entry = SongCache(
                            word=task.result['word'],
                            lyrics=task.result['lyrics'],
                            audio_url=task.result['audio_url'],
                            timings=task.result['timings'],
                            duration=task.result['duration'],
                            bpm=task.result['bpm']
                        )
                        await cache_entry.insert()

            elif task.state == 'FAILURE':
                job.status = "failed"
                job.error = str(task.info)

            # Update job in database
            job.updated_at = datetime.utcnow()
            await job.save()

        return JobResponse(
            job_id=job.job_id,
            status=job.status,
            progress=job.progress,
            error=job.error,
            result=job.result
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting job status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/cache/{word}", response_model=SongResponse)
async def get_cached_song(word: str):
    """
    Get cached song by word

    Args:
        word: The word to search for

    Returns:
        SongResponse with cached song data
    """
    try:
        word = word.strip().lower()

        cached_song = await SongCache.find_one(SongCache.word == word)

        if not cached_song:
            raise HTTPException(status_code=404, detail="Song not found in cache")

        return SongResponse(
            word=cached_song.word,
            lyrics=cached_song.lyrics,
            audio_url=cached_song.audio_url,
            timings=cached_song.timings,
            duration=cached_song.duration,
            bpm=cached_song.bpm
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting cached song: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/cache/{word}")
async def delete_cached_song(word: str):
    """
    Delete cached song by word

    Args:
        word: The word to delete

    Returns:
        Success message
    """
    try:
        word = word.strip().lower()

        cached_song = await SongCache.find_one(SongCache.word == word)

        if not cached_song:
            raise HTTPException(status_code=404, detail="Song not found in cache")

        await cached_song.delete()

        logger.info(f"Deleted cached song for word '{word}'")

        return {"message": f"Deleted cached song for '{word}'"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting cached song: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Import datetime for job updates
from datetime import datetime


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
