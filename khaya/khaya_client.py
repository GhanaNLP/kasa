from typing import Optional

from requests.models import Response

from khaya.services.base_api import BaseApi
from khaya.services.asr import AsrService
from khaya.services.translation import TranslationService
from khaya.services.tts import TtsService
from khaya.config import Settings

# custom type hint for Response or dict[str, str]
ResponseOrDict = Response | dict[str, str]


class KhayaClient:
    """
    KhayaInterface is a class that provides a high-level interface to the Khaya API.
    It provides methods for translating text, transcribing audio, and synthesizing speech.

    Args:
        api_key: The API key to use for authenticating requests to the Khaya API.
        base_url: The base URL of the Khaya API. Default is "https://translation-api.ghananlp.org".

    Returns:
        An instance of the KhayaInterface class.


    Example:

    ```python
    from khaya.khaya_client import KhayaClient

    import os

    # Initialize the Khaya API interface with your API key assuming you have one saved
    # in an environment variable called KHAYA_API_KEY

    api_key = os.environ.get("KHAYA_API_KEY")

    khaya = KhayaClient(api_key)

    # Translate text from English to Twi
    translation_response = khaya.translate("Hello, how are you?", "en-tw")
    print(translation_response.json())

    # Transcribe an audio file
    asr_response = khaya.transcribe("path/to/audio/file.wav", "tw")
    print(asr_response.json())

    # Synthesize speech
    tts_response = khaya.synthesize("Hello, how are you?", "en")
    # Save the synthesized speech to a file
    with open("output.mp3", "wb") as f:
        f.write(tts_response.content)
    ```

    """

    def __init__(
        self,
        api_key: str,
        config: Optional[Settings] = None,
    ):
        self.config = config if config else Settings(api_key=api_key)
        self.config.api_key = api_key
        self.http_client = BaseApi(self.config)
        self.translation = TranslationService(self.http_client, self.config)
        self.asr = AsrService(self.http_client, self.config)
        self.tts = TtsService(self.http_client, self.config)

    def translate(self, text: str, language_pair: str = "en-tw") -> ResponseOrDict:
        """
        Translate text from one language to another.

        Args:
            text: The text to translate.
            language_pair: The language pair to translate the text to. Default is "en-tw".

        Returns:
            A Response object containing the translated text.
        """

        return self.translation.translate(text, language_pair)

    def transcribe(self, audio_file_path: str, language: str = "tw") -> ResponseOrDict:
        """
        Get the transcription of an audio file from a given language.

        Args:
            audio_file_path: The path to the audio file to transcribe.
            language: The language of the audio file. Default is "tw".

        Returns:
            A Response object containing the transcription of the audio file.
        """
        return self.asr.transcribe(audio_file_path, language)

    def synthesize(self, text: str, lang: str) -> ResponseOrDict:
        """
        Synthesize speech from text.

        Args:
            text: The text to synthesize.
            lang: The language of the text. Default is "tw".

        Returns:
            A Response object containing the synthesized speech.
        """
        return self.tts.synthesize(text, lang)
