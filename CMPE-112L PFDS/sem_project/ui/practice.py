# Practice Screen for SignBridge
import os
import cv2
from PIL import Image
from typing import Optional, Dict, Any

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QProgressBar, QSizePolicy
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QPixmap, QImage

from database.db_manager import DatabaseManager
from modules.recognizer.asl_detector import ASLDetector
from modules.learning.lesson_manager import LessonManager


DARK_BG = "#0d0d1a"
CARD_BG = "#1a1a2e"
ACCENT = "#00d4aa"
RED_ACCENT = "#e94560"
BLUE_ACCENT = "#0f3460"
ORANGE = "#ffaa00"
TEXT_MAIN = "#e0e0e0"
TEXT_DIM = "#a0a0b0"


def _progress_bar(color: str = ACCENT) -> QProgressBar:
    pb = QProgressBar()
    pb.setRange(0, 100)
    pb.setValue(0)
    pb.setFixedHeight(12)
    pb.setTextVisible(False)
    pb.setStyleSheet(
        f"QProgressBar {{ background-color: {DARK_BG}; border-radius: 6px; border: none; }}"
        f"QProgressBar::chunk {{ background-color: {color}; border-radius: 6px; }}"
    )
    return pb


class PracticeScreen(QWidget):
    """Enables real-time sign language practice using the webcam and the ASLDetector."""

    def __init__(self, controller) -> None:
        super().__init__()
        self.controller = controller
        self.db = controller.db_manager
        self.detector = controller.asl_detector
        self.lesson_manager = LessonManager(self.db)

        self.cap: Optional[cv2.VideoCapture] = None
        self.is_running = False
        self.lesson: Optional[Dict[str, Any]] = None

        self.matching_frames = 0
        self.required_frames = 15
        self.best_confidence = 0.0
        self.practice_finished = False

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._update_frame)

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

        self.feed_label = QLabel("Camera Offline\nClick 'Start Camera' to begin.")
        self.feed_label.setAlignment(Qt.AlignCenter)
        self.feed_label.setFont(QFont("Helvetica", 14))
        self.feed_label.setStyleSheet(f"color: {TEXT_DIM}; background: transparent;")
        self.feed_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        cam_v.addWidget(self.feed_label)
        main.addWidget(self.cam_container, 3)

        # Progress panel
        self.progress_panel = QFrame()
        self.progress_panel.setStyleSheet(
            f"QFrame {{ background-color: {CARD_BG}; border-radius: 10px; }}"
        )
        self._pp_layout = QVBoxLayout(self.progress_panel)
        self._pp_layout.setContentsMargins(20, 20, 20, 20)
        self._pp_layout.setSpacing(10)
        self._build_default_instructions()
        main.addWidget(self.progress_panel, 2)

    def _build_default_instructions(self) -> None:
        while self._pp_layout.count():
            item = self._pp_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self._pp_layout.addStretch(1)
        lbl = QLabel("No sign selected.\nPlease select a lesson to practice from the Course Curriculum.")
        lbl.setAlignment(Qt.AlignCenter)
        lbl.setWordWrap(True)
        lbl.setStyleSheet(f"color: {TEXT_DIM}; background: transparent;")
        self._pp_layout.addWidget(lbl)
        self._pp_layout.addStretch(1)

    def on_enter(self, lesson_id: Optional[int] = None) -> None:
        if not lesson_id:
            self._build_default_instructions()
            return

        self.lesson = self.db.get_lesson_by_id(lesson_id)
        if not self.lesson:
            return

        self.matching_frames = 0
        self.best_confidence = 0.0
        self.practice_finished = False

        while self._pp_layout.count():
            item = self._pp_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        title = QLabel(f"Practice: {self.lesson['sign_name']}")
        title.setFont(QFont("Helvetica", 18, QFont.Bold))
        title.setStyleSheet(f"color: {TEXT_MAIN}; background: transparent;")
        self._pp_layout.addWidget(title)

        prompt = QLabel(f"Hold the sign for letter '{self.lesson['letter']}' in front of the camera.")
        prompt.setFont(QFont("Helvetica", 12))
        prompt.setStyleSheet(f"color: {ACCENT}; font-style: italic; background: transparent;")
        prompt.setWordWrap(True)
        self._pp_layout.addWidget(prompt)

        self.match_progress = _progress_bar()
        self._pp_layout.addWidget(self.match_progress)

        self.status_lbl = QLabel("Analyzing camera feed...")
        self.status_lbl.setFont(QFont("Helvetica", 13))
        self.status_lbl.setStyleSheet(f"color: {TEXT_DIM}; background: transparent;")
        self._pp_layout.addWidget(self.status_lbl)

        self.start_btn = QPushButton("Start Camera")
        self.start_btn.setFixedHeight(36)
        self.start_btn.setCursor(Qt.PointingHandCursor)
        self.start_btn.setStyleSheet(
            f"QPushButton {{ background-color: {BLUE_ACCENT}; color: {TEXT_MAIN}; "
            f"border: none; border-radius: 6px; }}"
            f"QPushButton:hover {{ background-color: {RED_ACCENT}; }}"
        )
        self.start_btn.clicked.connect(self._toggle_camera)
        self._pp_layout.addWidget(self.start_btn)

        if self.controller.settings.get("dev_mode", "Disabled") == "Enabled":
            sim_btn = QPushButton("Simulate Success (Dev)")
            sim_btn.setFixedHeight(36)
            sim_btn.setCursor(Qt.PointingHandCursor)
            sim_btn.setStyleSheet(
                f"QPushButton {{ background: transparent; color: {RED_ACCENT}; "
                f"border: 1px solid {RED_ACCENT}; border-radius: 6px; }}"
                f"QPushButton:hover {{ background-color: {RED_ACCENT}; color: white; }}"
            )
            sim_btn.clicked.connect(self._simulate_success)
            self._pp_layout.addWidget(sim_btn)

        self._pp_layout.addStretch(1)
        self._start_camera()

    def on_leave(self) -> None:
        self._stop_camera()

    def _toggle_camera(self) -> None:
        if self.is_running:
            self._stop_camera()
        else:
            self._start_camera()

    def _start_camera(self) -> None:
        if self.is_running or not self.lesson:
            return
        cam_idx = int(self.controller.settings.get("camera_index", 0))
        self.cap = cv2.VideoCapture(cam_idx)
        if not self.cap.isOpened():
            self.feed_label.setText("Webcam not found.\nPlease ensure your camera is connected.")
            self.cap = None
            return
        self.is_running = True
        if hasattr(self, 'start_btn'):
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
        if hasattr(self, 'start_btn'):
            self.start_btn.setText("Start Camera")
            self.start_btn.setStyleSheet(
                f"QPushButton {{ background-color: {BLUE_ACCENT}; color: {TEXT_MAIN}; "
                f"border: none; border-radius: 6px; }}"
                f"QPushButton:hover {{ background-color: {RED_ACCENT}; }}"
            )
        self.feed_label.setText("Camera Offline\nClick 'Start Camera' to begin.")

    def _update_frame(self) -> None:
        if not self.is_running or not self.cap or self.practice_finished:
            return

        ret, frame = self.cap.read()
        if not ret:
            self._stop_camera()
            return

        frame = cv2.flip(frame, 1)
        annotated, pred_label, confidence = self.detector.process_frame(frame)

        if pred_label and self.lesson:
            target = self.lesson["letter"].upper()
            if pred_label == target and confidence >= 0.80:
                self.matching_frames += 1
                self.best_confidence = max(self.best_confidence, confidence)
                progress = min(100, int(self.matching_frames / self.required_frames * 100))
                self.match_progress.setValue(progress)
                self.status_lbl.setText(f"Holding sign... ({self.matching_frames}/{self.required_frames})")
                self.status_lbl.setStyleSheet(f"color: {ACCENT}; background: transparent;")
                if self.matching_frames >= self.required_frames:
                    self._finish_practice()
                    return
            else:
                if self.matching_frames > 0:
                    self.matching_frames -= 1
                    self.match_progress.setValue(int(self.matching_frames / self.required_frames * 100))

        rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        ratio = min(600 / w, 400 / h)
        new_w, new_h = int(w * ratio), int(h * ratio)
        rgb = cv2.resize(rgb, (new_w, new_h))
        qimg = QImage(rgb.data, new_w, new_h, new_w * 3, QImage.Format_RGB888)
        self.feed_label.setPixmap(QPixmap.fromImage(qimg))

    def _simulate_success(self) -> None:
        self.best_confidence = 0.95
        self._finish_practice()

    def _finish_practice(self) -> None:
        self.practice_finished = True
        self._stop_camera()

        user_id = self.controller.current_user_id
        lesson_id = self.lesson["id"]
        accuracy = self.best_confidence * 100 if self.best_confidence > 0 else 85.0

        completed, xp_earned, badges = self.lesson_manager.complete_lesson_attempt(
            user_id, lesson_id, accuracy
        )

        self.match_progress.setValue(100)
        self.status_lbl.setText(f"Success! Accuracy: {accuracy:.1f}%")
        self.status_lbl.setStyleSheet(f"color: {ACCENT}; background: transparent;")

        feedback = QLabel(f"🎉 Sign Matched!\n+{xp_earned} XP earned!")
        feedback.setFont(QFont("Helvetica", 14, QFont.Bold))
        feedback.setAlignment(Qt.AlignCenter)
        feedback.setStyleSheet(f"color: {ACCENT}; background: transparent;")
        self._pp_layout.insertWidget(self._pp_layout.count() - 1, feedback)

        if badges:
            badge_lbl = QLabel(f"Unlocked Badges: {', '.join(badges)}")
            badge_lbl.setFont(QFont("Helvetica", 11, QFont.Bold))
            badge_lbl.setAlignment(Qt.AlignCenter)
            badge_lbl.setStyleSheet(f"color: {ORANGE}; background: transparent;")
            self._pp_layout.insertWidget(self._pp_layout.count() - 1, badge_lbl)

        next_btn = QPushButton("Continue to Curriculum")
        next_btn.setFixedHeight(36)
        next_btn.setCursor(Qt.PointingHandCursor)
        next_btn.setStyleSheet(
            f"QPushButton {{ background-color: {ACCENT}; color: {DARK_BG}; "
            f"border: none; border-radius: 6px; font-weight: bold; }}"
            f"QPushButton:hover {{ background-color: {BLUE_ACCENT}; color: white; }}"
        )
        next_btn.clicked.connect(lambda: self.controller.show_screen("learn"))
        self._pp_layout.insertWidget(self._pp_layout.count() - 1, next_btn)
