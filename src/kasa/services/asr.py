from requests.models import Response

from kasa.services.base_api import BaseApi
from kasa.exceptions import ASRTranscriptionError
from kasa.utils import check_authentication


class AsrService:
    def __init__(self, http_client: BaseApi):
        self.http_client = http_client
        self.endpoint = http_client.config.endpoints["asr"]

    @check_authentication
    def transcribe(
        self, audio_file_path: str, language="tw"
    ) -> Response | dict[str, str]:
        """
        Convert speech to text from audio binary data in an African language using the GhanaNLP STT API.

        Args:
            audio_file_path (str): The path to the audio file.
            language (str): The language of the audio file.

        Returns:
            dict: The transcribed text.
        """
        try:
            url = f"{self.endpoint}?language={language}"
            with open(audio_file_path, "rb") as db:
                data = db.read()

            # self.http_client.headers["Content-Type"] = "audio/wav"

            response = self.http_client.request("POST", url, data=data)
            return response
        except Exception as e:
            raise ASRTranscriptionError(str(e), 500)
