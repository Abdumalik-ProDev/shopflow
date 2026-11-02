"""Application configuration loaded from environment variables."""

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "ShopFlow"
    APP_VERSION: str = "0.1.0"
    ENVIRONMENT: str = Field(default="development")
    DEBUG: bool = Field(default=False)

    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://shopflow:shopflow@localhost:5432/shopflow"
    )

    @computed_field
    @property
    def database_url(self) -> str:
        return self.DATABASE_URL

    SECRET_KEY: str = Field(default="dev-secret-change-in-production-super-safe-shopflow")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    REDIS_URL: str = Field(default="redis://localhost:6379/0")
    CORS_ORIGINS: str = Field(default="http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173")
    MLFLOW_TRACKING_URI: str = Field(default="http://localhost:5000")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
