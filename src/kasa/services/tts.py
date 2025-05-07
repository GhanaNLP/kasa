import json

from requests.models import Response

from kasa.services.base_api import BaseApi
from kasa.exceptions import TTSGenerationError
from kasa.utils import check_authentication


class TtsService:
    def __init__(self, http_client: BaseApi):
        self.http_client = http_client
        self.endpoint = http_client.config.endpoints["tts"]

    @check_authentication
    def synthesize(self, text: str, lang: str) -> Response | dict[str, str]:
        """
        Convert text to speech in a specified African language using the GhanaNLP TTS API.

        Args:
            text (str): The text to convert to speech.
            lang (str): The language of the text.

        Returns:
            bytes: The synthesized audio. ## TODO: check the arguments for all documentation
        """
        if not text or not lang:
            raise TTSGenerationError("Text and language are required", 400)

        try:
            payload = json.dumps({"text": text, "language": lang})

            response = self.http_client.request("POST", self.endpoint, data=payload)
            return response
        except Exception as e:
            raise TTSGenerationError(str(e), 500)
