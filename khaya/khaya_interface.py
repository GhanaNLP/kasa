from typing import Optional

from requests.models import Response

from khaya.asr_api import ASRAPI
from khaya.translation_api import TranslationAPI
from khaya.tts_api import TTSAPI


class KhayaInterface:

    def __init__(self, api_key: str, base_url: Optional[str] = "https://translation-api.ghananlp.org"):
        self.api_key = api_key
        self.base_url = base_url
        self.translation_api = TranslationAPI(api_key, base_url)
        self.asr_api = ASRAPI(api_key, base_url)
        self.tts_api = TTSAPI(api_key, base_url)

    def translate(self, text: str, language_pair: str = "en-tw") -> Response:
        return self.translation_api.translate(text, language_pair)

    def asr(self, audio_file_path: str, language: str = "tw") -> Response:
        return self.asr_api.transcribe(audio_file_path, language)

    def tts(self, text, lang) -> Response:
        return self.tts_api.synthesize(text, lang)
