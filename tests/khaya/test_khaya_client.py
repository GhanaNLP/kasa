import pytest

from src.khaya import KhayaClient
from src.khaya.exceptions import (
    ASRTranscriptionError,
    TranslationError,
    TTSGenerationError,
)


@pytest.mark.parametrize(
    "task, input, lang",
    [
        ("translate", "Hello", "en-tw"),
        ("transcribe", "tests/khaya/me_ho_ye.wav", "tw"),
        ("synthesize", "Hello", "tw"),
    ],
)
def test_invalid_api_key(task, input, lang):
    invalid_api_key = "invalid_api_key"
    khaya_interface = KhayaClient(invalid_api_key)

    # execute the task
    result = getattr(khaya_interface, task)(input, lang)

    assert "401 Access Denied" in result["message"]


def test_translate_valid(khaya_interface):
    text = "Hello"
    translation_pair = "en-tw"

    result = khaya_interface.translate(text, translation_pair)

    assert result.status_code == 200
    assert result.text is not None
    assert "error" not in result.text.lower()


def test_translate_error(khaya_interface):
    text = "Hello"
    wrong_translation_pair = "en-fw"

    result = khaya_interface.translate(text, wrong_translation_pair)

    assert "error" in result.text.lower()


def test_translate_empty_text(khaya_interface):
    text = ""
    translation_pair = "en-tw"

    with pytest.raises(TranslationError):
        result = khaya_interface.translate(text, translation_pair)

        assert "error" in result.text.lower()


def test_tts_valid(khaya_interface):
    text = "Hello"
    lang = "tw"

    result = khaya_interface.synthesize(text, lang)

    assert result.status_code == 200
    assert isinstance(result.content, bytes)
    assert "error" not in result.text.lower()


def test_tts_error(khaya_interface):
    text = "Hello"
    wrong_lang = "fw"

    result = khaya_interface.synthesize(text, wrong_lang)

    assert "error" in result.text.lower()


def test_tts_empty_text(khaya_interface):
    text = ""
    lang = "tw"

    with pytest.raises(TTSGenerationError):
        result = khaya_interface.synthesize(text, lang)

        assert "error" in result.text.lower()


def test_asr_valid(khaya_interface):
    audio_file_path = "tests/khaya/me_ho_ye.wav"

    result = khaya_interface.transcribe(audio_file_path, "tw")

    assert result.status_code == 200
    assert "error" not in result.text.lower()
    assert result.json() == "me ho yɛ"


def test_asr_error_invalid_language(khaya_interface):
    audio_file_path = "tests/khaya/me_ho_ye.wav"
    wrong_lang = "fw"

    result = khaya_interface.transcribe(audio_file_path, wrong_lang)

    assert "error" in result["message"].lower()


def test_asr_error_nonexistent_file(khaya_interface):
    audio_file_path = "tests/khaya/nonexistent.wav"

    with pytest.raises(ASRTranscriptionError):
        result = khaya_interface.transcribe(audio_file_path, "tw")

        assert "error" in result["message"].lower()
