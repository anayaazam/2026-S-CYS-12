# Stats Screen for SignBridge
import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from typing import Dict, Any

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QSizePolicy
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


class StatsScreen(QWidget):
    """Embeds Matplotlib charts inside PyQt5 to show user progress analytics."""

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

        user_id = self.controller.current_user_id
        user = self.db.get_user_by_id(user_id)
        if not user:
            return

        progress = self.db.get_user_progress(user_id)
        quiz_stats = self.db.get_quiz_stats(user_id)
        lessons = self.db.get_lessons()

        total_lessons = len(lessons)
        completed_lessons = sum(1 for p in progress.values() if p.get("completed"))

        best_practice_acc = max([p.get("best_accuracy", 0.0) for p in progress.values()] or [0.0])
        best_overall_acc = max(best_practice_acc, quiz_stats.get("best_quiz_accuracy", 0.0) * 100)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(20, 15, 20, 10)
        outer.setSpacing(10)

        # --- SUMMARY TILES ---
        tiles_row = QHBoxLayout()
        tiles_row.setSpacing(10)

        stats_list = [
            ("Total XP", f"{user['xp']}", ACCENT),
            ("Streak", f"🔥 {user['streak']}", RED_ACCENT),
            ("Signs Learned", f"{completed_lessons}/{total_lessons}", BLUE_ACCENT),
            ("Quizzes Taken", f"{quiz_stats['quizzes_taken']}", ORANGE),
            ("Best Accuracy", f"{best_overall_acc:.1f}%", ACCENT),
        ]

        for t_title, t_val, t_color in stats_list:
            tile = QFrame()
            tile.setFixedHeight(85)
            tile.setStyleSheet(f"QFrame {{ background-color: {CARD_BG}; border-radius: 10px; }}")
            tile_v = QVBoxLayout(tile)
            tile_v.setAlignment(Qt.AlignCenter)
            tile_v.setSpacing(2)

            lbl_t = QLabel(t_title.upper())
            lbl_t.setFont(QFont("Helvetica", 9, QFont.Bold))
            lbl_t.setAlignment(Qt.AlignCenter)
            lbl_t.setStyleSheet(f"color: {TEXT_DIM}; background: transparent;")
            tile_v.addWidget(lbl_t)

            lbl_v = QLabel(t_val)
            lbl_v.setFont(QFont("Helvetica", 18, QFont.Bold))
            lbl_v.setAlignment(Qt.AlignCenter)
            lbl_v.setStyleSheet(f"color: {t_color}; background: transparent;")
            tile_v.addWidget(lbl_v)

            tiles_row.addWidget(tile, 1)

        outer.addLayout(tiles_row)

        # --- CHARTS ---
        charts_row = QHBoxLayout()
        charts_row.setSpacing(10)

        # Left: bar + line
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3.2))
        fig.patch.set_facecolor(CARD_BG)
        self._plot_bar_chart(ax1, progress)
        self._plot_line_chart(ax2, progress)
        plt.tight_layout()

        left_canvas = FigureCanvas(fig)
        left_canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        left_canvas.setStyleSheet("background: transparent;")
        charts_row.addWidget(left_canvas, 4)

        # Right: donut
        right_wrap = QFrame()
        right_wrap.setStyleSheet(f"QFrame {{ background-color: {CARD_BG}; border-radius: 10px; }}")
        right_v = QVBoxLayout(right_wrap)
        right_v.setContentsMargins(0, 0, 0, 0)

        fig2, ax3 = plt.subplots(figsize=(3.5, 3.2))
        fig2.patch.set_facecolor(CARD_BG)
        self._plot_donut_chart(ax3, completed_lessons, total_lessons)
        plt.tight_layout()

        right_canvas = FigureCanvas(fig2)
        right_canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        right_canvas.setStyleSheet("background: transparent;")
        right_v.addWidget(right_canvas)
        charts_row.addWidget(right_wrap, 3)

        outer.addLayout(charts_row, 1)

    def _plot_bar_chart(self, ax, progress: Dict[int, Dict[str, Any]]) -> None:
        ax.set_facecolor(CARD_BG)
        today = datetime.now().date()
        dates = [today - timedelta(days=i) for i in range(6, -1, -1)]
        date_strs = [d.strftime("%Y-%m-%d") for d in dates]
        date_labels = [d.strftime("%a") for d in dates]

        counts = {d_str: 0 for d_str in date_strs}
        for p in progress.values():
            if p.get("last_attempted"):
                try:
                    p_date = datetime.strptime(p["last_attempted"].split("T")[0], "%Y-%m-%d").date()
                    p_str = p_date.strftime("%Y-%m-%d")
                    if p_str in counts:
                        counts[p_str] += p.get("attempts", 1)
                except Exception:
                    pass

        y_vals = [counts[d_str] for d_str in date_strs]
        ax.bar(date_labels, y_vals, color=ACCENT, width=0.5)
        ax.set_title("Signs Practiced (7 Days)", color=TEXT_MAIN, fontsize=10, fontweight="bold")
        ax.tick_params(colors=TEXT_DIM, labelsize=8)
        ax.spines["bottom"].set_color(BLUE_ACCENT)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color(BLUE_ACCENT)
        ax.grid(axis="y", color=BLUE_ACCENT, linestyle="--", alpha=0.5)

    def _plot_line_chart(self, ax, progress: Dict[int, Dict[str, Any]]) -> None:
        ax.set_facecolor(CARD_BG)
        sessions = []
        for p in progress.values():
            if p.get("last_attempted") and p.get("best_accuracy", 0.0) > 0:
                sessions.append((p["last_attempted"], p["best_accuracy"]))

        sessions.sort(key=lambda x: x[0])
        recent = sessions[-10:]

        y_vals = [s[1] for s in recent]
        x_vals = list(range(1, len(y_vals) + 1))

        if not y_vals:
            y_vals = [0.0]
            x_vals = [1]

        ax.plot(x_vals, y_vals, marker="o", color=RED_ACCENT, linewidth=2)
        ax.set_title("Accuracy Trend (Practice)", color=TEXT_MAIN, fontsize=10, fontweight="bold")
        ax.tick_params(colors=TEXT_DIM, labelsize=8)
        ax.spines["bottom"].set_color(BLUE_ACCENT)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color(BLUE_ACCENT)
        ax.grid(color=BLUE_ACCENT, linestyle="--", alpha=0.5)
        ax.set_ylim(0, 105)

    def _plot_donut_chart(self, ax, completed: int, total: int) -> None:
        ax.set_facecolor(CARD_BG)
        remaining = max(0, total - completed)
        if total == 0:
            remaining = 1

        sizes = [completed, remaining]
        colors = [ACCENT, BLUE_ACCENT]
        labels = ["Learned", "Remaining"]

        wedges, texts, autotexts = ax.pie(
            sizes, labels=labels, colors=colors, autopct="%1.1f%%",
            startangle=90, pctdistance=0.75,
            textprops=dict(color=TEXT_DIM, size=8)
        )
        for autotext in autotexts:
            autotext.set_color(TEXT_MAIN)
            autotext.set_fontsize(8)
            autotext.set_weight("bold")

        centre_circle = plt.Circle((0, 0), 0.55, fc=CARD_BG)
        ax.add_artist(centre_circle)
        ax.set_title("Curriculum Mastery", color=TEXT_MAIN, fontsize=10, fontweight="bold")
        ax.axis("equal")
