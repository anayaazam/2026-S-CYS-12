# TTS Engine for SignBridge
import os
import tempfile
import logging
from typing import Tuple
from gtts import gTTS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TTSEngine")

# Initialize pygame mixer safely
pygame_available = False
try:
    import pygame
    pygame.mixer.init()
    pygame_available = True
except Exception as e:
    logger.warning("Failed to initialize pygame mixer (no audio device?): %s", str(e))

# Initialize pyttsx3 safely
pyttsx3_available = False
pyttsx3_engine = None
try:
    import pyttsx3
    pyttsx3_engine = pyttsx3.init()
    # Set speech rate and volume
    pyttsx3_engine.setProperty('rate', 150)
    pyttsx3_engine.setProperty('volume', 1.0)
    pyttsx3_available = True
except Exception as e:
    logger.warning("Failed to initialize pyttsx3 (offline TTS unavailable): %s", str(e))

class TTSEngine:
    """Manages text-to-speech synthesis in both English and Urdu with offline fallbacks."""

    def __init__(self) -> None:
        self.audio_enabled = pygame_available
        self.offline_enabled = pyttsx3_available
        self._temp_files = []

    def cleanup(self) -> None:
        """Cleans up any temporary MP3 files generated during the session."""
        if pygame_available:
            try:
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()
            except Exception:
                pass
                
        for path in self._temp_files:
            if os.path.exists(path):
                try:
                    os.remove(path)
                except Exception as e:
                    logger.debug("Failed to remove temp file %s: %s", path, str(e))
        self._temp_files.clear()

    def speak(self, text: str, lang: str = "en") -> Tuple[bool, str]:
        """Synthesizes and speaks the text.
        Returns (success, message_or_error).
        """
        if not text.strip():
            return False, "Empty text"

        # 1. Check if audio device is available
        if not self.audio_enabled and lang == "ur":
            return False, "Audio device not available for Urdu speech."

        # 2. Try online synthesis via gTTS
        if lang == "ur" or (lang == "en" and self.audio_enabled):
            try:
                tts = gTTS(text=text, lang=lang)
                # Use a temp file with delete=False so pygame can open it independently
                fd, temp_path = tempfile.mkstemp(suffix=".mp3")
                os.close(fd)
                self._temp_files.append(temp_path)
                
                tts.save(temp_path)
                
                if pygame_available:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load(temp_path)
                    pygame.mixer.music.play()
                    return True, "Online speech playing."
                else:
                    return False, "gTTS succeeded but audio mixer is not available."
            except Exception as e:
                logger.warning("gTTS speech failed: %s. Trying offline fallback if English.", str(e))
                # If Urdu, we cannot fall back to pyttsx3, so return failure
                if lang == "ur":
                    return False, f"Urdu speech requires internet. Connection failed: {str(e)}"

        # 3. Try offline synthesis via pyttsx3 (English only)
        if lang == "en":
            if self.offline_enabled and pyttsx3_engine:
                try:
                    pyttsx3_engine.say(text)
                    pyttsx3_engine.runAndWait()
                    return True, "Offline speech playing."
                except Exception as e:
                    return False, f"Offline TTS failed: {str(e)}"
            else:
                return False, "Offline TTS engine not initialized."

        return False, "Unable to play speech (unsupported combination of language and connection state)."
