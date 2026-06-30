# Registration Screen for SignBridge
import re
import bcrypt
import logging

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QCheckBox, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


DARK_BG = "#0d0d1a"
CARD_BG = "#111126"
ACCENT = "#00d4aa"
RED_ACCENT = "#e94560"
BLUE_ACCENT = "#0f3460"
GREEN_ACCENT = "#008f7a"
TEXT_MAIN = "#e0e0e0"
INPUT_BG = "#0d0d1a"
INPUT_BORDER = "#0f3460"


class RegisterScreen(QWidget):
    """PyQt5 widget providing user registration and account creation."""

    def __init__(self, controller) -> None:
        super().__init__()
        self.controller = controller
        self.db = controller.db_manager
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
        v.setSpacing(6)

        title = QLabel("Join SignBridge")
        title.setFont(QFont("Helvetica", 26, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"color: {TEXT_MAIN};")
        v.addWidget(title)

        subtitle = QLabel("Begin your sign language journey today.")
        subtitle.setFont(QFont("Helvetica", 13))
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet(f"color: {ACCENT};")
        v.addWidget(subtitle)

        v.addSpacing(16)

        entry_style = (
            f"QLineEdit {{ background-color: {INPUT_BG}; color: {TEXT_MAIN}; "
            f"border: 1px solid {INPUT_BORDER}; border-radius: 6px; padding: 0 10px; font-size: 14px; }}"
        )

        self.username_entry = QLineEdit()
        self.username_entry.setPlaceholderText("Username (unique)")
        self.username_entry.setFixedHeight(40)
        self.username_entry.setStyleSheet(entry_style)
        v.addWidget(self.username_entry)

        self.display_entry = QLineEdit()
        self.display_entry.setPlaceholderText("Display Name")
        self.display_entry.setFixedHeight(40)
        self.display_entry.setStyleSheet(entry_style)
        v.addWidget(self.display_entry)

        self.email_entry = QLineEdit()
        self.email_entry.setPlaceholderText("Email Address")
        self.email_entry.setFixedHeight(40)
        self.email_entry.setStyleSheet(entry_style)
        v.addWidget(self.email_entry)

        self.password_entry = QLineEdit()
        self.password_entry.setPlaceholderText("Password")
        self.password_entry.setEchoMode(QLineEdit.Password)
        self.password_entry.setFixedHeight(40)
        self.password_entry.setStyleSheet(entry_style)
        v.addWidget(self.password_entry)

        self.confirm_entry = QLineEdit()
        self.confirm_entry.setPlaceholderText("Confirm Password")
        self.confirm_entry.setEchoMode(QLineEdit.Password)
        self.confirm_entry.setFixedHeight(40)
        self.confirm_entry.setStyleSheet(entry_style)
        v.addWidget(self.confirm_entry)

        self.show_pw_checkbox = QCheckBox("Show password")
        self.show_pw_checkbox.setStyleSheet(
            f"QCheckBox {{ color: {TEXT_MAIN}; font-size: 13px; }}"
            f"QCheckBox::indicator {{ width: 16px; height: 16px; }}"
        )
        self.show_pw_checkbox.stateChanged.connect(self._toggle_password_visibility)
        v.addWidget(self.show_pw_checkbox)

        self.error_label = QLabel("")
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setStyleSheet(f"color: {RED_ACCENT}; font-size: 11px;")
        self.error_label.setWordWrap(True)
        v.addWidget(self.error_label)

        register_btn = QPushButton("Register & Sign In")
        register_btn.setFixedHeight(45)
        register_btn.setFont(QFont("Helvetica", 13, QFont.Bold))
        register_btn.setCursor(Qt.PointingHandCursor)
        register_btn.setStyleSheet(
            f"QPushButton {{ background-color: {GREEN_ACCENT}; color: white; "
            f"border: none; border-radius: 6px; }}"
            f"QPushButton:hover {{ background-color: {BLUE_ACCENT}; }}"
        )
        register_btn.clicked.connect(self._handle_registration)
        v.addWidget(register_btn)

        back_btn = QPushButton("Back to Login")
        back_btn.setFixedHeight(35)
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.setStyleSheet(
            f"QPushButton {{ background-color: transparent; color: {TEXT_MAIN}; "
            f"border: none; border-radius: 6px; }}"
            f"QPushButton:hover {{ background-color: {BLUE_ACCENT}; }}"
        )
        back_btn.clicked.connect(lambda: self.controller.show_screen("login"))
        v.addWidget(back_btn)

    def _toggle_password_visibility(self) -> None:
        if self.show_pw_checkbox.isChecked():
            self.password_entry.setEchoMode(QLineEdit.Normal)
            self.confirm_entry.setEchoMode(QLineEdit.Normal)
        else:
            self.password_entry.setEchoMode(QLineEdit.Password)
            self.confirm_entry.setEchoMode(QLineEdit.Password)

    def _handle_registration(self) -> None:
        username = self.username_entry.text().strip()
        display_name = self.display_entry.text().strip()
        email = self.email_entry.text().strip()
        password = self.password_entry.text()
        confirm = self.confirm_entry.text()

        if not all([username, display_name, email, password, confirm]):
            self.error_label.setText("Please fill in all fields.")
            return

        if len(username) < 3:
            self.error_label.setText("Username must be at least 3 characters.")
            return

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            self.error_label.setText("Please enter a valid email address.")
            return

        if len(password) < 6:
            self.error_label.setText("Password must be at least 6 characters.")
            return

        if password != confirm:
            self.error_label.setText("Passwords do not match.")
            return

        try:
            salt = bcrypt.gensalt()
            pw_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
            pw_hash_str = pw_hash.decode('utf-8')
        except Exception as e:
            self.error_label.setText("Error secure-hashing password.")
            logging.error("Password hashing failed: %s", str(e))
            return

        user_id = self.db.create_user(
            username=username,
            display_name=display_name,
            password_hash=pw_hash_str,
            email=email
        )

        if user_id is None:
            self.error_label.setText("Username already exists.")
            return

        self.error_label.setText("")
        self._clear_form()
        self.controller.login_user(user_id, remember_me=False)

    def _clear_form(self) -> None:
        self.username_entry.clear()
        self.display_entry.clear()
        self.email_entry.clear()
        self.password_entry.clear()
        self.confirm_entry.clear()
        self.show_pw_checkbox.setChecked(False)
        self.password_entry.setEchoMode(QLineEdit.Password)
        self.confirm_entry.setEchoMode(QLineEdit.Password)
        self.error_label.setText("")
