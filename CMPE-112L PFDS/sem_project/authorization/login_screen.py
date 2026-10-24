# Login Screen for SignBridge
import logging
import bcrypt
from typing import Optional

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFrame, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


DARK_BG = "#0d0d1a"
CARD_BG = "#111126"
SIDEBAR_BG = "#1a1a2e"
ACCENT = "#00d4aa"
RED_ACCENT = "#e94560"
BLUE_ACCENT = "#0f3460"
TEXT_MAIN = "#e0e0e0"
TEXT_DIM = "#a0a0b0"
INPUT_BG = "#0d0d1a"
INPUT_BORDER = "#0f3460"


def _btn_style(bg: str, hover: str, text: str, border: str = "none", border_color: str = "transparent") -> str:
    border_css = f"border: 1px solid {border_color};" if border != "none" else "border: none;"
    return (
        f"QPushButton {{ background-color: {bg}; color: {text}; {border_css} "
        f"border-radius: 6px; padding: 6px 12px; font-weight: bold; }}"
        f"QPushButton:hover {{ background-color: {hover}; }}"
    )


class LoginScreen(QWidget):
    """PyQt5 widget providing user login interface and credential validation."""

    def __init__(self, controller) -> None:
        super().__init__()
        self.controller = controller
        self.db = controller.db_manager
        self.show_password = False
        self.remember_me = False
        self.setStyleSheet(f"background-color: {DARK_BG};")
        self._setup_ui()

    def _setup_ui(self) -> None:
        outer = QVBoxLayout(self)
        outer.setAlignment(Qt.AlignCenter)

        center = QFrame()
        center.setFixedWidth(420)
        center.setStyleSheet("background: transparent;")
        outer.addWidget(center, alignment=Qt.AlignCenter)

        v = QVBoxLayout(center)
        v.setAlignment(Qt.AlignCenter)
        v.setSpacing(4)

        # Title
        title = QLabel("SignBridge")
        title.setFont(QFont("Helvetica", 28, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"color: {TEXT_MAIN};")
        v.addWidget(title)

        subtitle = QLabel("Bridge the gap, one sign at a time.")
        subtitle.setFont(QFont("Helvetica", 12))
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet(f"color: {ACCENT}; font-style: italic;")
        v.addWidget(subtitle)

        v.addSpacing(24)

        # Card
        card = QFrame()
        card.setStyleSheet(
            f"QFrame {{ background-color: {CARD_BG}; border-radius: 12px; }}"
        )
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(30, 20, 30, 20)
        card_layout.setSpacing(10)
        v.addWidget(card)

        # Username
        self.username_entry = QLineEdit()
        self.username_entry.setPlaceholderText("Username")
        self.username_entry.setFixedHeight(42)
        self.username_entry.setStyleSheet(
            f"QLineEdit {{ background-color: {INPUT_BG}; color: {TEXT_MAIN}; "
            f"border: 1px solid {INPUT_BORDER}; border-radius: 6px; padding: 0 10px; font-size: 14px; }}"
        )
        card_layout.addWidget(self.username_entry)

        # Password
        self.password_entry = QLineEdit()
        self.password_entry.setPlaceholderText("Password")
        self.password_entry.setEchoMode(QLineEdit.Password)
        self.password_entry.setFixedHeight(42)
        self.password_entry.setStyleSheet(
            f"QLineEdit {{ background-color: {INPUT_BG}; color: {TEXT_MAIN}; "
            f"border: 1px solid {INPUT_BORDER}; border-radius: 6px; padding: 0 10px; font-size: 14px; }}"
        )
        card_layout.addWidget(self.password_entry)

        # Toggle row
        toggle_row = QHBoxLayout()
        toggle_row.setSpacing(8)

        TOGGLE_OFF = f"#1a1a35"
        TOGGLE_TEXT = "#b0b0cc"

        self.show_pw_btn = QPushButton("👁 Show Password")
        self.show_pw_btn.setFixedHeight(32)
        self.show_pw_btn.setCursor(Qt.PointingHandCursor)
        self.show_pw_btn.setStyleSheet(
            f"QPushButton {{ background-color: {TOGGLE_OFF}; color: {TOGGLE_TEXT}; "
            f"border: none; border-radius: 8px; font-size: 12px; }}"
            f"QPushButton:hover {{ background-color: #252545; }}"
        )
        self.show_pw_btn.clicked.connect(self._toggle_password_visibility)
        toggle_row.addWidget(self.show_pw_btn)

        self.remember_btn = QPushButton("☐ Remember Me")
        self.remember_btn.setFixedHeight(32)
        self.remember_btn.setCursor(Qt.PointingHandCursor)
        self.remember_btn.setStyleSheet(
            f"QPushButton {{ background-color: {TOGGLE_OFF}; color: {TOGGLE_TEXT}; "
            f"border: none; border-radius: 8px; font-size: 12px; }}"
            f"QPushButton:hover {{ background-color: #252545; }}"
        )
        self.remember_btn.clicked.connect(self._toggle_remember_me)
        toggle_row.addWidget(self.remember_btn)

        card_layout.addLayout(toggle_row)

        # Error label
        self.error_label = QLabel("")
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setStyleSheet(f"color: {RED_ACCENT}; font-size: 12px;")
        card_layout.addWidget(self.error_label)

        # Login button
        login_btn = QPushButton("Login")
        login_btn.setFixedHeight(44)
        login_btn.setFont(QFont("Helvetica", 13, QFont.Bold))
        login_btn.setCursor(Qt.PointingHandCursor)
        login_btn.setStyleSheet(
            f"QPushButton {{ background-color: {BLUE_ACCENT}; color: {TEXT_MAIN}; "
            f"border: none; border-radius: 6px; }}"
            f"QPushButton:hover {{ background-color: {RED_ACCENT}; }}"
        )
        login_btn.clicked.connect(self._handle_login)
        card_layout.addWidget(login_btn)

        # Register button
        register_btn = QPushButton("Create New Account")
        register_btn.setFixedHeight(40)
        register_btn.setCursor(Qt.PointingHandCursor)
        register_btn.setStyleSheet(
            f"QPushButton {{ background-color: transparent; color: {ACCENT}; "
            f"border: 1px solid {ACCENT}; border-radius: 6px; }}"
            f"QPushButton:hover {{ background-color: {BLUE_ACCENT}; }}"
        )
        register_btn.clicked.connect(lambda: self.controller.show_screen("register"))
        card_layout.addWidget(register_btn)

    def _toggle_password_visibility(self) -> None:
        self.show_password = not self.show_password
        if self.show_password:
            self.password_entry.setEchoMode(QLineEdit.Normal)
            self.show_pw_btn.setText("🙈 Hide Password")
        else:
            self.password_entry.setEchoMode(QLineEdit.Password)
            self.show_pw_btn.setText("👁 Show Password")

    def _toggle_remember_me(self) -> None:
        self.remember_me = not self.remember_me
        if self.remember_me:
            self.remember_btn.setText("☑ Remember Me")
            self.remember_btn.setStyleSheet(
                f"QPushButton {{ background-color: {BLUE_ACCENT}; color: {TEXT_MAIN}; "
                f"border: none; border-radius: 8px; font-size: 12px; }}"
                f"QPushButton:hover {{ background-color: #0f3460; }}"
            )
        else:
            self.remember_btn.setText("☐ Remember Me")
            self.remember_btn.setStyleSheet(
                f"QPushButton {{ background-color: #1a1a35; color: #b0b0cc; "
                f"border: none; border-radius: 8px; font-size: 12px; }}"
                f"QPushButton:hover {{ background-color: #252545; }}"
            )

    def _handle_login(self) -> None:
        username = self.username_entry.text().strip()
        password = self.password_entry.text()
        if not username or not password:
            self.error_label.setText("Please fill in all fields.")
            return
        user = self.db.get_user_by_username(username)
        if not user:
            self.error_label.setText("Invalid username or password.")
            return

        stored_hash = user["password_hash"]
        password_bytes = password.encode('utf-8')

        try:
            if isinstance(stored_hash, str):
                stored_hash_bytes = stored_hash.encode('utf-8')
            else:
                stored_hash_bytes = stored_hash

            if bcrypt.checkpw(password_bytes, stored_hash_bytes):
                self.error_label.setText(" ")
                self.username_entry.clear()
                self.password_entry.clear()
                self.show_password = False
                self.password_entry.setEchoMode(QLineEdit.Password)
                self.show_pw_btn.setText("👁 Show Password")
                self.controller.login_user(user["id"], self.remember_me)
            else:
                self.error_label.setText("Invalid username or password.")
        except Exception as e:
            self.error_label.setText("Error authenticating. Try again.")
            logging.error("Login verification error: %s", str(e))
