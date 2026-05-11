from typing import Annotated

from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.server.crud.crud_server import server_dao
from common.response.response_schema import ResponseModel, response_base
from database.mongodb import get_db

router = APIRouter()


@router.get("", summary="Server distribution by country for world map")
async def get_map_data(
    db: Annotated[AsyncIOMotorDatabase, Depends(get_db)],
) -> ResponseModel[list[dict]]:
    data = await server_dao.get_map_data(db)
    return response_base.success(data=data)