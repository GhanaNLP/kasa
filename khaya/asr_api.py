from requests.models import Response

from khaya.base_api import BaseApi


class AsrApi(BaseApi):
    def transcribe(self, audio_file_path: str, language="tw") -> Response:
        """
        Convert speech to text from audio binary data in an African language using the GhanaNLP STT API.

        Args:
            audio_file_path (str): The path to the audio file.
            language (str): The language of the audio file.

        Returns:
            dict: The transcribed text.
        """

        url = f"{self.base_url}/asr/v1/transcribe?language={language}"
        with open(audio_file_path, "rb") as db:
            data = db.read()

        self.headers["Content-Type"] = "audio/wav"

        response = self._make_request("POST", url, data=data)
        return response
