import uuid

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from utils.datetime_utils import utcnow


class CRUDActivity:
    COLLECTION = "activities"

    async def create(
        self,
        db: AsyncIOMotorDatabase,
        server_id: str,
        server_name: str,
        action: str,
        detail: str,
    ) -> dict:
        doc = {
            "_id": str(uuid.uuid4()),
            "server_id": server_id,
            server_name: server_name,
            "action": action,
            "detail": detail,
            "timestamp": utcnow(),
        }
        await db[self.COLLECTION].insert_one(doc)
        return doc
    
    async def get_recent(
        self, db: AsyncIOMotorDatabase, limit: int = 20
    ) -> list[dict]:
        cursor = (
            db[self.COLLECTION]
            .find({})
            .sort("timestamp", -1)
            .limit(limit)
        )
        return await cursor.to_list(length=limit)
    
    
activity_dao = CRUDActivity()