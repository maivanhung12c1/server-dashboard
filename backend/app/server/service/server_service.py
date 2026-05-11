from motor.motor_asyncio import AsyncIOMotorDatabase

from app.server.crud.crud_activity import activity_dao
from app.server.crud.crud_server import server_dao
from app.server.schema.server import CreateServerParam, GetServerDetail, UpdateServerParam
from common.exception.errors import ConflictError, NotFoundError
from common.pagination import PageData


class ServerService:
    
    @staticmethod
    async def get(db: AsyncIOMotorDatabase, server_id: str) -> GetServerDetail:
        doc = await server_dao.get(db, server_id)
        if not doc:
            raise NotFoundError(f"Server '{server_id}' not found")
        return GetServerDetail.from_doc(doc)
    
    @staticmethod
    async def get_list(
        db: AsyncIOMotorDatabase,
        *,
        page: int,
        size: int,
        name: str | None = None,
        status: str | None = None,
        country: str | None = None,
        os: str | None = None,
        platform: str | None = None,
    ) -> PageData[GetServerDetail]:
        items, total = await server_dao.get_list(
            db,
            page=page,
            size=size,
            name=name,
            status=status,
            country=country,
            os=os,
            platform=platform,          
        )
        return PageData.create(
            items=[GetServerDetail.from_doc(doc) for doc in items],
            total=total,
            page=page,
            size=size,
        )
    
    @staticmethod
    async def create(db: AsyncIOMotorDatabase, obj: CreateServerParam) -> GetServerDetail:
        if await server_dao.get_by_name(db, obj.name):
            raise ConflictError(f"Server with name '{obj.name}' already exists")
        
        doc = await server_dao.create(db, obj.model_dump())
        await activity_dao.create(
            db,
            server_id=doc["_id"],
            server_name=doc["name"],
            action="created",
            detail=f"Server '{doc['name']}' was created",
        )
        return GetServerDetail.from_doc(doc)

        
    @staticmethod
    async def update(
        db: AsyncIOMotorDatabase, server_id: str, obj: UpdateServerParam
    ) -> GetServerDetail:
        existing = await server_dao.get(db, server_id)
        if not existing:
            raise NotFoundError(f"Server '{server_id}' not found")
        
        if obj.name and obj.name != existing["name"]:
            if await server_dao.get_by_name(db, obj.name):
                raise ConflictError(f"Server with name '{obj.name}' already exists")
        
        update_data = {
            k: v for k, v in obj.model_dump().items() if v is not None
        }
        
        changed_fields = []

        for field, new_value in update_data.items():
            old_value = existing.get(field)

            if old_value != new_value:
                changed_fields.append(
                    f"{field}: '{old_value}' -> '{new_value}'"
                )
        
        doc = await server_dao.update(db, server_id, update_data)
        
        if changed_fields:
            detail = (
                f"Server '{doc['name']}' updated: "
                + ", ".join(changed_fields)
            )
        else:
            detail = f"Server '{doc['name']}' updated"
        
        await activity_dao.create(
            db,
            server_id=doc["_id"],
            server_name=doc["name"],
            action="updated",
            detail=detail,
        )  
        return GetServerDetail.from_doc(doc)

    @staticmethod
    async def delete(db: AsyncIOMotorDatabase, server_id: str) -> None:
        existing = await server_dao.get(db, server_id)
        if not existing:
            raise NotFoundError(f"Server '{server_id}' not found")
        
        server_name = existing["name"]
        await server_dao.delete(db, server_id)
        await activity_dao.create(
            db,
            server_id=server_id,
            server_name=server_name,
            action="deleted",
            detail=f"Server '{server_name}' was removed",
        )

server_service = ServerService()