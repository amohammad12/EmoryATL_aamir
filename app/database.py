"""
MongoDB database setup using Motor (async driver) and Beanie (ODM)
"""
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import logging
from app.config import settings

logger = logging.getLogger(__name__)

# MongoDB client (will be initialized on startup)
mongodb_client: AsyncIOMotorClient = None


async def connect_to_mongo():
    """Connect to MongoDB and initialize Beanie"""
    global mongodb_client

    try:
        logger.info(f"Connecting to MongoDB at {settings.MONGODB_URL}")

        # Create MongoDB client
        mongodb_client = AsyncIOMotorClient(settings.MONGODB_URL)

        # Get database
        database = mongodb_client[settings.MONGODB_DB_NAME]

        # Import models
        from app.models import Job, SongCache

        # Initialize Beanie with models
        await init_beanie(
            database=database,
            document_models=[Job, SongCache]
        )

        logger.info(f"Successfully connected to MongoDB database: {settings.MONGODB_DB_NAME}")

    except Exception as e:
        logger.error(f"Error connecting to MongoDB: {e}")
        raise


async def close_mongo_connection():
    """Close MongoDB connection"""
    global mongodb_client

    if mongodb_client:
        logger.info("Closing MongoDB connection")
        mongodb_client.close()
        logger.info("MongoDB connection closed")


def get_database():
    """
    Get MongoDB database instance

    Returns:
        MongoDB database
    """
    if mongodb_client is None:
        raise RuntimeError("MongoDB client not initialized. Call connect_to_mongo() first.")

    return mongodb_client[settings.MONGODB_DB_NAME]
