
class TestTranslate:

    def test_translate_valid(self, khaya_interface):
        text = "Hello"
        translation_pair = "en-tw"

        result = khaya_interface.translate(text, translation_pair)

        assert result.status_code == 200
        assert result.text is not None
        assert "error" not in result.text.lower()

    def test_translate_error(self, khaya_interface):
        text = "Hello"
        wrong_translation_pair = "en-fw"

        result = khaya_interface.translate(text, wrong_translation_pair)

        assert "error" in result.text.lower()


class TestASR:

    def test_asr_valid(self, khaya_interface):
        audio_file_path = "tests/khaya/me_ho_ye.wav"

        result = khaya_interface.asr(audio_file_path, "tw")

        assert result.status_code == 200
        assert "error" not in result.text.lower()
        assert result.json() == "me ho yɛ"

    def test_asr_error(self, khaya_interface):
        audio_file_path = "tests/khaya/me_ho_ye.wav"
        wrong_lang = "fw"

        result = khaya_interface.asr(audio_file_path, wrong_lang)

        assert "error" in result['message'].lower()


class TestTTS:

    def test_tts_valid(self, khaya_interface):
        text = "Hello"
        lang = "tw"

        result = khaya_interface.tts(text, lang)

        assert result.status_code == 200
        assert isinstance(result.content, bytes)
        assert "error" not in result.text.lower()

    def test_tts_error(self, khaya_interface):
        text = "Hello"
        wrong_lang = "fw"

        result = khaya_interface.tts(text, wrong_lang)

        assert "error" in result.text.lower()
