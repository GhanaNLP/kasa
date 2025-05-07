from functools import wraps
from kasa.exceptions import AuthenticationError


def check_authentication(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self.http_client.config.api_key:
            raise AuthenticationError("API key is required", 401)
        return func(self, *args, **kwargs)

    return wrapper
