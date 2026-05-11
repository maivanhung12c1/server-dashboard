from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )
    
    ENVIRONMENT: Literal["dev", "prod"] = "dev"

    # FastAPI metadata
    PROJECT_NAME: str = "Server Dashboard API"
    PROJECT_VERSION: str = "1.0.0"

    # MongoDB
    MONGO_HOST: str = "localhost"
    MONGO_PORT: int = 27017
    MONGO_USER: str = "admin"
    MONGO_PASSWORD: str = "changeme"
    MONGO_DB: str = "server_dashboard"

    # App server
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    
    # CORS
    CORS_ORIGINS: list[str] = Field(default_factory=lambda: ["*"])

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_JSON: bool = False
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_PER_MINUTE: int = 100
    RATE_LIMIT_WRITE_PER_MINUTE: int = 20
    
    @property
    def MONGO_URI(self) -> str:
        if self.MONGO_USER and self.MONGO_PASSWORD:
            return (
                f"mongodb://{self.MONGO_USER}:{self.MONGO_PASSWORD}"
                f"@{self.MONGO_HOST}:{self.MONGO_PORT}/{self.MONGO_DB}"
                f"?authSource=admin"
            )
        return f"mongodb://{self.MONGO_HOST}:{self.MONGO_PORT}"
        
    @property
    def is_dev(self) -> bool:
        return self.ENVIRONMENT == "dev"
    
    @property
    def docs_url(self) -> str | None:
        return "/docs" if self.is_dev else None
    
    @property
    def redoc_url(self) -> str | None:
        return "/redoc" if self.is_dev else None
    
@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()