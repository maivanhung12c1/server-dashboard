from typing import Annotated

from fastapi import APIRouter, Depends, Query
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.server.crud.crud_activity import activity_dao
from app.server.schema.activity import GetActivityDetail
from common.response.response_schema import ResponseModel, response_base
from database.mongodb import get_db

router = APIRouter()


@router.get("", summary="Get recent activity log")
async def get_activities(
    db: Annotated[AsyncIOMotorDatabase, Depends(get_db)],
    limit: int = Query(default=20, ge=1, le=100),
) -> ResponseModel[list[GetActivityDetail]]:
    docs = await activity_dao.get_recent(db, limit=limit)
    return response_base.success(data=[GetActivityDetail.from_doc(d) for d in docs])
