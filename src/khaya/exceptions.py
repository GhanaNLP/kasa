class APIError(Exception):
    """Base class for API errors."""

    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class AuthenticationError(APIError):
    """Error during authentication."""

    def __init__(self, message: str, status_code: int):
        super().__init__(message, status_code)


class RateLimitError(APIError):
    """Error during rate limiting."""

    def __init__(self, message: str, status_code: int):
        super().__init__(message, status_code)


class TranslationError(APIError):
    """Error during translation."""

    def __init__(self, message: str, status_code: int):
        super().__init__(message, status_code)


class TTSGenerationError(APIError):
    """Error during TTS generation."""

    def __init__(self, message: str, status_code: int):
        super().__init__(message, status_code)


class ASRTranscriptionError(APIError):
    """Error during ASR transcription."""

    def __init__(self, message: str, status_code: int):
        super().__init__(message, status_code)
