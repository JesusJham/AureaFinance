from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # App
    APP_NAME: str = "Aurea Finance API"
    DEBUG: bool = False

    # JWT
    SECRET_KEY: str = "cambia-esta-clave-en-produccion"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:5500", "http://127.0.0.1:5500", "https://project-wk0hp.vercel.app"]

    # Base de datos interna (SQLite para dev, PostgreSQL para prod)
    DATABASE_URL: str = "sqlite:///./aurea.db"

    class Config:
        env_file = ".env"


settings = Settings()
