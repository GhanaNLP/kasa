from abc import ABC, abstractmethod
from typing import Optional
import requests


class BASE_API(ABC):
    def __init__(self, api_key: str, base_url: Optional[str] = None):
        self.api_key = api_key
        self.base_url = base_url or "https://translation-api.ghananlp.org"
        self.headers = {
            "Ocp-Apim-Subscription-Key": self.api_key,
            "Content-Type": "application/json",
            "Cache-Control": "no-cache",
        }

    def _make_request(self, method: str, url: str, **kwargs) -> requests.Response:
        """
        Make an HTTP request.

        Args:
            method (str): HTTP method ('GET', 'POST', etc.).
            url (str): The URL to make the request to.
            **kwargs: Additional arguments to pass to the request.

        Returns:
            requests.Response: The HTTP response.
        """
        try:
            response = requests.request(method, url, headers=self.headers, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as http_e:
            return {"type": "HTTP, request reached the API", "message": f"{http_e}"}
        except Exception as e:
            return {
                "type": "Failed to process, an error occurred",
                "message": f"{e}",
            }
