# TTS Engine for SignBridge
import os
import tempfile
import logging
from typing import Tuple

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TTSEngine")


class TTSEngine:
    """Manages text-to-speech synthesis in English and Urdu with offline fallbacks.
    All heavy initialisation (pygame, pyttsx3) is deferred to first use.
    """

    def __init__(self) -> None:
        self._pygame_ready = False
        self._pyttsx3_engine = None
        self._temp_files = []
        self._init_audio()

    def _init_audio(self) -> None:
        """Initialise audio backends lazily and safely."""
        try:
            import pygame
            pygame.mixer.init()
            self._pygame_ready = True
        except Exception as e:
            logger.warning("pygame mixer unavailable: %s", e)

        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.setProperty("rate", 150)
            engine.setProperty("volume", 1.0)
            self._pyttsx3_engine = engine
        except Exception as e:
            logger.warning("pyttsx3 unavailable: %s", e)

    def speak(self, text: str, lang: str = "en") -> Tuple[bool, str]:
        """Synthesise and play speech. Returns (success, message)."""
        if not text.strip():
            return False, "Empty text"

        # --- Try gTTS (online, supports Urdu) ---
        try:
            from gtts import gTTS
            import pygame

            tts = gTTS(text=text, lang=lang)
            fd, tmp = tempfile.mkstemp(suffix=".mp3")
            os.close(fd)
            self._temp_files.append(tmp)
            tts.save(tmp)

            if self._pygame_ready:
                pygame.mixer.music.stop()
                pygame.mixer.music.load(tmp)
                pygame.mixer.music.play()
                return True, "Online speech playing."
            else:
                return False, "gTTS saved but no audio mixer available."
        except Exception as e:
            logger.warning("gTTS failed: %s", e)
            if lang == "ur":
                return False, f"Urdu TTS requires internet. Error: {e}"

        # --- Fallback: pyttsx3 offline (English only) ---
        if lang == "en" and self._pyttsx3_engine:
            try:
                self._pyttsx3_engine.say(text)
                self._pyttsx3_engine.runAndWait()
                return True, "Offline speech playing."
            except Exception as e:
                return False, f"Offline TTS failed: {e}"

        return False, "No TTS backend available."

    def cleanup(self) -> None:
        """Stop playback and delete temp files."""
        if self._pygame_ready:
            try:
                import pygame
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()
            except Exception:
                pass
        for path in self._temp_files:
            try:
                if os.path.exists(path):
                    os.remove(path)
            except Exception:
                pass
        self._temp_files.clear()
