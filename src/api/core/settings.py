import secrets
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


class Settings(BaseSettings):
    """Config settings for app"""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # app config
    API_NAME: str = "Insightia Labs"
    API_VERSION: str = "1.0.0"

    # Environment Variable
    ENV: str = "development"

    # DB config
    DB_TYPE: str = ""
    DB_HOST: str = ""
    DB_USER: str = ""
    DB_PASSWORD: str = ""
    DB_PORT: str = ""
    DB_NAME: str = ""

    # Github variables
    GITHUB_CLIENT_ID: str = ""
    GITHUB_CLIENT_SECRET: str = ""
    GITHUB_USER_URL: str = ""
    GITHUB_TOKEN_URL: str = ""
    GITHUB_AUTHORIZE_URL: str = ""
    GITHUB_EMAIL_URL:str = ""

    # Security
    SECRET_KEY: str = secrets.token_hex(32)
    CSRF_MAX_AGE_SECONDS: int = 600
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 3
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7


settings = Settings()
