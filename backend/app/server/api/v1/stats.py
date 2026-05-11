from datetime import datetime, timedelta, timezone
from typing import Annotated, Literal

from fastapi import APIRouter, Depends, Query
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.server.crud.crud_server import server_dao
from common.exception.errors import BadRequestError
from common.response.response_schema import ResponseModel, response_base
from database.mongodb import get_db

router = APIRouter()


@router.get("/overview", summary="Dashboard overview statistics")
async def get_overview_stats(
    db: Annotated[AsyncIOMotorDatabase, Depends(get_db)],
) -> ResponseModel[dict]:
    total = await server_dao.count_total(db)
    by_os = await server_dao.count_by_field(db, "os")
    by_platform = await server_dao.count_by_field(db, "platform")
    by_arch = await server_dao.count_by_field(db, "arch")
    by_status = await server_dao.count_by_field(db, "status")

    return response_base.success(data={
        "total_servers": total,
        "by_os": [{"name": r["_id"], "count": r["count"]} for r in by_os],
        "by_platform": [{"name": r["_id"], "count": r["count"]} for r in by_platform],
        "by_arch": [{"name": r["_id"], "count": r["count"]} for r in by_arch],
        "by_status": [{"name": r["_id"], "count": r["count"]} for r in by_status],
    })


@router.get("/timeseries", summary="Server creation over time")
async def get_timeseries_stats(
    db: Annotated[AsyncIOMotorDatabase, Depends(get_db)],
    range: Literal["24h", "7d", "30d", "custom"] = Query(default="7d"),
    start: str | None = Query(default=None, description="ISO 8601 start (custom range)"),
    end: str | None = Query(default=None, description="ISO 8601 end (custom range)"),
) -> ResponseModel[dict]:
    now = datetime.now(timezone.utc)

    if range == "24h":
        start_dt, end_dt, group_by = now - timedelta(hours=24), now, "hour"
    elif range == "7d":
        start_dt, end_dt, group_by = now - timedelta(days=7), now, "day"
    elif range == "30d":
        start_dt, end_dt, group_by = now - timedelta(days=30), now, "day"
    else:
        if not start or not end:
            raise BadRequestError("start and end are required for custom range")
        try:
            start_dt = datetime.fromisoformat(start).replace(tzinfo=timezone.utc)
            end_dt = datetime.fromisoformat(end).replace(tzinfo=timezone.utc)
        except ValueError:
            raise BadRequestError("Invalid date format. Use ISO 8601 (e.g. 2024-01-15)")
        group_by = "hour" if (end_dt - start_dt).days <= 2 else "day"

    total_all = await server_dao.count_total(db)
    new_in_range = await server_dao.count_created_in_range(db, start_dt, end_dt)
    timeseries = await server_dao.get_timeseries(db, start_dt, end_dt, group_by=group_by)

    return response_base.success(data={
        "range": range,
        "start": start_dt.isoformat(),
        "end": end_dt.isoformat(),
        "total_servers": total_all,
        "new_in_range": new_in_range,
        "timeseries": timeseries,
    })
