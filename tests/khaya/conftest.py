import os

import pytest
from dotenv import load_dotenv

from khaya import khayaAPI

# os.environ.pop("khaya_api_key", None)  # Remove the key if it exists

load_dotenv()
khaya_api_key = os.getenv("khaya_api_key", "test")


@pytest.fixture
def khaya_interface():
    api_key = khaya_api_key
    return khayaAPI(api_key)
