from typing import ClassVar, List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import (
    AliasChoices,
    AmqpDsn,
    BaseModel,
    Field,
    ImportString,
    PostgresDsn,
    RedisDsn,
    model_validator,
    SecretStr,
)
import os


class Settings(BaseSettings):
    TOKEN: SecretStr
    DB_URL: str
    WHITELISTED_IDS: Optional[List[str]] = []
    API_SANDBOX_TOKEN: str
    API_LIVE_TOKEN: str

    @model_validator(mode="before")
    def split_whitelisted_ids(cls, values):
        whitelisted_ids = values.get("WHITELISTED_IDS", "")
        if isinstance(whitelisted_ids, str) and whitelisted_ids:
            # Разделяем строку на список, удаляя лишние пробелы
            values["WHITELISTED_IDS"] = [id.strip() for id in whitelisted_ids.split(",")]
        return values

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


# Load settings
settings = Settings()

