from typing import Dict
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    api_key: str = Field(validation_alias="KHAYA_API_KEY")
    base_url: str = "https://translation-api.ghananlp.org"
    endpoints: Dict[str, str] = {
        "translation": "https://translation-api.ghananlp.org/v1/translate",
        "tts": "https://translation-api.ghananlp.org/tts/v1/tts",
        "asr": "https://translation-api.ghananlp.org/asr/v1/transcribe",
    }
    timeout: int = 30
    retry_attempts: int = 3

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )
