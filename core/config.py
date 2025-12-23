#core/config.py

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # -------------------------------------------------
    # Environment
    # -------------------------------------------------
    ENV: str = Field(default="local", description="Environment name")
    DEBUG: bool = Field(default=False)

    # -------------------------------------------------
    # Database
    # -------------------------------------------------
    DATABASE_URL: str = Field(..., description="PostgreSQL connection URL")

    # -------------------------------------------------
    # External APIs
    # -------------------------------------------------
    API_KEY: str = Field(..., description="External API key")

    # -------------------------------------------------
    # SQLAlchemy tuning (optional but expected)
    # -------------------------------------------------
    DB_POOL_SIZE: int = Field(default=5)
    DB_MAX_OVERFLOW: int = Field(default=10)

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
