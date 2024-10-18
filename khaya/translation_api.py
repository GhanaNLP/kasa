from requests.models import Response

from khaya.base_api import BaseApi


class TranslationApi(BaseApi):
    def translate(self, text: str, language_pair: str = "en-tw") -> Response:
        """
        Translate text from one language to another using the GhanaNLP translation API.

        Args:
            text (str): The text to translate.
            language_pair (str): The language pair to translate the text to

        Returns:
            dict: The translated text.
        """
        url = f"{self.base_url}/v1/translate"
        payload = {"in": text, "lang": language_pair}
        response = self._make_request("POST", url, json=payload)
        return response
