# Speak (ASL-to-Speech) Screen for SignBridge
import os
import cv2
import threading
from typing import Optional

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QTextEdit, QButtonGroup, QSizePolicy, QScrollArea
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap, QImage

from modules.recognizer.letter_buffer import LetterBuffer
from modules.tts.translator import UrduTranslator
from modules.tts.tts_engine import TTSEngine
from modules.gamification.badge_engine import increment_urdu_tts_counter


DARK_BG = "#0d0d1a"
CARD_BG = "#1a1a2e"
ACCENT = "#00d4aa"
RED_ACCENT = "#e94560"
BLUE_ACCENT = "#0f3460"
TEXT_MAIN = "#e0e0e0"
TEXT_DIM = "#a0a0b0"
GREEN_ACCENT = "#008f7a"


class SpeakScreen(QWidget):
    """Integrates real-time ASL spelling, temporal buffering, translation,
    and Urdu/English TTS into a unified speech builder interface.
    """
    _urdu_signal = pyqtSignal(str)

    def __init__(self, controller) -> None:
        super().__init__()
        self.controller = controller
        self.db = controller.db_manager
        self.detector = controller.asl_detector

        self.letter_buffer = LetterBuffer(window_size=15, stability_threshold=10)
        self.translator = UrduTranslator()
        self.tts_engine = TTSEngine()

        self.cap: Optional[cv2.VideoCapture] = None
        self.is_running = False

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._update_frame)

        self._urdu_signal.connect(self._on_urdu_ready)

        self.setStyleSheet(f"background-color: {DARK_BG};")
        self._setup_ui()

    def _setup_ui(self) -> None:
        main = QHBoxLayout(self)
        main.setContentsMargins(20, 20, 20, 20)
        main.setSpacing(20)

        # Camera panel
        self.cam_container = QFrame()
        self.cam_container.setStyleSheet(
            f"QFrame {{ background-color: {CARD_BG}; border-radius: 10px; }}"
        )
        cam_v = QVBoxLayout(self.cam_container)
        cam_v.setAlignment(Qt.AlignCenter)

        self.feed_label = QLabel("Camera Offline\nClick 'Start Camera' to spell words.")
        self.feed_label.setAlignment(Qt.AlignCenter)
        self.feed_label.setFont(QFont("Helvetica", 14))
        self.feed_label.setStyleSheet(f"color: {TEXT_DIM}; background: transparent;")
        self.feed_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        cam_v.addWidget(self.feed_label)
        main.addWidget(self.cam_container, 3)

        # Right panel
        right_panel = QFrame()
        right_panel.setStyleSheet(
            f"QFrame {{ background-color: {CARD_BG}; border-radius: 10px; }}"
        )
        right_v = QVBoxLayout(right_panel)
        right_v.setContentsMargins(15, 15, 15, 15)
        right_v.setSpacing(10)

        # Sentence Builder
        sb_hdr = QLabel("SENTENCE BUILDER")
        sb_hdr.setFont(QFont("Helvetica", 10, QFont.Bold))
        sb_hdr.setStyleSheet(f"color: {ACCENT}; background: transparent;")
        right_v.addWidget(sb_hdr)

        self.text_box = QTextEdit()
        self.text_box.setFixedHeight(80)
        self.text_box.setFont(QFont("Helvetica", 16))
        self.text_box.setStyleSheet(
            f"QTextEdit {{ background-color: {DARK_BG}; color: {TEXT_MAIN}; "
            f"border: 1px solid {BLUE_ACCENT}; border-radius: 6px; padding: 4px; }}"
        )
        self.text_box.textChanged.connect(self._on_text_changed)
        right_v.addWidget(self.text_box)

        # Buffer controls
        btn_row = QHBoxLayout()
        btn_row.setSpacing(6)

        for text, slot in [("Space", self._add_space), ("Backspace", self._backspace), ("Clear", self._clear_buffer)]:
            b = QPushButton(text)
            b.setFixedHeight(28)
            b.setCursor(Qt.PointingHandCursor)
            if text == "Clear":
                style = (
                    f"QPushButton {{ background-color: {RED_ACCENT}; color: white; "
                    f"border: none; border-radius: 4px; font-size: 12px; }}"
                    f"QPushButton:hover {{ background-color: {BLUE_ACCENT}; }}"
                )
            else:
                style = (
                    f"QPushButton {{ background-color: {BLUE_ACCENT}; color: white; "
                    f"border: none; border-radius: 4px; font-size: 12px; }}"
                    f"QPushButton:hover {{ background-color: {RED_ACCENT}; }}"
                )
            b.setStyleSheet(style)
            b.clicked.connect(slot)
            btn_row.addWidget(b)

        right_v.addLayout(btn_row)

        # Urdu translation
        trans_hdr = QLabel("URDU TRANSLATION")
        trans_hdr.setFont(QFont("Helvetica", 10, QFont.Bold))
        trans_hdr.setStyleSheet(f"color: {RED_ACCENT}; background: transparent;")
        right_v.addWidget(trans_hdr)

        urdu_frame = QFrame()
        urdu_frame.setStyleSheet(
            f"QFrame {{ background-color: {DARK_BG}; border-radius: 8px; }}"
        )
        urdu_v = QVBoxLayout(urdu_frame)
        urdu_v.setContentsMargins(10, 8, 10, 8)

        self.urdu_label = QLabel("یہاں ترجمہ ظاہر ہوگا")
        self.urdu_label.setFont(QFont("Noto Nastaliq Urdu", 16))
        self.urdu_label.setAlignment(Qt.AlignRight)
        self.urdu_label.setWordWrap(True)
        self.urdu_label.setStyleSheet(f"color: {TEXT_MAIN}; background: transparent;")
        urdu_v.addWidget(self.urdu_label)

        right_v.addWidget(urdu_frame)

        # Language toggle (two buttons acting like segmented)
        lang_row = QHBoxLayout()
        lang_row.setSpacing(0)

        self.lang_en_btn = QPushButton("English")
        self.lang_en_btn.setCheckable(True)
        self.lang_en_btn.setChecked(True)
        self.lang_en_btn.setFixedHeight(34)
        self.lang_en_btn.setCursor(Qt.PointingHandCursor)

        self.lang_ur_btn = QPushButton("Urdu")
        self.lang_ur_btn.setCheckable(True)
        self.lang_ur_btn.setChecked(False)
        self.lang_ur_btn.setFixedHeight(34)
        self.lang_ur_btn.setCursor(Qt.PointingHandCursor)

        self._lang_group = QButtonGroup(self)
        self._lang_group.setExclusive(True)
        self._lang_group.addButton(self.lang_en_btn)
        self._lang_group.addButton(self.lang_ur_btn)
        self._lang_group.buttonClicked.connect(self._update_lang_styles)

        for btn in [self.lang_en_btn, self.lang_ur_btn]:
            lang_row.addWidget(btn)
        self._update_lang_styles()

        right_v.addLayout(lang_row)

        self.speak_btn = QPushButton("Speak Sentence")
        self.speak_btn.setFixedHeight(40)
        self.speak_btn.setFont(QFont("Helvetica", 13, QFont.Bold))
        self.speak_btn.setCursor(Qt.PointingHandCursor)
        self.speak_btn.setStyleSheet(
            f"QPushButton {{ background-color: {GREEN_ACCENT}; color: white; "
            f"border: none; border-radius: 6px; }}"
            f"QPushButton:hover {{ background-color: {BLUE_ACCENT}; }}"
        )
        self.speak_btn.clicked.connect(self._trigger_speak)
        right_v.addWidget(self.speak_btn)

        self.start_btn = QPushButton("Start Camera")
        self.start_btn.setFixedHeight(36)
        self.start_btn.setCursor(Qt.PointingHandCursor)
        self.start_btn.setStyleSheet(
            f"QPushButton {{ background-color: {BLUE_ACCENT}; color: white; "
            f"border: none; border-radius: 6px; }}"
            f"QPushButton:hover {{ background-color: {RED_ACCENT}; }}"
        )
        self.start_btn.clicked.connect(self._toggle_camera)
        right_v.addWidget(self.start_btn)

        right_v.addStretch(1)
        main.addWidget(right_panel, 2)

    def _update_lang_styles(self, btn=None) -> None:
        active = f"QPushButton {{ background-color: {BLUE_ACCENT}; color: white; border: none; border-radius: 4px; }}"
        inactive = f"QPushButton {{ background-color: #0d0d1a; color: {TEXT_DIM}; border: none; border-radius: 4px; }}"
        self.lang_en_btn.setStyleSheet(active if self.lang_en_btn.isChecked() else inactive)
        self.lang_ur_btn.setStyleSheet(active if self.lang_ur_btn.isChecked() else inactive)

    def on_enter(self) -> None:
        self._clear_buffer()
        self._start_camera()

    def on_leave(self) -> None:
        self._stop_camera()
        self.tts_engine.cleanup()

    def _toggle_camera(self) -> None:
        if self.is_running:
            self._stop_camera()
        else:
            self._start_camera()

    def _start_camera(self) -> None:
        if self.is_running:
            return
        cam_idx = int(self.controller.settings.get("camera_index", 0))
        self.cap = cv2.VideoCapture(cam_idx)
        if not self.cap.isOpened():
            self.feed_label.setText("Webcam not found.\nPlease connect a camera.")
            self.cap = None
            return
        self.is_running = True
        self.start_btn.setText("Stop Camera")
        self.start_btn.setStyleSheet(
            f"QPushButton {{ background-color: {RED_ACCENT}; color: white; "
            f"border: none; border-radius: 6px; }}"
            f"QPushButton:hover {{ background-color: {BLUE_ACCENT}; }}"
        )
        self._timer.start(15)

    def _stop_camera(self) -> None:
        self._timer.stop()
        self.is_running = False
        if self.cap:
            self.cap.release()
            self.cap = None
        self.start_btn.setText("Start Camera")
        self.start_btn.setStyleSheet(
            f"QPushButton {{ background-color: {BLUE_ACCENT}; color: white; "
            f"border: none; border-radius: 6px; }}"
            f"QPushButton:hover {{ background-color: {RED_ACCENT}; }}"
        )
        self.feed_label.setText("Camera Offline\nClick 'Start Camera' to spell words.")

    def _update_frame(self) -> None:
        if not self.is_running or not self.cap:
            return

        ret, frame = self.cap.read()
        if not ret:
            self._stop_camera()
            return

        frame = cv2.flip(frame, 1)
        annotated, pred_label, confidence = self.detector.process_frame(frame)

        if pred_label and confidence >= 0.80:
            stable, is_new = self.letter_buffer.add_prediction(pred_label)
            if is_new and stable:
                self._sync_textbox()

        rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        ratio = min(600 / w, 400 / h)
        new_w, new_h = int(w * ratio), int(h * ratio)
        rgb = cv2.resize(rgb, (new_w, new_h))
        qimg = QImage(rgb.data, new_w, new_h, new_w * 3, QImage.Format_RGB888)
        self.feed_label.setPixmap(QPixmap.fromImage(qimg))

    def _sync_textbox(self) -> None:
        text = self.letter_buffer.get_sentence()
        self.text_box.blockSignals(True)
        self.text_box.setPlainText(text)
        self.text_box.blockSignals(False)
        self._translate_async(text)

    def _on_text_changed(self) -> None:
        text = self.text_box.toPlainText().strip()
        self._translate_async(text)

    def _translate_async(self, text: str) -> None:
        if not text.strip():
            self.urdu_label.setText("")
            return

        def run():
            translation = self.translator.translate(text)
            self._urdu_signal.emit(translation)

        threading.Thread(target=run, daemon=True).start()

    def _on_urdu_ready(self, text: str) -> None:
        self.urdu_label.setText(text)

    def _add_space(self) -> None:
        self.letter_buffer.add_space()
        self._sync_textbox()

    def _backspace(self) -> None:
        self.letter_buffer.backspace()
        self._sync_textbox()

    def _clear_buffer(self) -> None:
        self.letter_buffer.clear()
        self._sync_textbox()

    def _trigger_speak(self) -> None:
        text = self.text_box.toPlainText().strip()
        if not text:
            return

        user_id = self.controller.current_user_id

        if self.lang_ur_btn.isChecked():
            urdu_text = self.translator.translate(text)
            success, msg = self.tts_engine.speak(urdu_text, lang="ur")
            if success:
                increment_urdu_tts_counter(self.db, user_id)
        else:
            success, msg = self.tts_engine.speak(text, lang="en")

        if not success:
            self.controller.show_toast(f"TTS Error: {msg}")
