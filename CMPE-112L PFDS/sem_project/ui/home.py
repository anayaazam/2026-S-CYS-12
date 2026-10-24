# Home Dashboard Screen for SignBridge
import json
import random
from datetime import datetime

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QProgressBar, QSizePolicy, QScrollArea
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from modules.gamification.xp_engine import get_level_info


DARK_BG = "#0d0d1a"
CARD_BG = "#1a1a2e"
ACCENT = "#00d4aa"
RED_ACCENT = "#e94560"
BLUE_ACCENT = "#0f3460"
ORANGE = "#ffaa00"
TEXT_MAIN = "#e0e0e0"
TEXT_DIM = "#a0a0b0"


def _card(parent=None) -> QFrame:
    f = QFrame(parent)
    f.setStyleSheet(f"QFrame {{ background-color: {CARD_BG}; border-radius: 12px; }}")
    return f


def _progress_bar(value: float, color: str = ACCENT) -> QProgressBar:
    pb = QProgressBar()
    pb.setRange(0, 100)
    pb.setValue(int(value * 100))
    pb.setFixedHeight(10)
    pb.setTextVisible(False)
    pb.setStyleSheet(
        f"QProgressBar {{ background-color: {DARK_BG}; border-radius: 5px; border: none; }}"
        f"QProgressBar::chunk {{ background-color: {color}; border-radius: 5px; }}"
    )
    return pb


