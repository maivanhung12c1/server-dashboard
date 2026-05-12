import sys
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger

from common.exception.errors import BaseAppError
from common.response.response_schema import ResponseModel
from core.conf import settings
from database.mongodb import mongodb
from middleware.request_id import RequestIDMiddleware
from middleware.request_log import RequestLogMiddleware


def _configure_logging() -> None:
    logger.remove()
    if settings.LOG_JSON:
        logger.add(sys.stdout, serialize=True, level=settings.LOG_LEVEL)
    else:
        fmt = (
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{line}</cyan> — <level>{message}</level>"
        )
        logger.add(sys.stdout, format=fmt, level=settings.LOG_LEVEL, colorize=True) 
    

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    _configure_logging()
    logger.info("starting {} v{}", settings.PROJECT_NAME, settings.PROJECT_VERSION)
    await mongodb.connect()
    logger.info("Application startup complete")
    yield
    logger.info("Shutting down...")
    await mongodb.disconnect()
    
    
def register_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.PROJECT_VERSION,
        docs_url=settings.docs_url,
        redoc_url=settings.redoc_url,
        lifespan=lifespan,
    )
    _register_middleware(app)
    _register_routers(app)
    _register_exception_handlers(app)
    return app


def _register_middleware(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(RequestLogMiddleware)
    app.add_middleware(RequestIDMiddleware)


def _register_routers(app: FastAPI) -> None:
    from app.router import router
    app.include_router(router)
    
    # @app.get("/health", tags=["System"])
    # async def health_check() -> dict:
    #     return {"status": "ok", "version": settings.PROJECT_VERSION}
    @app.get("/health", tags=["System"])                                                                                                                                                                                                                  
    async def health_check() -> JSONResponse:
        db_ok = await mongodb.ping()                                                                                                                                                                                                                      
        if not db_ok:                                                                                                                                                                                                                                     
            return JSONResponse(
                status_code=503,  # Service Unavailable                                                                                                                                                                                                   
                content={
                    "status": "degraded",
                    "db": "unreachable",                                                                                                                                                                                                                  
                    "version": settings.PROJECT_VERSION,
                },                                                                                                                                                                                                                                        
            )       
        return JSONResponse(
            status_code=200,                                                                                                                                                                                                                              
            content={"status": "ok", "version": settings.PROJECT_VERSION},
        )  


def _register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(BaseAppError)
    async def app_error_handler(request: Request, exc: BaseAppError) -> JSONResponse:
        rid = getattr(request.state, "request_id", None)
        return JSONResponse(
            status_code=exc.http_status,
            content=ResponseModel(code=exc.code, msg=exc.msg).model_dump(),
            headers={"X-Request-ID": rid} if rid else {},
        )
    
    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        errors = exc.errors()
        first = errors[0] if errors else {}
        field = " -> ".join(str(loc) for loc in first.get("loc", []))
        msg = f"Validation error on '{field}': {first.get('msg', 'invalid')}"
        return JSONResponse(
            status_code=422,
            content=ResponseModel(code=422, msg=msg).model_dump(),
        )
    
    @app.exception_handler(Exception)
    async def unhandled_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.exception("Unhandled exception on {} {}", request.method, request.url.path)
        return JSONResponse(
            status_code=500,
            content=ResponseModel(code=500, msg="Internal server error").model_dump(),
        )