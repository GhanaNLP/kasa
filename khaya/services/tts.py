import json

from requests.models import Response

from khaya.services.base_api import BaseApi
from khaya.config import Settings


class TtsService:
    def __init__(self, http_client: BaseApi, config: Settings):
        self.http_client = http_client
        self.endpoint = config.endpoints["tts"]

    def synthesize(self, text: str, lang: str) -> Response | dict[str, str]:
        """
        Convert text to speech in a specified African language using the GhanaNLP TTS API.

        Args:
            text (str): The text to convert to speech.
            lang (str): The language of the text.

        Returns:
            bytes: The synthesized audio.
        """
        payload = json.dumps({"text": text, "language": lang})

        response = self.http_client.request("POST", self.endpoint, data=payload)
        return response
