import os

import pytest
from dotenv import load_dotenv

from khaya import KhayaClient

# os.environ.pop("khaya_api_key", None)  # Remove the key if it exists

load_dotenv()
khaya_api_key = os.getenv("KHAYA_API_KEY", "test")


@pytest.fixture
def khaya_interface():
    api_key = khaya_api_key
    print(api_key)
    return KhayaClient(api_key)
