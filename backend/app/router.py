from fastapi import APIRouter

from app.server.api.v1 import server as server_api
from app.server.api.v1 import stats as stats_api
from app.server.api.v1 import activity as activity_api
from app.server.api.v1 import map as map_api

router = APIRouter(prefix="/api/v1")

router.include_router(server_api.router, prefix="/servers", tags=["Servers"])
router.include_router(stats_api.router, prefix="/stats", tags=["Statistics"])
router.include_router(activity_api.router, prefix="/activities", tags=["Activities"])
router.include_router(map_api.router, prefix="/map", tags=["Map"])
