from typing import Optional

from requests.models import Response

from khaya.asr_api import AsrApi
from khaya.translation_api import TranslationApi
from khaya.tts_api import TtsApi

# custom type hint for Response or dict[str, str]
ResponseOrDict = Response | dict[str, str]

class KhayaInterface:
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
    from khaya.khaya_interface import KhayaInterface

    import os

    # Initialize the Khaya API interface with your API key assuming you have one saved 
    # in an environment variable called KHAYA_API_KEY

    api_key = os.environ.get("KHAYA_API_KEY")

    khaya = KhayaInterface(api_key)

    # Translate text from English to Twi
    translation_response = khaya.translate("Hello, how are you?", "en-tw")
    print(translation_response.json())

    # Transcribe an audio file
    asr_response = khaya.asr("path/to/audio/file.wav", "tw")
    print(asr_response.json())

    # Synthesize speech
    tts_response = khaya.tts("Hello, how are you?", "en")
    # Save the synthesized speech to a file
    with open("output.mp3", "wb") as f:
        f.write(tts_response.content)
    ```

    """

    def __init__(self, api_key: str, base_url: Optional[str] = "https://translation-api.ghananlp.org"):
        self.api_key = api_key
        self.base_url = base_url
        self.translation_api = TranslationApi(api_key, base_url)
        self.asr_api = AsrApi(api_key, base_url)
        self.tts_api = TtsApi(api_key, base_url)

    def translate(self, text: str, language_pair: str = "en-tw") -> ResponseOrDict:
        """
        Translate text from one language to another.

        Args:
            text: The text to translate.
            language_pair: The language pair to translate the text to. Default is "en-tw".

        Returns:
            A Response object containing the translated text.
        """

        return self.translation_api.translate(text, language_pair)

    def asr(self, audio_file_path: str, language: str = "tw") -> ResponseOrDict:
        """
        Get the transcription of an audio file from a given language.

        Args:
            audio_file_path: The path to the audio file to transcribe.
            language: The language of the audio file. Default is "tw".

        Returns:
            A Response object containing the transcription of the audio file.
        """
        return self.asr_api.transcribe(audio_file_path, language)

    def tts(self, text: str, lang: str) -> ResponseOrDict:
        """
        Synthesize speech from text.

        Args:
            text: The text to synthesize.
            lang: The language of the text. Default is "tw".

        Returns:
            A Response object containing the synthesized speech.
        """
        return self.tts_api.synthesize(text, lang)
