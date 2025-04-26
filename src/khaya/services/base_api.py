from abc import ABC

import httpx
import requests

from src.khaya.config import Settings
from src.khaya.logger import logger


class BaseApi(ABC):
    def __init__(self, config: Settings):
        self.config = config
        self.sync_client = httpx.Client(timeout=self.config.timeout)
        self.async_client = httpx.AsyncClient(timeout=self.config.timeout)

    def _prepare_headers(self):
        return {
            "Ocp-Apim-Subscription-Key": self.config.api_key,
            "Content-Type": "application/json",
            "Cache-Control": "no-cache",
        }

    def request(
        self, method: str, url: str, **kwargs
    ) -> requests.Response | dict[str, str]:
        """
        Make an HTTP request.

        Args:
            method (str): HTTP method ('GET', 'POST', etc.).
            url (str): The URL to make the request to.
            **kwargs: Additional arguments to pass to the request.

        Returns:
            requests.Response: The HTTP response.
        """
        headers = self._prepare_headers()
        kwargs.setdefault("headers", headers)
        try:
            logger.debug(f"Sync request to {method} {url} with {kwargs}")
            response = self.sync_client.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except httpx.HTTPError as http_e:
            logger.error(f"HTTP error occurred: {http_e}")
            return {"type": "HTTP, request reached the API", "message": f"{http_e}"}
        except Exception as e:
            return {
                "type": "Failed to process, an error occurred",
                "message": f"{e}",
            }
