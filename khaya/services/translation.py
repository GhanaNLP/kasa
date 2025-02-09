from requests.models import Response

from khaya.services.base_api import BaseApi
from khaya.config import Settings
from khaya.exceptions import TranslationError


class TranslationService:

    def __init__(self, http_client: BaseApi, config: Settings):
        self.http_client = http_client
        self.endpoint = config.endpoints["translation"]

    def translate(
        self, text: str, language_pair: str = "en-tw"
    ) -> Response | dict[str, str]:
        """
        Translate text from one language to another using the GhanaNLP translation API.

        Args:
            text (str): The text to translate.
            language_pair (str): The language pair to translate the text to

        Returns:
            dict: The translated text.
        """
        if not text or not language_pair:
            raise TranslationError("Text and language pair are required", 400)

        try:
            payload = {"in": text, "lang": language_pair}
            response = self.http_client.request("POST", self.endpoint, json=payload)
            return response
        except Exception as e:
            raise TranslationError(str(e), 500)
