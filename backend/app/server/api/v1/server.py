from typing import Annotated

from fastapi import APIRouter, Depends, Query
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.server.schema.server import CreateServerParam, GetServerDetail, UpdateServerParam
from app.server.service.server_service import server_service
from common.pagination import PageData
from common.response.response_schema import ResponseModel, response_base
from database.mongodb import get_db

router = APIRouter()


@router.get("", summary="List servers with pagination and filters")
async def list_servers(
    db: Annotated[AsyncIOMotorDatabase, Depends(get_db)],
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=200),
    name: str | None = Query(default=None),
    status: str | None = Query(default=None, description="Online | Offline"),
    country: str | None = Query(default=None),
    os: str | None = Query(default=None),
    platform: str | None = Query(default=None),
) -> ResponseModel[PageData[GetServerDetail]]:
    data = await server_service.get_list(
        db,
        page=page,
        size=size,
        name=name,
        status=status,
        country=country,
        os=os,
        platform=platform,
    )
    return response_base.success(data=data)


@router.get("/{server_id}", summary="Get server by ID")
async def get_server(
    server_id: str,
    db: Annotated[AsyncIOMotorDatabase, Depends(get_db)],
) -> ResponseModel[GetServerDetail]:
    data = await server_service.get(db, server_id)
    return response_base.success(data=data)


@router.post("", summary="Create a new server", status_code=201)
async def create_server(
    body: CreateServerParam,
    db: Annotated[AsyncIOMotorDatabase, Depends(get_db)],
) -> ResponseModel[GetServerDetail]:
    data = await server_service.create(db, body)
    return response_base.success(data=data, msg="Server created successfully")


@router.put("/{server_id}", summary="Update server fields")
async def update_server(
    server_id: str,
    body: UpdateServerParam,
    db: Annotated[AsyncIOMotorDatabase, Depends(get_db)],
) -> ResponseModel[GetServerDetail]:
    data = await server_service.update(db, server_id, body)
    return response_base.success(data=data, msg="Server updated successfully")


@router.delete("/{server_id}", summary="Delete a server")
async def delete_server(
    server_id: str,
    db: Annotated[AsyncIOMotorDatabase, Depends(get_db)],
) -> ResponseModel[None]:
    await server_service.delete(db, server_id)
    return response_base.success(msg="Server deleted successfully")