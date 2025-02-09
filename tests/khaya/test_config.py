import os
import tempfile

import pytest

from khaya.config import Settings
from khaya.constants import TIMEOUT, RETRY_ATTEMPTS


def test_default_config(monkeypatch):
    # clear the environment variable that may be set
    monkeypatch.delenv("KHAYA_API_KEY", raising=False)

    # set temporary environment variable
    monkeypatch.setenv("KHAYA_API_KEY", "test_api_key")

    config = Settings()
    assert config.api_key == "test_api_key"
    assert config.base_url == "https://translation-api.ghananlp.org"
    assert "translation" in config.endpoints
    assert "asr" in config.endpoints
    assert "tts" in config.endpoints

    assert config.timeout == TIMEOUT
    assert config.retry_attempts == RETRY_ATTEMPTS


def test_config_from_env_file(tmp_path, monkeypatch):
    # clear the environment variable that may be set
    monkeypatch.delenv("KHAYA_API_KEY", raising=False)
    # create a temporary environment file
    env_file = tmp_path / ".env"
    env_file.write_text("KHAYA_API_KEY=test_api_key")
    # set the environment file path
    monkeypatch.setenv("KHAYA_ENV_FILE", str(env_file))

    # load settings using the .env file
    config = Settings(_env_file=str(env_file))

    assert config.api_key == "test_api_key"
