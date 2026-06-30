# Leaderboard Screen for SignBridge
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QScrollArea, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


DARK_BG = "#0d0d1a"
CARD_BG = "#1a1a2e"
ACCENT = "#00d4aa"
RED_ACCENT = "#e94560"
BLUE_ACCENT = "#0f3460"
ORANGE = "#ffaa00"
TEXT_MAIN = "#e0e0e0"
TEXT_DIM = "#a0a0b0"


class LeaderboardScreen(QWidget):
    """Displays a scrollable table of top users ranked by total XP."""

    def __init__(self, controller) -> None:
        super().__init__()
        self.controller = controller
        self.db = controller.db_manager
        self.setStyleSheet(f"background-color: {DARK_BG};")

    def refresh(self) -> None:
        if self.layout():
            while self.layout().count():
                item = self.layout().takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
            QWidget().setLayout(self.layout())

        current_user_id = self.controller.current_user_id
        outer = QVBoxLayout(self)
        outer.setContentsMargins(30, 25, 30, 15)
        outer.setSpacing(10)

        title_lbl = QLabel("Global Leaderboard")
        title_lbl.setFont(QFont("Helvetica", 22, QFont.Bold))
        title_lbl.setStyleSheet(f"color: {TEXT_MAIN};")
        outer.addWidget(title_lbl)

        # Table container
        table_container = QFrame()
        table_container.setStyleSheet(
            f"QFrame {{ background-color: {CARD_BG}; border-radius: 12px; }}"
        )
        table_v = QVBoxLayout(table_container)
        table_v.setContentsMargins(15, 10, 15, 10)
        table_v.setSpacing(5)

        # Header row
        header_row = QHBoxLayout()
        header_row.setContentsMargins(10, 0, 10, 0)
        header_row.setSpacing(0)

        def _hdr(text, width=None, align=Qt.AlignLeft):
            lbl = QLabel(text)
            lbl.setFont(QFont("Helvetica", 10, QFont.Bold))
            lbl.setStyleSheet(f"color: {ACCENT}; background: transparent;")
            lbl.setAlignment(align)
            if width:
                lbl.setFixedWidth(width)
            return lbl

        header_row.addWidget(_hdr("RANK", 70))
        header_row.addWidget(_hdr("SIGNER"), 1)
        header_row.addWidget(_hdr("STREAK", 100, Qt.AlignCenter))
        header_row.addWidget(_hdr("TOTAL XP", 100, Qt.AlignRight))
        table_v.addLayout(header_row)

        # Separator
        sep = QFrame()
        sep.setFixedHeight(2)
        sep.setStyleSheet(f"background-color: {BLUE_ACCENT};")
        table_v.addWidget(sep)

        # Scrollable body
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(
            "QScrollArea { border: none; background: transparent; }"
            f"QScrollBar:vertical {{ background: {DARK_BG}; width: 8px; border-radius: 4px; }}"
            f"QScrollBar::handle:vertical {{ background: {BLUE_ACCENT}; border-radius: 4px; }}"
        )

        body_widget = QWidget()
        body_widget.setStyleSheet("background: transparent;")
        body_v = QVBoxLayout(body_widget)
        body_v.setContentsMargins(0, 0, 0, 0)
        body_v.setSpacing(2)

        top_users = self.db.get_leaderboard(limit=25)

        for idx, user in enumerate(top_users):
            rank = idx + 1
            is_current = (user["id"] == current_user_id)

            row = QFrame()
            row.setFixedHeight(45)
            row_bg = BLUE_ACCENT if is_current else "transparent"
            row.setStyleSheet(f"QFrame {{ background-color: {row_bg}; border-radius: 6px; }}")

            row_h = QHBoxLayout(row)
            row_h.setContentsMargins(10, 0, 10, 0)
            row_h.setSpacing(0)

            # Rank
            if rank == 1:
                rank_text = "🥇 1"
            elif rank == 2:
                rank_text = "🥈 2"
            elif rank == 3:
                rank_text = "🥉 3"
            else:
                rank_text = f"  {rank}"

            rank_lbl = QLabel(rank_text)
            rank_lbl.setFont(QFont("Helvetica", 13, QFont.Bold if rank <= 3 else QFont.Normal))
            rank_lbl.setFixedWidth(70)
            rank_lbl.setStyleSheet(
                f"color: {ORANGE if rank <= 3 else TEXT_MAIN}; background: transparent;"
            )
            row_h.addWidget(rank_lbl)

            # Name
            name_text = user["display_name"]
            if is_current:
                name_text += " (You)"
            name_lbl = QLabel(name_text)
            name_lbl.setFont(QFont("Helvetica", 13, QFont.Bold if is_current else QFont.Normal))
            name_lbl.setStyleSheet(
                f"color: {ACCENT if is_current else TEXT_MAIN}; background: transparent;"
            )
            row_h.addWidget(name_lbl, 1)

            # Streak
            streak_text = f"🔥 {user['streak']}" if user['streak'] > 0 else "-"
            streak_lbl = QLabel(streak_text)
            streak_lbl.setFont(QFont("Helvetica", 12))
            streak_lbl.setFixedWidth(100)
            streak_lbl.setAlignment(Qt.AlignCenter)
            streak_lbl.setStyleSheet(
                f"color: {RED_ACCENT if user['streak'] > 0 else TEXT_DIM}; background: transparent;"
            )
            row_h.addWidget(streak_lbl)

            # XP
            xp_lbl = QLabel(f"{user['xp']} XP")
            xp_lbl.setFont(QFont("Helvetica", 13, QFont.Bold))
            xp_lbl.setFixedWidth(100)
            xp_lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            xp_lbl.setStyleSheet(f"color: {ACCENT}; background: transparent;")
            row_h.addWidget(xp_lbl)

            body_v.addWidget(row)

        body_v.addStretch(1)
        scroll.setWidget(body_widget)
        table_v.addWidget(scroll, 1)

        outer.addWidget(table_container, 1)
