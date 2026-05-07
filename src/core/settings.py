from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    """Config settings for app"""

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        extra="ignore"
        )

    # app config
    API_NAME: str = ""
    API_VERSION: str = ""

    # Environment Variable
    ENV: str = "development"
    TESTING: bool = False

    # DB config
    DB_TYPE: str = ""
    DB_HOST: str = ""
    DB_USER: str = ""
    DB_PASSWORD: str = ""
    DB_PORT: str = ""
    DB_NAME: str = ""


settings = Settings()
