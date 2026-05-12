from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from loguru import logger

from core.conf import settings

class MongoDB:
    
    def __init__(self) -> None:
        self.client: AsyncIOMotorClient | None = None
        self.db: AsyncIOMotorDatabase | None = None
    
    async def connect(self) -> None:
        logger.info("Connecting to MongoDB at {}:{}", settings.MONGO_HOST, settings.MONGO_PORT)
        self.client = AsyncIOMotorClient(
            settings.MONGO_URI,
            serverSelectionTimeoutMS=5000,
            maxPoolSize=10,
            minPoolSize=2
        )
        self.db = self.client[settings.MONGO_DB]
        # Verify connection is alive
        await self.client.admin.command("ping")
        logger.info("MongoDB connected - database: {}", settings.MONGO_DB)
        await self._create_indexes()
        
    async def disconnect(self) -> None:
        if self.client:
            self.client.close()
            logger.info("MongoDB disconnected")
    
    async def _create_indexes(self) -> None:
        db = self.db
        await db["servers"].create_index("name", unique=True)
        await db["servers"].create_index("status")
        await db["servers"].create_index("country")
        await db["servers"].create_index("os")
        await db["servers"].create_index("platform")
        await db["servers"].create_index("arch")
        await db["servers"].create_index([("created_at", -1)])
        # activities collection indexes
        await db["activities"].create_index([("timestamp", -1)])
        await db["activities"].create_index("server_id")
        logger.debug("MongoDB indexes verified")
        
    def get_db(self) -> AsyncIOMotorDatabase:
        if self.db is None:
            raise RuntimeError("MongoDB not connected. Call connect() first.")
        return self.db
    
mongodb = MongoDB()

async def get_db() -> AsyncIOMotorDatabase:
    """FastAPI dependency — inject database into route handlers."""
    return mongodb.get_db()