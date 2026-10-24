# Quiz Screen for SignBridge
import os
import cv2
from PIL import Image
from typing import List, Dict, Any, Optional

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QProgressBar, QSizePolicy, QGridLayout
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QPixmap, QImage

from modules.quiz.quiz_engine import QuizEngine
from modules.recognizer.asl_detector import ASLDetector


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
    pb.setFixedHeight(10)
    pb.setTextVisible(False)
    pb.setStyleSheet(
        f"QProgressBar {{ background-color: {DARK_BG}; border-radius: 5px; border: none; }}"
        f"QProgressBar::chunk {{ background-color: {color}; border-radius: 5px; }}"
    )
    return pb


class QuizScreen(QWidget):
    """Interactive quiz session interface supporting FLASHCARD and SIGN_IT questions."""

    def __init__(self, controller) -> None:
        super().__init__()
        self.controller = controller
        self.db = controller.db_manager
        self.detector = controller.asl_detector
        self.quiz_engine = QuizEngine(self.db)

        self.questions: List[Dict[str, Any]] = []
        self.current_idx = 0
        self.score = 0

        self.cap: Optional[cv2.VideoCapture] = None
        self.is_running = False
        self.matching_frames = 0
        self.required_frames = 15
        self.best_confidence = 0.0
        self.question_answered = False
        # Prevents camera loop from touching deleted widgets during transitions
        self._locked = False

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._update_camera_loop)

        self.setStyleSheet(f"background-color: {DARK_BG};")
        self._main_layout = QVBoxLayout(self)
        self._main_layout.setContentsMargins(20, 20, 20, 20)
        self._main_layout.setSpacing(10)

    def refresh(self) -> None:
        self._start_new_quiz()

    def _start_new_quiz(self, mode: str = "MIXED") -> None:
        user_id = self.controller.current_user_id
        progress = self.db.get_user_progress(user_id)
        completed_ids = [lid for lid, p in progress.items() if p.get("completed")]

        if not completed_ids:
            self._show_no_lessons_screen()
            return

        self.questions = self.quiz_engine.generate_quiz_from_completed(user_id, completed_ids, mode)
        self.current_idx = 0
        self.score = 0
        self.question_answered = False
        self._locked = False

        if not self.questions:
            self._show_no_lessons_screen()
            return

        self._show_current_question()

    def _clear_layout(self) -> None:
        while self._main_layout.count():
            item = self._main_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self._clear_sublayout(item.layout())

    def _clear_sublayout(self, layout) -> None:
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def _show_no_lessons_screen(self) -> None:
        self._stop_camera()
        self._clear_layout()
        self._main_layout.addStretch(1)

        msg = QLabel("Complete some lessons first before taking a quiz! 🎓")
        msg.setFont(QFont("Helvetica", 16, QFont.Bold))
        msg.setAlignment(Qt.AlignCenter)
        msg.setWordWrap(True)
        msg.setStyleSheet(f"color: {TEXT_DIM};")
        self._main_layout.addWidget(msg)

        go_btn = QPushButton("Go to Learn")
        go_btn.setFixedHeight(40)
        go_btn.setMaximumWidth(200)
        go_btn.setCursor(Qt.PointingHandCursor)
        go_btn.setStyleSheet(
            f"QPushButton {{ background-color: {BLUE_ACCENT}; color: white; "
            f"border: none; border-radius: 6px; }}"
            f"QPushButton:hover {{ background-color: {ACCENT}; color: {DARK_BG}; }}"
        )
        go_btn.clicked.connect(lambda: self.controller.show_screen("learn"))
        go_btn_wrap = QHBoxLayout()
        go_btn_wrap.addStretch(1)
        go_btn_wrap.addWidget(go_btn)
        go_btn_wrap.addStretch(1)
        self._main_layout.addLayout(go_btn_wrap)
        self._main_layout.addStretch(1)

    def _show_current_question(self) -> None:
        self._stop_camera()
        self._locked = False
        self.question_answered = False
        self._clear_layout()

        if self.current_idx >= len(self.questions):
            self._show_score_screen()
            return

        q = self.questions[self.current_idx]

        hdr = QLabel(f"Question {self.current_idx + 1} of {len(self.questions)}  ·  Score: {self.score}")
        hdr.setFont(QFont("Helvetica", 13, QFont.Bold))
        hdr.setAlignment(Qt.AlignCenter)
        hdr.setStyleSheet(f"color: {ACCENT};")
        self._main_layout.addWidget(hdr)

        q_frame = QFrame()
        q_frame.setStyleSheet(
            f"QFrame {{ background-color: {CARD_BG}; border-radius: 12px; }}"
        )
        q_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._main_layout.addWidget(q_frame, 1)

        if q["type"] == "FLASHCARD":
            self._build_flashcard_ui(q_frame, q)
        else:
            self._build_sign_it_ui(q_frame, q)

    def _build_flashcard_ui(self, parent: QFrame, q: Dict[str, Any]) -> None:
        v = QVBoxLayout(parent)
        v.setContentsMargins(30, 20, 30, 20)
        v.setSpacing(12)
        v.setAlignment(Qt.AlignCenter)

        lbl = QLabel("Which sign is shown in the image?")
        lbl.setFont(QFont("Helvetica", 15, QFont.Bold))
        lbl.setAlignment(Qt.AlignCenter)
        lbl.setStyleSheet(f"color: {TEXT_MAIN}; background: transparent;")
        v.addWidget(lbl)

        img_frame = QFrame()
        img_frame.setFixedSize(180, 180)
        img_frame.setStyleSheet(f"QFrame {{ background-color: {DARK_BG}; border-radius: 8px; }}")
        img_v = QVBoxLayout(img_frame)
        img_v.setAlignment(Qt.AlignCenter)

        img_loaded = False
        if q.get("image_path"):
            app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            abs_path = os.path.join(app_dir, q["image_path"])
            if os.path.exists(abs_path):
                try:
                    pix = QPixmap(abs_path).scaled(160, 160, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    img_lbl = QLabel()
                    img_lbl.setPixmap(pix)
                    img_lbl.setAlignment(Qt.AlignCenter)
                    img_lbl.setStyleSheet("background: transparent;")
                    img_v.addWidget(img_lbl)
                    img_loaded = True
                except Exception:
                    pass

        if not img_loaded:
            ph = QLabel(f"[ Sign {q['letter']} ]")
            ph.setFont(QFont("Helvetica", 13, QFont.Bold))
            ph.setAlignment(Qt.AlignCenter)
            ph.setStyleSheet(f"color: {ORANGE}; background: transparent;")
            img_v.addWidget(ph)

        img_wrap = QHBoxLayout()
        img_wrap.addStretch(1)
        img_wrap.addWidget(img_frame)
        img_wrap.addStretch(1)
        v.addLayout(img_wrap)

        # 2x2 choice grid
        grid = QGridLayout()
        grid.setSpacing(8)
        self.choice_btns = []
        for idx, choice in enumerate(q["choices"]):
            r = idx // 2
            c = idx % 2
            btn = QPushButton(choice)
            btn.setFixedHeight(42)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet(
                f"QPushButton {{ background-color: {BLUE_ACCENT}; color: {TEXT_MAIN}; "
                f"border: none; border-radius: 6px; font-size: 13px; }}"
                f"QPushButton:hover {{ background-color: {RED_ACCENT}; }}"
            )
            btn.clicked.connect(lambda checked, ch=choice: self._submit_flashcard_answer(ch))
            grid.addWidget(btn, r, c)
            self.choice_btns.append(btn)

        v.addLayout(grid)

    def _submit_flashcard_answer(self, choice: str) -> None:
        if self.question_answered or self._locked:
            return
        self.question_answered = True

        q = self.questions[self.current_idx]
        correct_ans = q["correct_answer"]
        is_correct = (choice == correct_ans)

        user_id = self.controller.current_user_id
        try:
            self.quiz_engine.record_question_outcome(user_id, q["lesson_id"], is_correct)
        except Exception as e:
            print(f"[Quiz] record_outcome error: {e}")

        if is_correct:
            self.score += 1

        for btn in self.choice_btns:
            btn_text = btn.text()
            if btn_text == correct_ans:
                btn.setStyleSheet(
                    f"QPushButton {{ background-color: {ACCENT}; color: {DARK_BG}; "
                    f"border: none; border-radius: 6px; font-size: 13px; }}"
                )
            elif btn_text == choice and not is_correct:
                btn.setStyleSheet(
                    f"QPushButton {{ background-color: {RED_ACCENT}; color: white; "
                    f"border: none; border-radius: 6px; font-size: 13px; }}"
                )
            btn.setEnabled(False)

        next_btn = QPushButton("Next Question ➔")
        next_btn.setFixedHeight(40)
        next_btn.setCursor(Qt.PointingHandCursor)
        next_btn.setStyleSheet(
            f"QPushButton {{ background-color: {ACCENT}; color: {DARK_BG}; "
            f"border: none; border-radius: 6px; font-weight: bold; }}"
            f"QPushButton:hover {{ background-color: {BLUE_ACCENT}; color: white; }}"
        )
        next_btn.clicked.connect(self._next_question)
        self._main_layout.addWidget(next_btn)

    def _build_sign_it_ui(self, parent: QFrame, q: Dict[str, Any]) -> None:
        v = QVBoxLayout(parent)
        v.setContentsMargins(20, 15, 20, 15)
        v.setSpacing(10)

        lbl = QLabel(f"SIGN IT: Demonstrate letter '{q['letter']}'")
        lbl.setFont(QFont("Helvetica", 15, QFont.Bold))
        lbl.setAlignment(Qt.AlignCenter)
        lbl.setStyleSheet(f"color: {TEXT_MAIN}; background: transparent;")
        v.addWidget(lbl)

        split = QHBoxLayout()
        split.setSpacing(15)

        self._cam_lbl = QLabel("Camera Offline\nClick 'Start Camera'")
        self._cam_lbl.setAlignment(Qt.AlignCenter)
        self._cam_lbl.setStyleSheet(
            f"background-color: {DARK_BG}; color: {TEXT_DIM}; border-radius: 6px;"
        )
        self._cam_lbl.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        split.addWidget(self._cam_lbl, 3)

        ctrl_frame = QFrame()
        ctrl_frame.setStyleSheet("background: transparent;")
        ctrl = QVBoxLayout(ctrl_frame)
        ctrl.setSpacing(10)

        self._q_progress = _progress_bar()
        ctrl.addWidget(self._q_progress)

        self._q_status = QLabel("Ready...")
        self._q_status.setFont(QFont("Helvetica", 12))
        self._q_status.setStyleSheet(f"color: {TEXT_DIM}; background: transparent;")
        ctrl.addWidget(self._q_status)

        self._cam_btn = QPushButton("Start Camera")
        self._cam_btn.setFixedHeight(36)
        self._cam_btn.setCursor(Qt.PointingHandCursor)
        self._cam_btn.setStyleSheet(
            f"QPushButton {{ background-color: {BLUE_ACCENT}; color: white; "
            f"border: none; border-radius: 6px; }}"
            f"QPushButton:hover {{ background-color: {RED_ACCENT}; }}"
        )
        self._cam_btn.clicked.connect(self._toggle_camera)
        ctrl.addWidget(self._cam_btn)

        if self.controller.settings.get("dev_mode", "Disabled") == "Enabled":
            sim_btn = QPushButton("Simulate Correct")
            sim_btn.setFixedHeight(36)
            sim_btn.setCursor(Qt.PointingHandCursor)
            sim_btn.setStyleSheet(
                f"QPushButton {{ background: transparent; color: {RED_ACCENT}; "
                f"border: 1px solid {RED_ACCENT}; border-radius: 6px; }}"
                f"QPushButton:hover {{ background-color: {RED_ACCENT}; color: white; }}"
            )
            sim_btn.clicked.connect(self._simulate_correct_sign)
            ctrl.addWidget(sim_btn)

        ctrl.addStretch(1)
        split.addWidget(ctrl_frame, 2)

        v.addLayout(split, 1)

        self.matching_frames = 0
        self.best_confidence = 0.0
        self._start_camera()

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
            self.cap = None
            if hasattr(self, "_cam_lbl"):
                self._cam_lbl.setText("Webcam not found.")
            return
        self.is_running = True
        if hasattr(self, "_cam_btn"):
            self._cam_btn.setText("Stop Camera")
            self._cam_btn.setStyleSheet(
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

    def _update_camera_loop(self) -> None:
        # _locked is set before any UI teardown — guards against timer firing
        # between stop() and the actual widget deletion
        if self._locked or not self.is_running or not self.cap or self.question_answered:
            return

        try:
            ret, frame = self.cap.read()
            if not ret:
                self._stop_camera()
                return

            frame = cv2.flip(frame, 1)
            annotated, pred_label, confidence = self.detector.process_frame(frame)
            q = self.questions[self.current_idx]

            if pred_label and pred_label == q["letter"].upper() and confidence >= 0.80:
                self.matching_frames += 1
                self.best_confidence = max(self.best_confidence, confidence)
                progress = min(100, int(self.matching_frames / self.required_frames * 100))
                self._q_progress.setValue(progress)
                self._q_status.setText(f"Matching... ({self.matching_frames}/{self.required_frames})")
                self._q_status.setStyleSheet(f"color: {ACCENT}; background: transparent;")
                if self.matching_frames >= self.required_frames:
                    self._submit_sign_it_answer(True)
                    return
            else:
                if self.matching_frames > 0:
                    self.matching_frames -= 1
                    self._q_progress.setValue(int(self.matching_frames / self.required_frames * 100))

            rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb.shape
            rgb_resized = cv2.resize(rgb, (320, 240))
            qimg = QImage(rgb_resized.data, 320, 240, 320 * 3, QImage.Format_RGB888)
            self._cam_lbl.setPixmap(QPixmap.fromImage(qimg))

        except Exception as e:
            print(f"[Quiz] camera error: {e}")
            self._stop_camera()

    def _simulate_correct_sign(self) -> None:
        self.best_confidence = 0.90
        self._submit_sign_it_answer(True)

    def _submit_sign_it_answer(self, is_correct: bool) -> None:
        if self.question_answered or self._locked:
            return
        # Lock first — prevents any further timer ticks from touching these widgets
        self._locked = True
        self.question_answered = True
        self._stop_camera()

        q = self.questions[self.current_idx]
        user_id = self.controller.current_user_id
        try:
            self.quiz_engine.record_question_outcome(user_id, q["lesson_id"], is_correct)
        except Exception as e:
            print(f"[Quiz] record_outcome error: {e}")

        if is_correct:
            self.score += 1
            self._q_status.setText("✓ Correct! Sign matched.")
            self._q_status.setStyleSheet(f"color: {ACCENT}; background: transparent;")
        else:
            self._q_status.setText("❌ Skip/Incorrect")
            self._q_status.setStyleSheet(f"color: {RED_ACCENT}; background: transparent;")

        self._q_progress.setValue(100)

        next_btn = QPushButton("Next Question ➔")
        next_btn.setFixedHeight(40)
        next_btn.setCursor(Qt.PointingHandCursor)
        next_btn.setStyleSheet(
            f"QPushButton {{ background-color: {ACCENT}; color: {DARK_BG}; "
            f"border: none; border-radius: 6px; font-weight: bold; }}"
            f"QPushButton:hover {{ background-color: {BLUE_ACCENT}; color: white; }}"
        )
        next_btn.clicked.connect(self._next_question)
        self._main_layout.addWidget(next_btn)

    def _next_question(self) -> None:
        self._locked = True
        self._stop_camera()
        self.current_idx += 1
        # singleShot gives deleteLater() time to run before we rebuild the UI
        QTimer.singleShot(30, self._show_current_question)

    def _show_score_screen(self) -> None:
        self._locked = True
        self._stop_camera()
        self._clear_layout()
        user_id = self.controller.current_user_id
        mode = "MIXED"
        try:
            xp_earned, bonus, badges = self.quiz_engine.complete_quiz(
                user_id, self.score, len(self.questions), mode
            )
        except Exception as e:
            print(f"[Quiz] complete_quiz error: {e}")
            xp_earned, bonus, badges = 0, 0, []

        self._main_layout.addStretch(1)

        title = QLabel("Quiz Completed! 🎉")
        title.setFont(QFont("Helvetica", 26, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"color: {ACCENT};")
        self._main_layout.addWidget(title)

        score_lbl = QLabel(f"Your Score: {self.score} / {len(self.questions)}")
        score_lbl.setFont(QFont("Helvetica", 18, QFont.Bold))
        score_lbl.setAlignment(Qt.AlignCenter)
        score_lbl.setStyleSheet(f"color: {TEXT_MAIN};")
        self._main_layout.addWidget(score_lbl)

        xp_lbl = QLabel(
            f"Base XP: +{self.score * 5} XP\nBonus XP: +{bonus} XP\nTotal Earned: +{xp_earned} XP"
        )
        xp_lbl.setFont(QFont("Helvetica", 13))
        xp_lbl.setAlignment(Qt.AlignCenter)
        xp_lbl.setStyleSheet(f"color: {TEXT_DIM};")
        self._main_layout.addWidget(xp_lbl)

        if badges:
            badge_lbl = QLabel(f"🏆 Newly Unlocked Badges: {', '.join(badges)}")
            badge_lbl.setFont(QFont("Helvetica", 13, QFont.Bold))
            badge_lbl.setAlignment(Qt.AlignCenter)
            badge_lbl.setStyleSheet(f"color: {ORANGE};")
            self._main_layout.addWidget(badge_lbl)

        finish_btn = QPushButton("Finish & Go Home")
        finish_btn.setFixedHeight(44)
        finish_btn.setMaximumWidth(240)
        finish_btn.setFont(QFont("Helvetica", 13, QFont.Bold))
        finish_btn.setCursor(Qt.PointingHandCursor)
        finish_btn.setStyleSheet(
            f"QPushButton {{ background-color: {ACCENT}; color: {DARK_BG}; "
            f"border: none; border-radius: 6px; }}"
            f"QPushButton:hover {{ background-color: {BLUE_ACCENT}; color: white; }}"
        )
        finish_btn.clicked.connect(lambda: self.controller.show_screen("home"))
        btn_wrap = QHBoxLayout()
        btn_wrap.addStretch(1)
        btn_wrap.addWidget(finish_btn)
        btn_wrap.addStretch(1)
        self._main_layout.addLayout(btn_wrap)

        self._main_layout.addStretch(1)

    def on_leave(self) -> None:
        self._locked = True
        self._stop_camera()
