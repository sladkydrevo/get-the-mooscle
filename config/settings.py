from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

from .session_models import FlaskConfig, MySQLConfig

ENV_PATH = Path.cwd() / ".env"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_nested_max_split=2
    )

    DEBUG: bool
    LOG_LEVEL: str

    DATA_FOLDER: str

    mysql: MySQLConfig
    flask: FlaskConfig


def get_settings() -> Settings:
    return Settings()


settings = get_settings()