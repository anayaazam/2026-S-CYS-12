# Learn Screen for SignBridge
import os
from PIL import Image
from typing import Optional, Dict, Any

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QScrollArea, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap


DARK_BG = "#0d0d1a"
CARD_BG = "#1a1a2e"
ACCENT = "#00d4aa"
RED_ACCENT = "#e94560"
BLUE_ACCENT = "#0f3460"
ORANGE = "#ffaa00"
TEXT_MAIN = "#e0e0e0"
TEXT_DIM = "#a0a0b0"


class LearnScreen(QWidget):
    """Provides a browser for learning units and lessons, complete with lesson details."""

    def __init__(self, controller) -> None:
        super().__init__()
        self.controller = controller
        self.db = controller.db_manager
        self.selected_lesson: Optional[Dict[str, Any]] = None
        self.setStyleSheet(f"background-color: {DARK_BG};")
        self._right_panel = None

    def refresh(self) -> None:
        if self.layout():
            while self.layout().count():
                item = self.layout().takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
            QWidget().setLayout(self.layout())

        user_id = self.controller.current_user_id
        progress = self.db.get_user_progress(user_id)

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # LEFT PANEL
        left_panel = QWidget()
        left_panel.setStyleSheet("background: transparent;")
        left_v = QVBoxLayout(left_panel)
        left_v.setContentsMargins(0, 0, 0, 0)
        left_v.setSpacing(10)

        title = QLabel("Course Curriculum")
        title.setFont(QFont("Helvetica", 20, QFont.Bold))
        title.setStyleSheet(f"color: {TEXT_MAIN};")
        left_v.addWidget(title)

        # Scrollable list
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(
            f"QScrollArea {{ background-color: {CARD_BG}; border-radius: 10px; border: none; }}"
            f"QScrollBar:vertical {{ background: {DARK_BG}; width: 8px; border-radius: 4px; }}"
            f"QScrollBar::handle:vertical {{ background: {BLUE_ACCENT}; border-radius: 4px; }}"
        )

        scroll_content = QWidget()
        scroll_content.setStyleSheet(f"background-color: {CARD_BG};")
        scroll_v = QVBoxLayout(scroll_content)
        scroll_v.setContentsMargins(10, 10, 10, 10)
        scroll_v.setSpacing(4)

        units = [
            (1, "Unit 1: ASL Alphabet"),
            (2, "Unit 2: Common Words"),
            (3, "Unit 3: Numbers"),
        ]

        first_lesson = None

        for u_id, u_title in units:
            unit_lessons = self.db.get_lessons_by_unit(u_id)
            completed_in_unit = sum(
                1 for l in unit_lessons
                if l["id"] in progress and progress[l["id"]]["completed"]
            )
            total_in_unit = len(unit_lessons)
            pct = int((completed_in_unit / total_in_unit) * 100) if total_in_unit else 0

            unit_lbl = QLabel(f"{u_title.upper()}  —  {pct}% complete")
            unit_lbl.setFont(QFont("Helvetica", 11, QFont.Bold))
            unit_lbl.setStyleSheet(f"color: {ACCENT}; background: transparent; padding: 10px 5px 4px 5px;")
            scroll_v.addWidget(unit_lbl)

            for lesson in unit_lessons:
                if not first_lesson:
                    first_lesson = lesson

                l_id = lesson["id"]
                is_done = l_id in progress and progress[l_id]["completed"]
                has_started = l_id in progress

                if is_done:
                    bg = BLUE_ACCENT
                    status_char = "✓"
                    status_color = ACCENT
                    name_color = "#c0faf0"
                    btn_color = ACCENT
                    btn_text = "#0d0d1a"
                elif has_started:
                    bg = "#0d1a2e"
                    status_char = "◉"
                    status_color = RED_ACCENT
                    name_color = TEXT_MAIN
                    btn_color = RED_ACCENT
                    btn_text = "#ffffff"
                else:
                    bg = DARK_BG
                    status_char = "○"
                    status_color = ORANGE
                    name_color = "#ffcc66"
                    btn_color = ORANGE
                    btn_text = DARK_BG

                row = QFrame()
                row.setFixedHeight(45)
                row.setStyleSheet(f"QFrame {{ background-color: {bg}; border-radius: 6px; }}")
                row_h = QHBoxLayout(row)
                row_h.setContentsMargins(12, 0, 12, 0)
                row_h.setSpacing(10)

                s_lbl = QLabel(status_char)
                s_lbl.setFont(QFont("Helvetica", 16, QFont.Bold))
                s_lbl.setStyleSheet(f"color: {status_color}; background: transparent;")
                s_lbl.setFixedWidth(24)
                row_h.addWidget(s_lbl)

                n_lbl = QLabel(f"{lesson['sign_name']} (Sign)")
                n_lbl.setFont(QFont("Helvetica", 13, QFont.Bold if is_done else QFont.Normal))
                n_lbl.setStyleSheet(f"color: {name_color}; background: transparent;")
                row_h.addWidget(n_lbl, 1)

                view_btn = QPushButton("View")
                view_btn.setFixedSize(60, 26)
                view_btn.setCursor(Qt.PointingHandCursor)
                view_btn.setStyleSheet(
                    f"QPushButton {{ background-color: {btn_color}; color: {btn_text}; "
                    f"border: none; border-radius: 4px; font-size: 11px; font-weight: bold; }}"
                    f"QPushButton:hover {{ background-color: {RED_ACCENT}; color: white; }}"
                )
                view_btn.clicked.connect(lambda checked, l=lesson: self._display_lesson_details(l))
                row_h.addWidget(view_btn)

                scroll_v.addWidget(row)

        scroll_v.addStretch(1)
        scroll.setWidget(scroll_content)
        left_v.addWidget(scroll, 1)
        main_layout.addWidget(left_panel, 3)

        # RIGHT PANEL
        self._right_panel = QFrame()
        self._right_panel.setStyleSheet(
            f"QFrame {{ background-color: {CARD_BG}; border-radius: 10px; }}"
        )
        self._right_panel_layout = QVBoxLayout(self._right_panel)
        self._right_panel_layout.setContentsMargins(20, 20, 20, 20)
        self._right_panel_layout.setSpacing(10)
        main_layout.addWidget(self._right_panel, 2)

        if self.selected_lesson:
            updated = self.db.get_lesson_by_id(self.selected_lesson["id"])
            self._display_lesson_details(updated)
        elif first_lesson:
            self._display_lesson_details(first_lesson)

    def _display_lesson_details(self, lesson: Dict[str, Any]) -> None:
        self.selected_lesson = lesson

        # Clear right panel
        while self._right_panel_layout.count():
            item = self._right_panel_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        title = QLabel(lesson["sign_name"])
        title.setFont(QFont("Helvetica", 22, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"color: {TEXT_MAIN}; background: transparent;")
        self._right_panel_layout.addWidget(title)

        sub = QLabel(f"Target sign: '{lesson['letter']}' · Unit {lesson['unit_id']}")
        sub.setFont(QFont("Helvetica", 12))
        sub.setAlignment(Qt.AlignCenter)
        sub.setStyleSheet(f"color: {ACCENT}; font-style: italic; background: transparent;")
        self._right_panel_layout.addWidget(sub)

        # Image container
        img_frame = QFrame()
        img_frame.setFixedSize(220, 220)
        img_frame.setStyleSheet(f"QFrame {{ background-color: {DARK_BG}; border-radius: 8px; }}")
        img_v = QVBoxLayout(img_frame)
        img_v.setAlignment(Qt.AlignCenter)

        img_loaded = False
        if lesson["image_path"]:
            app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            abs_path = os.path.join(app_dir, lesson["image_path"])
            if os.path.exists(abs_path):
                try:
                    pix = QPixmap(abs_path).scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    img_lbl = QLabel()
                    img_lbl.setPixmap(pix)
                    img_lbl.setAlignment(Qt.AlignCenter)
                    img_lbl.setStyleSheet("background: transparent;")
                    img_v.addWidget(img_lbl)
                    img_loaded = True
                except Exception:
                    pass

        if not img_loaded:
            ph = QLabel(f"[ Sign {lesson['letter']} ]\n(Image file missing)")
            ph.setFont(QFont("Helvetica", 13, QFont.Bold))
            ph.setAlignment(Qt.AlignCenter)
            ph.setStyleSheet(f"color: {ORANGE}; background: transparent;")
            img_v.addWidget(ph)

        img_wrapper = QHBoxLayout()
        img_wrapper.addStretch(1)
        img_wrapper.addWidget(img_frame)
        img_wrapper.addStretch(1)
        self._right_panel_layout.addLayout(img_wrapper)

        desc_title = QLabel("HOW TO SIGN:")
        desc_title.setFont(QFont("Helvetica", 10, QFont.Bold))
        desc_title.setStyleSheet(f"color: {TEXT_DIM}; background: transparent;")
        self._right_panel_layout.addWidget(desc_title)

        desc_body = QLabel(lesson["description"])
        desc_body.setFont(QFont("Helvetica", 13))
        desc_body.setStyleSheet(f"color: {TEXT_MAIN}; background: transparent;")
        desc_body.setWordWrap(True)
        self._right_panel_layout.addWidget(desc_body)

        self._right_panel_layout.addStretch(1)

        practice_btn = QPushButton("Practice This Sign")
        practice_btn.setFixedHeight(40)
        practice_btn.setFont(QFont("Helvetica", 13, QFont.Bold))
        practice_btn.setCursor(Qt.PointingHandCursor)
        practice_btn.setStyleSheet(
            f"QPushButton {{ background-color: {BLUE_ACCENT}; color: {TEXT_MAIN}; "
            f"border: none; border-radius: 6px; }}"
            f"QPushButton:hover {{ background-color: {RED_ACCENT}; }}"
        )
        practice_btn.clicked.connect(
            lambda: self.controller.show_screen("practice", lesson_id=lesson["id"])
        )
        self._right_panel_layout.addWidget(practice_btn)
