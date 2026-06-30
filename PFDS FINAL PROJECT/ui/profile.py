# Profile and Badges Screen for SignBridge
import os
from PIL import Image

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QScrollArea, QGridLayout, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap

from modules.gamification.badge_engine import BADGES
from modules.gamification.xp_engine import get_level_info


DARK_BG = "#0d0d1a"
CARD_BG = "#1a1a2e"
ACCENT = "#00d4aa"
RED_ACCENT = "#e94560"
BLUE_ACCENT = "#0f3460"
ORANGE = "#ffaa00"
TEXT_MAIN = "#e0e0e0"
TEXT_DIM = "#a0a0b0"

AVATAR_IMAGE_PATHS = {
    1: "assets/icons/avatars/avatar_1.png",
    2: "assets/icons/avatars/avatar_2.png",
    3: "assets/icons/avatars/avatar_3.png",
    4: "assets/icons/avatars/avatar_4.png",
    5: "assets/icons/avatars/avatar_5.png",
    6: "assets/icons/avatars/avatar_6.png",
}

BADGE_IMAGE_PATHS = {
    "first_sign": "assets/icons/badge/first_sign.png",
    "bilingual": "assets/icons/badge/bilingual.png",
    "week_warrior": "assets/icons/badge/week_warrior.png",
    "quiz_ace": "assets/icons/badge/quiz_ace.png",
}


def _load_pixmap(abs_path: str, size: tuple) -> QPixmap:
    if os.path.exists(abs_path):
        try:
            pix = QPixmap(abs_path).scaled(size[0], size[1], Qt.KeepAspectRatio, Qt.SmoothTransformation)
            return pix
        except Exception:
            pass
    return None


