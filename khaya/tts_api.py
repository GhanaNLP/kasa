import json

from khaya.abstract_api import BASE_API


class TTSAPI(BASE_API):
    def synthesize(self, text: str, lang: str) -> bytes:
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
