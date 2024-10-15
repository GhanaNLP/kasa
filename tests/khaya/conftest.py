import os

import pytest

from khaya.khaya_interface import KhayaInterface

khaya_api_key = os.getenv("khaya_api_key", "test_key")


@pytest.fixture
def khaya_interface():
    api_key = khaya_api_key
    return KhayaInterface(api_key)

# @pytest.fixture
# def audio_file():

#     audio_file_path = "tests/khaya/me_ho_ye.wav"

#     audio_data, sampling_rate
