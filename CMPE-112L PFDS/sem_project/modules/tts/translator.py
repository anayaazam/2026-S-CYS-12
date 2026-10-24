# Translator module for SignBridge English -> Urdu
import logging
from deep_translator import GoogleTranslator

class UrduTranslator:
    """Handles English to Urdu translation using deep_translator with graceful offline fallback."""
    
    def __init__(self) -> None:
        self.logger = logging.getLogger("UrduTranslator")
        # Cache for offline usage to translate common words without internet
        self._common_cache = {
            "hello": "ہیلو",
            "please": "براہ مہربانی",
            "thank you": "شکریہ",
            "yes": "جی ہاں",
            "no": "نہیں",
            "help": "مدد",
            "sorry": "معذرت",
            "a": "اے",
            "b": "بی",
            "c": "سی",
            "d": "ڈی",
            "e": "ای",
            "f": "ایف",
            "g": "جی",
            "h": "ایچ",
            "i": "آئی",
            "j": "جے",
            "k": "کے",
            "l": "ایل",
            "m": "ایم",
            "n": "این",
            "o": "او",
            "p": "پی",
            "q": "کیو",
            "r": "آر",
            "s": "ایس",
            "t": "ٹی",
            "u": "یو",
            "v": "وی",
            "w": "ڈبلیو",
            "x": "ایکس",
            "y": "وائی",
            "z": "زیڈ"
        }

    def translate(self, text: str) -> str:
        """Translates English text to Urdu. Falls back to a local dictionary or original text if offline."""
        if not text:
            return ""
            
        cleaned = text.strip().lower()
        
        # Check cache first (highly useful for common signs/alphabet offline)
        if cleaned in self._common_cache:
            return self._common_cache[cleaned]
            
        # Try online translation
        try:
            translator = GoogleTranslator(source='en', target='ur')
            translation = translator.translate(text)
            if translation:
                return translation
        except Exception as e:
            self.logger.warning("Online translation failed, using fallback. Error: %s", str(e))
            
        # Offline fallback: translate word-by-word if possible, or return original text
        words = text.split()
        translated_words = []
        for word in words:
            w_clean = word.strip(".,!?\"'").lower()
            translated_words.append(self._common_cache.get(w_clean, word))
            
        return " ".join(translated_words)