class HomeScreen(QWidget):
    """The landing dashboard showing streak, XP, curriculum progress, and daily challenge."""

    def __init__(self, controller) -> None:
        super().__init__()
        self.controller = controller
        self.db = controller.db_manager
        self.setStyleSheet(f"background-color: {DARK_BG};")

    def refresh(self) -> None:
        # Clear existing widgets
        if self.layout():
            while self.layout().count():
                item = self.layout().takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
            QWidget().setLayout(self.layout())

        outer = QVBoxLayout(self)
        outer.setContentsMargins(30, 25, 30, 20)
        outer.setSpacing(10)

        user_id = self.controller.current_user_id
        user = self.db.get_user_by_id(user_id)
        if not user:
            return

        # Header
        header = QHBoxLayout()
        welcome = QLabel(f"Welcome back, {user['display_name']}!")
        welcome.setFont(QFont("Helvetica", 22, QFont.Bold))
        welcome.setStyleSheet(f"color: {TEXT_MAIN};")
        header.addWidget(welcome)

        streak_val = user.get("streak", 0)
        streak_lbl = QLabel(f"🔥 {streak_val} Day Streak")
        streak_lbl.setFont(QFont("Helvetica", 15, QFont.Bold))
        streak_lbl.setStyleSheet(f"color: {RED_ACCENT};")
        streak_lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        header.addWidget(streak_lbl)
        outer.addLayout(header)

        # Two columns
        cols = QHBoxLayout()
        cols.setSpacing(20)

        left = QVBoxLayout()
        left.setSpacing(15)
        self._build_xp_card(left, user["xp"])
        self._build_curriculum_card(left, user_id)
        left.addStretch(1)

        right = QVBoxLayout()
        right.setSpacing(15)
        self._build_challenge_card(right, user_id)
        self._build_activity_card(right, user_id)
        right.addStretch(1)

        cols.addLayout(left, 1)
        cols.addLayout(right, 1)
        outer.addLayout(cols, 1)

    def _build_xp_card(self, layout: QVBoxLayout, xp: int) -> None:
        lvl_info = get_level_info(xp)
        card = _card()
        v = QVBoxLayout(card)
        v.setContentsMargins(20, 15, 20, 15)
        v.setSpacing(6)

        sec = QLabel("YOUR LEVEL PROGRESS")
        sec.setFont(QFont("Helvetica", 10, QFont.Bold))
        sec.setStyleSheet(f"color: {ACCENT}; background: transparent;")
        v.addWidget(sec)

        lvl = QLabel(f"Level {lvl_info['level']}: {lvl_info['tier_name']}")
        lvl.setFont(QFont("Helvetica", 16, QFont.Bold))
        lvl.setStyleSheet(f"color: {TEXT_MAIN}; background: transparent;")
        v.addWidget(lvl)

        v.addWidget(_progress_bar(lvl_info["progress"]))

        xp_text = (
            f"{xp} XP Total · {lvl_info['xp_needed']} XP to next level"
            if lvl_info["xp_needed"] > 0
            else f"{xp} XP Total (Max Level)"
        )
        xp_lbl = QLabel(xp_text)
        xp_lbl.setFont(QFont("Helvetica", 11))
        xp_lbl.setStyleSheet(f"color: {TEXT_DIM}; background: transparent;")
        v.addWidget(xp_lbl)

        layout.addWidget(card)

    def _build_curriculum_card(self, layout: QVBoxLayout, user_id: int) -> None:
        card = _card()
        v = QVBoxLayout(card)
        v.setContentsMargins(20, 15, 20, 15)
        v.setSpacing(8)

        header = QLabel("CURRICULUM PROGRESS")
        header.setFont(QFont("Helvetica", 10, QFont.Bold))
        header.setStyleSheet(f"color: {RED_ACCENT}; background: transparent;")
        v.addWidget(header)

        progress = self.db.get_user_progress(user_id)
        units = [
            (1, "Unit 1: ASL Alphabet", "learn"),
            (2, "Unit 2: Common Words", "learn"),
            (3, "Unit 3: Numbers", "learn"),
        ]

        for u_id, u_title, screen in units:
            lessons = self.db.get_lessons_by_unit(u_id)
            total = len(lessons)
            done = sum(1 for l in lessons if l["id"] in progress and progress[l["id"]]["completed"])
            pct = done / total if total else 0

            row = QHBoxLayout()
            row.setSpacing(8)

            name_lbl = QLabel(f"{u_title}  ({done}/{total})")
            name_lbl.setFont(QFont("Helvetica", 12))
            name_lbl.setStyleSheet(f"color: {TEXT_MAIN}; background: transparent;")
            name_lbl.setFixedWidth(220)
            row.addWidget(name_lbl)

            bar = _progress_bar(pct)
            bar.setFixedWidth(100)
            row.addWidget(bar)

            btn_color = BLUE_ACCENT if done > 0 else ORANGE
            btn_text_color = TEXT_MAIN if done > 0 else DARK_BG
            start_btn = QPushButton("Continue" if done > 0 else "Start")
            start_btn.setFixedSize(80, 26)
            start_btn.setCursor(Qt.PointingHandCursor)
            start_btn.setStyleSheet(
                f"QPushButton {{ background-color: {btn_color}; color: {btn_text_color}; "
                f"border: none; border-radius: 4px; font-size: 11px; font-weight: bold; }}"
                f"QPushButton:hover {{ background-color: {RED_ACCENT}; color: {TEXT_MAIN}; }}"
            )
            start_btn.clicked.connect(lambda checked, s=screen: self.controller.show_screen(s))
            row.addWidget(start_btn)
            row.addStretch(1)

            v.addLayout(row)

        layout.addWidget(card)

    def _build_challenge_card(self, layout: QVBoxLayout, user_id: int) -> None:
        card = _card()
        v = QVBoxLayout(card)
        v.setContentsMargins(20, 15, 20, 15)
        v.setSpacing(8)

        header = QLabel("DAILY CHALLENGE")
        header.setFont(QFont("Helvetica", 10, QFont.Bold))
        header.setStyleSheet(f"color: {ACCENT}; background: transparent;")
        v.addWidget(header)

        today_str = datetime.now().strftime("%Y-%m-%d")
        challenge = self.db.get_daily_challenge(user_id, today_str)
        lessons = self.db.get_lessons()

        if not lessons:
            return

        if not challenge:
            sample_size = min(5, len(lessons))
            selected = random.sample(lessons, sample_size)
            ids = [l["id"] for l in selected]
            self.db.save_daily_challenge(user_id, today_str, json.dumps(ids))
            challenge = self.db.get_daily_challenge(user_id, today_str)

        try:
            challenge_ids = json.loads(challenge["signs_json"])
        except Exception:
            challenge_ids = []

        progress = self.db.get_user_progress(user_id)
        completed_count = sum(
            1 for l_id in challenge_ids
            if l_id in progress and progress[l_id]["completed"]
        )

        status_text = (
            "5 signs today — Complete! 🎉"
            if challenge["completed"] or completed_count >= 5
            else f"5 signs today — {completed_count}/5 completed"
        )

        title = QLabel(status_text)
        title.setFont(QFont("Helvetica", 14, QFont.Bold))
        title.setStyleSheet(f"color: {TEXT_MAIN}; background: transparent;")
        v.addWidget(title)

        desc = QLabel("Practice the selected signs today to earn a +50 XP bonus reward.")
        desc.setFont(QFont("Helvetica", 12))
        desc.setStyleSheet(f"color: {TEXT_DIM}; background: transparent;")
        desc.setWordWrap(True)
        v.addWidget(desc)

        layout.addWidget(card)

    def _build_activity_card(self, layout: QVBoxLayout, user_id: int) -> None:
        card = _card()
        v = QVBoxLayout(card)
        v.setContentsMargins(20, 15, 20, 15)
        v.setSpacing(6)

        header = QLabel("RECENT ACTIVITY")
        header.setFont(QFont("Helvetica", 10, QFont.Bold))
        header.setStyleSheet(f"color: {TEXT_DIM}; background: transparent;")
        v.addWidget(header)

        progress = self.db.get_user_progress(user_id)

        recent_items = []
        for l_id, p in progress.items():
            if p.get("last_attempted"):
                lesson = self.db.get_lesson_by_id(l_id)
                if lesson:
                    recent_items.append(
                        (p["last_attempted"], f"Practiced sign: {lesson['sign_name']}")
                    )

        recent_items.sort(reverse=True, key=lambda x: x[0])

        if not recent_items:
            no_lbl = QLabel("No recent activity yet. Start learning!")
            no_lbl.setFont(QFont("Helvetica", 12))
            no_lbl.setStyleSheet(f"color: {TEXT_DIM}; background: transparent;")
            v.addWidget(no_lbl)
        else:
            for _, text in recent_items[:3]:
                item_lbl = QLabel(f"✓ {text}")
                item_lbl.setFont(QFont("Helvetica", 12))
                item_lbl.setStyleSheet(f"color: {ACCENT}; background: transparent;")
                v.addWidget(item_lbl)

        layout.addWidget(card)