class ProfileScreen(QWidget):
    """Displays the user's profile card, stats summary, avatar selector, and badges grid."""

    def __init__(self, controller) -> None:
        super().__init__()
        self.controller = controller
        self.db = controller.db_manager
        self.app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.setStyleSheet(f"background-color: {DARK_BG};")

    def refresh(self) -> None:
        if self.layout():
            while self.layout().count():
                item = self.layout().takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
            QWidget().setLayout(self.layout())

        user_id = self.controller.current_user_id
        user = self.db.get_user_by_id(user_id)
        if not user:
            return

        lvl_info = get_level_info(user["xp"])
        unlocked_badges = self.db.get_unlocked_badges(user_id)

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # LEFT: profile card
        left_panel = QFrame()
        left_panel.setStyleSheet(f"QFrame {{ background-color: {CARD_BG}; border-radius: 12px; }}")
        left_v = QVBoxLayout(left_panel)
        left_v.setContentsMargins(20, 25, 20, 20)
        left_v.setSpacing(8)
        left_v.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        # Avatar
        current_avatar_idx = user.get("avatar_id", 1)
        avatar_rel = AVATAR_IMAGE_PATHS.get(current_avatar_idx, AVATAR_IMAGE_PATHS[1])
        avatar_abs = os.path.join(self.app_dir, avatar_rel)
        avatar_pix = _load_pixmap(avatar_abs, (96, 96))

        avatar_lbl = QLabel()
        avatar_lbl.setAlignment(Qt.AlignCenter)
        avatar_lbl.setStyleSheet("background: transparent;")
        if avatar_pix:
            avatar_lbl.setPixmap(avatar_pix)
        else:
            avatar_lbl.setText("👤")
            avatar_lbl.setFont(QFont("Helvetica", 56))
            avatar_lbl.setStyleSheet(f"color: {TEXT_DIM}; background: transparent;")
        left_v.addWidget(avatar_lbl)

        display_lbl = QLabel(user["display_name"])
        display_lbl.setFont(QFont("Helvetica", 20, QFont.Bold))
        display_lbl.setAlignment(Qt.AlignCenter)
        display_lbl.setStyleSheet(f"color: {TEXT_MAIN}; background: transparent;")
        left_v.addWidget(display_lbl)

        username_lbl = QLabel(f"@{user['username']}")
        username_lbl.setFont(QFont("Helvetica", 13))
        username_lbl.setAlignment(Qt.AlignCenter)
        username_lbl.setStyleSheet(f"color: {TEXT_DIM}; font-style: italic; background: transparent;")
        left_v.addWidget(username_lbl)

        left_v.addSpacing(10)

        # Avatar selector
        sel_hdr = QLabel("CHOOSE AVATAR")
        sel_hdr.setFont(QFont("Helvetica", 10, QFont.Bold))
        sel_hdr.setAlignment(Qt.AlignCenter)
        sel_hdr.setStyleSheet(f"color: {ACCENT}; background: transparent;")
        left_v.addWidget(sel_hdr)

        selector_row = QHBoxLayout()
        selector_row.setAlignment(Qt.AlignCenter)
        selector_row.setSpacing(4)

        for av_id, rel_path in AVATAR_IMAGE_PATHS.items():
            abs_path = os.path.join(self.app_dir, rel_path)
            av_pix = _load_pixmap(abs_path, (36, 36))
            is_selected = (av_id == current_avatar_idx)

            av_btn = QPushButton()
            av_btn.setFixedSize(44, 44)
            av_btn.setCursor(Qt.PointingHandCursor)
            if av_pix:
                av_btn.setIcon(self.style().standardIcon(0))
                av_btn.setIcon(self._pix_to_icon(av_pix))
                av_btn.setIconSize(av_pix.size())
            else:
                av_btn.setText(str(av_id))

            border_color = ACCENT if is_selected else "transparent"
            av_btn.setStyleSheet(
                f"QPushButton {{ background-color: {BLUE_ACCENT if is_selected else 'transparent'}; "
                f"border: 2px solid {border_color}; border-radius: 6px; }}"
                f"QPushButton:hover {{ background-color: {BLUE_ACCENT}; }}"
            )
            av_btn.clicked.connect(lambda checked, aid=av_id: self._update_avatar(aid))
            selector_row.addWidget(av_btn)

        left_v.addLayout(selector_row)
        left_v.addSpacing(10)

        # Stats box
        stats_box = QFrame()
        stats_box.setStyleSheet(f"QFrame {{ background-color: {DARK_BG}; border-radius: 8px; }}")
        stats_v = QVBoxLayout(stats_box)
        stats_v.setContentsMargins(15, 10, 15, 10)
        stats_v.setSpacing(4)

        for text, color in [
            (f"Level {lvl_info['level']} · {lvl_info['tier_name']}", ACCENT),
            (f"Total XP: {user['xp']} XP", TEXT_MAIN),
            (f"Active Streak: 🔥 {user['streak']} Days", RED_ACCENT),
        ]:
            lbl = QLabel(text)
            lbl.setFont(QFont("Helvetica", 12, QFont.Bold if color == ACCENT else QFont.Normal))
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setStyleSheet(f"color: {color}; background: transparent;")
            stats_v.addWidget(lbl)

        left_v.addWidget(stats_box)
        left_v.addStretch(1)

        main_layout.addWidget(left_panel, 2)

        # RIGHT: badges
        right_panel = QWidget()
        right_panel.setStyleSheet("background: transparent;")
        right_v = QVBoxLayout(right_panel)
        right_v.setContentsMargins(0, 0, 0, 0)
        right_v.setSpacing(10)

        badges_title = QLabel("Achievements & Badges")
        badges_title.setFont(QFont("Helvetica", 20, QFont.Bold))
        badges_title.setStyleSheet(f"color: {TEXT_MAIN};")
        right_v.addWidget(badges_title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(
            f"QScrollArea {{ background-color: {CARD_BG}; border-radius: 12px; border: none; }}"
            f"QScrollBar:vertical {{ background: {DARK_BG}; width: 8px; border-radius: 4px; }}"
            f"QScrollBar::handle:vertical {{ background: {BLUE_ACCENT}; border-radius: 4px; }}"
        )

        grid_widget = QWidget()
        grid_widget.setStyleSheet(f"background-color: {CARD_BG};")
        grid_layout = QGridLayout(grid_widget)
        grid_layout.setContentsMargins(10, 10, 10, 10)
        grid_layout.setSpacing(12)

        col_idx = 0
        row_idx = 0

        for badge_id, details in BADGES.items():
            is_unlocked = badge_id in unlocked_badges

            badge_card = QFrame()
            badge_card.setFixedHeight(130)
            badge_card.setStyleSheet(
                f"QFrame {{ background-color: {'#0d0d1a' if is_unlocked else '#151525'}; border-radius: 10px; }}"
            )
            card_v = QVBoxLayout(badge_card)
            card_v.setContentsMargins(8, 8, 8, 8)
            card_v.setSpacing(3)
            card_v.setAlignment(Qt.AlignCenter)

            # Badge image / emoji
            badge_img_path = BADGE_IMAGE_PATHS.get(badge_id)
            badge_pix = None
            if badge_img_path and is_unlocked:
                abs_badge = os.path.join(self.app_dir, badge_img_path)
                badge_pix = _load_pixmap(abs_badge, (40, 40))

            icon_lbl = QLabel()
            icon_lbl.setAlignment(Qt.AlignCenter)
            icon_lbl.setStyleSheet("background: transparent;")
            if badge_pix:
                icon_lbl.setPixmap(badge_pix)
            else:
                emoji_char = details["emoji"] if is_unlocked else "🔒"
                emoji_color = TEXT_MAIN if is_unlocked else "#505060"
                icon_lbl.setText(emoji_char)
                icon_lbl.setFont(QFont("Helvetica", 28))
                icon_lbl.setStyleSheet(f"color: {emoji_color}; background: transparent;")
            card_v.addWidget(icon_lbl)

            name_lbl = QLabel(details["name"])
            name_lbl.setFont(QFont("Helvetica", 11, QFont.Bold))
            name_lbl.setAlignment(Qt.AlignCenter)
            name_lbl.setStyleSheet(
                f"color: {ORANGE if is_unlocked else '#606070'}; background: transparent;"
            )
            card_v.addWidget(name_lbl)

            desc_lbl = QLabel(details["description"])
            desc_lbl.setFont(QFont("Helvetica", 9))
            desc_lbl.setAlignment(Qt.AlignCenter)
            desc_lbl.setWordWrap(True)
            desc_lbl.setStyleSheet(
                f"color: {TEXT_DIM if is_unlocked else '#454555'}; background: transparent;"
            )
            card_v.addWidget(desc_lbl)

            grid_layout.addWidget(badge_card, row_idx, col_idx)

            col_idx += 1
            if col_idx > 1:
                col_idx = 0
                row_idx += 1

        scroll.setWidget(grid_widget)
        right_v.addWidget(scroll, 1)

        main_layout.addWidget(right_panel, 3)

    def _pix_to_icon(self, pix: QPixmap):
        from PyQt5.QtGui import QIcon
        return QIcon(pix)

    def _update_avatar(self, avatar_id: int) -> None:
        user_id = self.controller.current_user_id
        sql = "UPDATE users SET avatar_id = ? WHERE id = ?"
        with self.db.get_connection() as conn:
            conn.execute(sql, (avatar_id, user_id))
            conn.commit()
        self.refresh()
