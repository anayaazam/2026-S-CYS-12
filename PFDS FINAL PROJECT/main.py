# Main Application Entry Point and Screen Router for SignBridge
import os
import json
import sys
from typing import Dict, Any, Optional

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QFrame,
    QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QStackedWidget, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor

from database.db_manager import DatabaseManager
from modules.learning.seed_lessons import seed_database
from modules.recognizer.asl_detector import ASLDetector

from auth.login_screen import LoginScreen
from auth.register_screen import RegisterScreen
from ui.home import HomeScreen
from ui.learn import LearnScreen
from ui.practice import PracticeScreen
from ui.speak import SpeakScreen
from ui.stats import StatsScreen
from ui.leaderboard import LeaderboardScreen
from ui.profile import ProfileScreen
from ui.settings import SettingsScreen
from ui.quiz import QuizScreen


DARK_BG = "#0d0d1a"
SIDEBAR_BG = "#1a1a2e"
ACCENT = "#00d4aa"
RED_ACCENT = "#e94560"
BLUE_ACCENT = "#0f3460"
TEXT_MAIN = "#e0e0e0"
TEXT_DIM = "#a0a0b0"
CARD_BG = "#1a1a2e"


class SignBridgeApp(QMainWindow):
    """Root window for SignBridge — main session manager and screen router."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("SignBridge - ASL Learning Platform")
        self.resize(1280, 720)
        self.setMinimumSize(1100, 650)
        self.showMaximized()

        self.app_dir = os.path.dirname(os.path.abspath(__file__))
        self.session_path = os.path.join(self.app_dir, "session.json")
        self.settings_path = os.path.join(self.app_dir, "settings.json")

        self.db_manager = DatabaseManager()
        seed_database(self.db_manager)

        self._asl_detector = None
        self._asl_model_dir = os.path.join(self.app_dir, "model")

        self.current_user_id: Optional[int] = None
        self.settings: Dict[str, Any] = {
            "theme": "Dark Theme",
            "language": "Bilingual (Urdu)",
            "camera_index": 0,
            "dev_mode": "Disabled"
        }
        self.load_settings()

        self.screens: Dict[str, QWidget] = {}
        self.active_screen_name: Optional[str] = None

        self._setup_layout()
        self.apply_theme()
        self._check_persistent_session()

    @property
    def asl_detector(self):
        if self._asl_detector is None:
            self._asl_detector = ASLDetector(model_dir=self._asl_model_dir)
        return self._asl_detector

    def _setup_layout(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)
        self.setStyleSheet(f"background-color: {DARK_BG};")

        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(200)
        self.sidebar.setStyleSheet(f"background-color: {SIDEBAR_BG}; border: none;")
        self._build_sidebar_widgets()
        main_layout.addWidget(self.sidebar)

        # Stacked content area
        self.stack = QStackedWidget()
        self.stack.setStyleSheet(f"background-color: {DARK_BG};")
        main_layout.addWidget(self.stack, 1)

        # Create all screens
        screen_classes = {
            "login": LoginScreen,
            "register": RegisterScreen,
            "home": HomeScreen,
            "learn": LearnScreen,
            "practice": PracticeScreen,
            "speak": SpeakScreen,
            "stats": StatsScreen,
            "leaderboard": LeaderboardScreen,
            "profile": ProfileScreen,
            "settings": SettingsScreen,
            "quiz": QuizScreen,
        }
        for name, cls in screen_classes.items():
            widget = cls(self)
            self.screens[name] = widget
            self.stack.addWidget(widget)

    def _build_sidebar_widgets(self) -> None:
        layout = QVBoxLayout(self.sidebar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        logo = QLabel("SignBridge")
        logo.setAlignment(Qt.AlignCenter)
        logo.setFont(QFont("Helvetica", 20, QFont.Bold))
        logo.setStyleSheet(f"color: {ACCENT}; padding: 30px 0 25px 0;")
        layout.addWidget(logo)

        nav_config = [
            ("Home", "home"),
            ("Learn", "learn"),
            ("Quiz", "quiz"),
            ("Speak", "speak"),
            ("Stats", "stats"),
            ("Leaderboard", "leaderboard"),
            ("Profile", "profile"),
            ("Settings", "settings"),
        ]

        self.nav_buttons: Dict[str, QPushButton] = {}
        for label, screen_name in nav_config:
            btn = QPushButton(label)
            btn.setFixedHeight(40)
            btn.setFont(QFont("Helvetica", 13, QFont.Bold))
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet(self._nav_btn_style(False))
            btn.clicked.connect(lambda checked, s=screen_name: self.show_screen(s))
            btn.setContentsMargins(15, 0, 0, 0)
            layout.addWidget(btn)
            self.nav_buttons[screen_name] = btn

        layout.addStretch(1)

        logout_btn = QPushButton("Logout")
        logout_btn.setFixedHeight(40)
        logout_btn.setFont(QFont("Helvetica", 13, QFont.Bold))
        logout_btn.setCursor(Qt.PointingHandCursor)
        logout_btn.setStyleSheet(
            f"QPushButton {{ background: transparent; color: #e94560; border: none; "
            f"text-align: left; padding-left: 15px; }}"
            f"QPushButton:hover {{ background-color: {BLUE_ACCENT}; }}"
        )
        logout_btn.clicked.connect(self.logout_user)
        layout.addWidget(logout_btn)
        layout.addSpacing(25)

    def _nav_btn_style(self, active: bool) -> str:
        if active:
            return (
                f"QPushButton {{ background-color: {BLUE_ACCENT}; color: {ACCENT}; "
                f"border: none; text-align: left; padding-left: 15px; }}"
                f"QPushButton:hover {{ background-color: {BLUE_ACCENT}; }}"
            )
        return (
            f"QPushButton {{ background: transparent; color: {TEXT_MAIN}; "
            f"border: none; text-align: left; padding-left: 15px; }}"
            f"QPushButton:hover {{ background-color: #0f3460; }}"
        )

    def show_screen(self, screen_name: str, **kwargs) -> None:
        if self.active_screen_name == screen_name and not kwargs:
            return

        if self.active_screen_name:
            old_screen = self.screens[self.active_screen_name]
            if hasattr(old_screen, "on_leave"):
                old_screen.on_leave()

        self._update_sidebar_highlight(screen_name)

        new_screen = self.screens[screen_name]
        self.stack.setCurrentWidget(new_screen)
        self.active_screen_name = screen_name

        if hasattr(new_screen, "on_enter"):
            new_screen.on_enter(**kwargs)
        elif hasattr(new_screen, "refresh"):
            new_screen.refresh()

    def _update_sidebar_highlight(self, active_name: str) -> None:
        for name, btn in self.nav_buttons.items():
            btn.setStyleSheet(self._nav_btn_style(name == active_name))

    def _check_persistent_session(self) -> None:
        if os.path.exists(self.session_path):
            try:
                with open(self.session_path, "r") as f:
                    data = json.load(f)
                    user_id = data.get("user_id")
                    if user_id and self.db_manager.get_user_by_id(user_id):
                        self.login_user(user_id, remember_me=True, auto_login=True)
                        return
            except Exception:
                pass

        self.sidebar.hide()
        self.show_screen("login")

    def login_user(self, user_id: int, remember_me: bool = False, auto_login: bool = False) -> None:
        self.current_user_id = user_id
        self.db_manager.update_user_last_login(user_id)

        if remember_me:
            try:
                with open(self.session_path, "w") as f:
                    json.dump({"user_id": user_id}, f)
            except Exception:
                pass
        elif os.path.exists(self.session_path) and not auto_login:
            try:
                os.remove(self.session_path)
            except Exception:
                pass

        self.sidebar.show()
        self.show_screen("home")

    def logout_user(self) -> None:
        self.current_user_id = None
        if os.path.exists(self.session_path):
            try:
                os.remove(self.session_path)
            except Exception:
                pass

        self.sidebar.hide()
        self.show_screen("login")

    def load_settings(self) -> None:
        if os.path.exists(self.settings_path):
            try:
                with open(self.settings_path, "r") as f:
                    self.settings.update(json.load(f))
            except Exception:
                pass

    def apply_theme(self) -> None:
        """Switch between Light and Dark theme by changing the app palette."""
        theme = self.settings.get("theme", "Dark Theme")
        app = QApplication.instance()
        palette = QPalette()
        if theme == "Light Theme":
            palette.setColor(QPalette.Window,          QColor("#f0f2f5"))
            palette.setColor(QPalette.WindowText,      QColor("#1a1a2e"))
            palette.setColor(QPalette.Base,            QColor("#ffffff"))
            palette.setColor(QPalette.AlternateBase,   QColor("#e8eaf0"))
            palette.setColor(QPalette.Text,            QColor("#1a1a2e"))
            palette.setColor(QPalette.Button,          QColor("#dde1ea"))
            palette.setColor(QPalette.ButtonText,      QColor("#1a1a2e"))
            palette.setColor(QPalette.Highlight,       QColor("#00d4aa"))
            palette.setColor(QPalette.HighlightedText, QColor("#0d0d1a"))
            # Also update structural widget backgrounds directly
            self.centralWidget().setStyleSheet("background-color: #f0f2f5;")
            self.sidebar.setStyleSheet("background-color: #dde1ea; border: none;")
            self.stack.setStyleSheet("background-color: #f0f2f5;")
            for w in self.screens.values():
                w.setStyleSheet("background-color: #f0f2f5;")
            for name, btn in self.nav_buttons.items():
                active = name == self.active_screen_name
                if active:
                    btn.setStyleSheet(
                        "QPushButton { background-color: #c0c8d8; color: #0f3460; "
                        "border: none; text-align: left; padding-left: 15px; }"
                    )
                else:
                    btn.setStyleSheet(
                        "QPushButton { background: transparent; color: #1a1a2e; "
                        "border: none; text-align: left; padding-left: 15px; }"
                        "QPushButton:hover { background-color: #c0c8d8; }"
                    )
        else:
            palette.setColor(QPalette.Window,          QColor(DARK_BG))
            palette.setColor(QPalette.WindowText,      QColor(TEXT_MAIN))
            palette.setColor(QPalette.Base,            QColor(CARD_BG))
            palette.setColor(QPalette.AlternateBase,   QColor(DARK_BG))
            palette.setColor(QPalette.Text,            QColor(TEXT_MAIN))
            palette.setColor(QPalette.Button,          QColor(BLUE_ACCENT))
            palette.setColor(QPalette.ButtonText,      QColor(TEXT_MAIN))
            palette.setColor(QPalette.Highlight,       QColor(ACCENT))
            palette.setColor(QPalette.HighlightedText, QColor(DARK_BG))
            self.centralWidget().setStyleSheet(f"background-color: {DARK_BG};")
            self.sidebar.setStyleSheet(f"background-color: {SIDEBAR_BG}; border: none;")
            self.stack.setStyleSheet(f"background-color: {DARK_BG};")
            for w in self.screens.values():
                w.setStyleSheet(f"background-color: {DARK_BG};")
            for name, btn in self.nav_buttons.items():
                btn.setStyleSheet(self._nav_btn_style(name == self.active_screen_name))
        app.setPalette(palette)

    def save_settings(self) -> None:
        try:
            with open(self.settings_path, "w") as f:
                json.dump(self.settings, f)
        except Exception:
            pass

    def show_toast(self, message: str) -> None:
        print(f"[SignBridge Toast] {message}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SignBridgeApp()
    window.show()
    sys.exit(app.exec_())
