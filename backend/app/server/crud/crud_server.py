import re
import uuid
from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorDatabase

from utils.datetime_utils import utcnow


class CRUDServer:
    COLLECTION = "servers"

    async def get(self, db: AsyncIOMotorDatabase, server_id: str) -> dict | None:
        return await db[self.COLLECTION].find_one({"_id": server_id})

    async def get_by_name(self, db: AsyncIOMotorDatabase, name: str) -> dict | None:
        return await db[self.COLLECTION].find_one({"name": name})
    
    async def get_list(
        self,
        db: AsyncIOMotorDatabase,
        *,
        page: int = 1,
        size: int = 20,
        name: str | None = None,
        status: str | None = None,
        country: str | None = None,
        os: str | None = None,
        platform: str | None = None,
    ) -> tuple[list[dict], int]:
        filters: dict = {}
        if name:
            filters["name"] = {"$regex": re.escape(name), "$options": "i"}
        if status:
            filters["status"] = status
        if country:
            filters["country"] = {"$regex": re.escape(country), "$options": "i"}
        if os:
            filters["os"] = {"$regex": re.escape(os), "$options": "i"}
        if platform:
            filters["platform"] = {"$regex": re.escape(platform), "$options": "i"}
        
        skip = (page - 1) * size
        total = await db[self.COLLECTION].count_documents(filters)
        cursor = (
            db[self.COLLECTION]
            .find(filters)
            .sort("created_at", -1)
            .skip(skip)
            .limit(size)
        )
        items = await cursor.to_list(length=size)
        return items, total
    
    async def create(self, db: AsyncIOMotorDatabase, data: dict) -> dict:
        now = utcnow()
        doc = {
            "_id": str(uuid.uuid4()),
            **data,
            "created_at": now,
            "updated_at": now,
        }
        await db[self.COLLECTION].insert_one(doc)
        return doc
    
    async def update(
        self, db: AsyncIOMotorDatabase, server_id: str, data: dict
    ) -> dict | None:
        data["updated_at"] = utcnow()
        from pymongo import ReturnDocument
        return await db[self.COLLECTION].find_one_and_update(
            {"_id": server_id},
            {"$set": data},
            return_document=ReturnDocument.AFTER
        )
    
    async def delete(self, db: AsyncIOMotorDatabase, server_id: str) -> bool:
        result = await db[self.COLLECTION].delete_one({"_id": server_id})
        return result.deleted_count > 0
    
    async def count_total(self, db: AsyncIOMotorDatabase) -> int:
        return await db[self.COLLECTION].count_documents({})

    async def count_by_field(
        self, db: AsyncIOMotorDatabase, field: str, limit: int = 10
    ) -> list[dict]:
        pipeline = [
            {"$group": {"_id": f"${field}", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": limit},
        ]
        return await db[self.COLLECTION].aggregate(pipeline).to_list(length=limit)
    
    async def count_created_in_range(
        self, db: AsyncIOMotorDatabase, start: datetime, end: datetime
    ) -> int:
        return await db[self.COLLECTION].count_documents(
            {"created_at": {"$gte": start, "$lte": end}}
        )
    
    async def get_timeseries(
        self,
        db: AsyncIOMotorDatabase,
        start: datetime,
        end: datetime,
        group_by: str = "day",
    ) -> list[dict]:
        date_fmt = "%Y-%m-%d %H:00" if group_by == "hour" else "%Y-%m-%d"
        pipeline = [
            {"$match": {"created_at": {"$gte": start, "$lte": end}}},
            {
                "$group": {
                    "_id": {
                        "$dateToString": {"format": date_fmt, "date": "$created_at"}
                    },
                    "count": {"$sum": 1},
                }
            },
            {"$sort": {"_id": 1}},
        ]
        results = await db[self.COLLECTION].aggregate(pipeline).to_list(length=1000)
        return [{"date": r["_id"], "count": r["count"]} for r in results]
    
    async def get_map_data(self, db: AsyncIOMotorDatabase) -> list[dict]:
        pipeline = [
            {
                "$group": {
                    "_id": "$country",
                    "count": {"$sum": 1},
                    "servers": {
                        "$push": {
                            "id": "$_id",
                            "name": "$name",
                            "ip_address": "$ip_address",
                            "status": "$status",
                        }
                    }
                }
            },
            {"$sort": {"count": -1}},
        ]
        results = await db[self.COLLECTION].aggregate(pipeline).to_list(length=1000)
        return [
            {
                "country": r["_id"],
                "count": r["count"],
                "servers": r["servers"][:5],
            }
            for r in results
        ]
        

server_dao = CRUDServer()
