from requests.models import Response

from kasa.services.base_api import BaseApi
from kasa.exceptions import TranslationError
from kasa.utils import check_authentication


class TranslationService:

    def __init__(self, http_client: BaseApi):
        self.http_client = http_client
        self.endpoint = http_client.config.endpoints["translation"]

    @check_authentication
    def translate(
        self, text: str, language_pair: str = "en-tw"
    ) -> Response | dict[str, str]:
        """
        Translate text from one language to another using the GhanaNLP translation API.

        Args:
            text (str): The text to translate.
            language_pair (str): The language pair to translate the text from and to.

        Returns:
            Response: The response from the translation API.
        """
        if not text or not language_pair:
            raise TranslationError("Text and language pair are required", 400)
        try:
            payload = {"in": text, "lang": language_pair}
            response = self.http_client.request("POST", self.endpoint, json=payload)
            return response
        except Exception as e:
            raise TranslationError(str(e), 500)
