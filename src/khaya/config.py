from typing import Dict, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from src.khaya.constants import TIMEOUT, RETRY_ATTEMPTS


class Settings(BaseSettings):
    api_key: Optional[str] = Field(default=None)
    base_url: str = "https://translation-api.ghananlp.org"
    timeout: int = TIMEOUT
    retry_attempts: int = RETRY_ATTEMPTS

    model_config = SettingsConfigDict(
        env_file=None, extra="ignore", populate_by_name=True
    )

    @property
    def endpoints(self) -> Dict[str, str]:
        return {
            "translation": f"{self.base_url}/v1/translate",
            "tts": f"{self.base_url}/tts/v1/tts",
            "asr": f"{self.base_url}/asr/v1/transcribe",
        }


class DevSettings(Settings):
    # development settings: automatically load from a .env file
    api_key: Optional[str] = Field(default=None, alias="KHAYA_API_KEY")
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )
