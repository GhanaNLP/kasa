import requests
import json

class GhanaNLP:
    def __init__(self, api_key):
        self.base_url = "https://translation-api.ghananlp.org"  
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            'Cache-Control': 'no-cache',
            "Ocp-Apim-Subscription-Key":self.api_key
        }

    # Translation
    def translate(self, text, language_pair="en-tw"):
        """Translate text from one language to another using the GhanaNLP translation API."""

        url = f"{self.base_url}/v1/translate"
        payload = {
            "in": text,
            "lang": language_pair
        }

        return self._post_request(url, payload)
    
    # STT - Speech to Text
    def stt(self, audio_file_path, language="tw"):
        """Convert speech to text from audio binary data in an African language using the GhanaNLP STT API."""

        url = f"{self.base_url}/asr/v1/transcribe?language={language}"
        with open(audio_file_path, 'rb') as db:
            data = db.read()

        headers = {
            'Content-Type': 'audio/mpeg',
            'Cache-Control': 'no-cache',
            "Ocp-Apim-Subscription-Key": self.api_key,
        }

        try:
            response = requests.post(url, headers=headers, data=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_e:
            return {
                "type":"HTTP, request reached the API",
                "message": f"{http_e}"}
        except Exception as e:
            return {
                "type":"Failed to process, possibly internet connectivity",
                "message": f"{e}"}
        
    # TTS - Text to Speech
    def tts(self, text, lang):
        """Convert text to speech in a specified African language using the GhanaNLP TTS API."""
        url = f"{self.base_url}/tts/v1/tts"

        payload = json.dumps({"text": text, "language": lang})   

        try:
            req = requests.post(url, headers=self.headers, data=bytes(payload.encode("utf-8")))

            req.get_method = lambda: 'POST'
            response = req

            if response.status_code == 200:        
                audio_data = response.content
                return audio_data            
            else:
                return{
                    "type":"System",
                "message": "Failed to process"}
              
        except Exception as e:
            return {
                "type":"Request couldn't reach the API.",
                "message": e}


    def _post_request(self, url, payload):
        """A method for POST requests."""
        try:
            response = requests.post(url, json=payload, headers=self.headers)
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.HTTPError as http_e:
            return {
                "type":"HTTP, request reached the API",
                "message": f"{http_e}"}
        except Exception as e:
            return {
                "type":"Failed to process, possibly internet connectivity",
                "message": f"{e}"}
