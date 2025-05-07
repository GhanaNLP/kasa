from dotenv import load_dotenv


from kasa.config import Settings, DevSettings
from kasa.constants import TIMEOUT, RETRY_ATTEMPTS


def test_default_config(monkeypatch):
    # clear the environment variable that may be set
    monkeypatch.delenv("KHAYA_API_KEY", raising=False)

    # set temporary environment variable
    api_key = "test_api_key"

    config = Settings(api_key=api_key)
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

    load_dotenv(dotenv_path=str(env_file))

    # Set the environment variable using monkeypatch
    monkeypatch.setenv("KHAYA_API_KEY", "test_api_key")

    # load settings using the .env file
    config = DevSettings(_env_file=str(env_file))

    assert config.api_key == "test_api_key"
