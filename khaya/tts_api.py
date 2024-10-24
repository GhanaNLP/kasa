import json

from requests.models import Response

from khaya.base_api import BaseApi


class TtsApi(BaseApi):
    def synthesize(self, text: str, lang: str) -> Response | dict[str, str]:
        """
        Convert text to speech in a specified African language using the GhanaNLP TTS API.

        Args:
            text (str): The text to convert to speech.
            lang (str): The language of the text.

        Returns:
            bytes: The synthesized audio.
        """
        url = f"{self.base_url}/tts/v1/tts"

        payload = json.dumps({"text": text, "language": lang})

        response = self._make_request("POST", url, data=payload)
        return response
