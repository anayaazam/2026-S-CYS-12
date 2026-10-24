# Settings Screen for SignBridge
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QComboBox, QButtonGroup, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


DARK_BG = "#0d0d1a"
CARD_BG = "#1a1a2e"
ACCENT = "#00d4aa"
RED_ACCENT = "#e94560"
BLUE_ACCENT = "#0f3460"
TEXT_MAIN = "#e0e0e0"
TEXT_DIM = "#a0a0b0"


def _segmented(values: list, parent=None) -> tuple:
    """Returns (QFrame container, list of QPushButtons, QButtonGroup)."""
    frame = QFrame(parent)
    frame.setStyleSheet("background: transparent;")
    h = QHBoxLayout(frame)
    h.setContentsMargins(0, 0, 0, 0)
    h.setSpacing(0)

    group = QButtonGroup(frame)
    group.setExclusive(True)
    buttons = []
    for i, val in enumerate(values):
        btn = QPushButton(val)
        btn.setCheckable(True)
        btn.setFixedHeight(34)
        btn.setCursor(Qt.PointingHandCursor)
        group.addButton(btn, i)
        h.addWidget(btn)
        buttons.append(btn)
    return frame, buttons, group


def _apply_seg_styles(buttons: list, group: QButtonGroup) -> None:
    active = (
        f"QPushButton {{ background-color: {BLUE_ACCENT}; color: white; "
        f"border: none; border-radius: 4px; font-size: 13px; }}"
    )
    inactive = (
        f"QPushButton {{ background-color: {DARK_BG}; color: {TEXT_DIM}; "
        f"border: none; border-radius: 4px; font-size: 13px; }}"
        f"QPushButton:hover {{ background-color: {RED_ACCENT}; color: white; }}"
    )
    for btn in buttons:
        btn.setStyleSheet(active if btn.isChecked() else inactive)


class SettingsScreen(QWidget):
    """Provides configuration settings for theme, language, webcam, and developer tools."""

    def __init__(self, controller) -> None:
        super().__init__()
        self.controller = controller
        self.setStyleSheet(f"background-color: {DARK_BG};")
        self._setup_ui()

    def _setup_ui(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(30, 25, 30, 20)
        outer.setSpacing(10)

        title = QLabel("Application Settings")
        title.setFont(QFont("Helvetica", 22, QFont.Bold))
        title.setStyleSheet(f"color: {TEXT_MAIN};")
        outer.addWidget(title)

        # Settings card
        card = QFrame()
        card.setStyleSheet(f"QFrame {{ background-color: {CARD_BG}; border-radius: 12px; }}")
        card_v = QVBoxLayout(card)
        card_v.setContentsMargins(30, 25, 30, 30)
        card_v.setSpacing(8)

        def section_label(text: str, color: str) -> QLabel:
            lbl = QLabel(text)
            lbl.setFont(QFont("Helvetica", 10, QFont.Bold))
            lbl.setStyleSheet(f"color: {color}; background: transparent;")
            return lbl

        # 1. Theme
        card_v.addWidget(section_label("APPEARANCE THEME", ACCENT))
        card_v.addSpacing(2)

        theme_frame, self._theme_btns, self._theme_group = _segmented(
            ["Light Theme", "Dark Theme", "System Default"]
        )
        self._theme_group.buttonClicked.connect(
            lambda: (_apply_seg_styles(self._theme_btns, self._theme_group),
                     self._on_theme_changed())
        )
        card_v.addWidget(theme_frame)

        card_v.addSpacing(12)

        # 2. Language
        card_v.addWidget(section_label("DEFAULT SPEECH LANGUAGE", RED_ACCENT))
        card_v.addSpacing(2)

        lang_frame, self._lang_btns, self._lang_group = _segmented(
            ["English Only", "Bilingual (Urdu)"]
        )
        self._lang_group.buttonClicked.connect(
            lambda: (_apply_seg_styles(self._lang_btns, self._lang_group),
                     self._on_lang_changed())
        )
        card_v.addWidget(lang_frame)

        card_v.addSpacing(12)

        # 3. Camera
        card_v.addWidget(section_label("WEBCAM INPUT DEVICE", "#ffaa00"))
        card_v.addSpacing(2)

        self.cam_combo = QComboBox()
        self.cam_combo.addItems(["Camera 0 (Default)", "Camera 1", "Camera 2", "Camera 3"])
        self.cam_combo.setFixedHeight(36)
        self.cam_combo.setStyleSheet(
            f"QComboBox {{ background-color: {DARK_BG}; color: {TEXT_MAIN}; "
            f"border: 1px solid {BLUE_ACCENT}; border-radius: 6px; padding: 0 10px; font-size: 13px; }}"
            f"QComboBox::drop-down {{ border: none; }}"
            f"QComboBox QAbstractItemView {{ background-color: {CARD_BG}; color: {TEXT_MAIN}; "
            f"selection-background-color: {BLUE_ACCENT}; border: none; }}"
        )
        self.cam_combo.currentTextChanged.connect(self._on_cam_changed)
        card_v.addWidget(self.cam_combo)

        card_v.addSpacing(12)

        # 4. Dev mode
        card_v.addWidget(section_label("DEVELOPER MODE", RED_ACCENT))
        card_v.addSpacing(2)

        dev_frame, self._dev_btns, self._dev_group = _segmented(["Disabled", "Enabled"])
        self._dev_group.buttonClicked.connect(
            lambda: (_apply_seg_styles(self._dev_btns, self._dev_group),
                     self._on_dev_changed())
        )
        card_v.addWidget(dev_frame)

        card_v.addSpacing(16)

        # Status
        self.status_lbl = QLabel("")
        self.status_lbl.setFont(QFont("Helvetica", 11))
        self.status_lbl.setStyleSheet(f"color: {ACCENT}; font-style: italic; background: transparent;")
        card_v.addWidget(self.status_lbl)

        # Save button
        save_btn = QPushButton("Apply & Save Settings")
        save_btn.setFixedHeight(38)
        save_btn.setFont(QFont("Helvetica", 13, QFont.Bold))
        save_btn.setCursor(Qt.PointingHandCursor)
        save_btn.setStyleSheet(
            f"QPushButton {{ background-color: {BLUE_ACCENT}; color: white; "
            f"border: none; border-radius: 6px; }}"
            f"QPushButton:hover {{ background-color: {RED_ACCENT}; }}"
        )
        save_btn.clicked.connect(self._apply_and_save)
        card_v.addWidget(save_btn)

        card_v.addStretch(1)
        outer.addWidget(card, 1)

    def refresh(self) -> None:
        """Loads and syncs UI with active controller settings."""
        # Theme
        theme = self.controller.settings.get("theme", "Dark Theme")
        theme_values = ["Light Theme", "Dark Theme", "System Default"]
        idx = theme_values.index(theme) if theme in theme_values else 1
        self._theme_btns[idx].setChecked(True)
        _apply_seg_styles(self._theme_btns, self._theme_group)

        # Language
        lang = self.controller.settings.get("language", "Bilingual (Urdu)")
        lang_values = ["English Only", "Bilingual (Urdu)"]
        idx = lang_values.index(lang) if lang in lang_values else 1
        self._lang_btns[idx].setChecked(True)
        _apply_seg_styles(self._lang_btns, self._lang_group)

        # Camera
        cam_idx = self.controller.settings.get("camera_index", 0)
        self.cam_combo.setCurrentText(
            "Camera 0 (Default)" if cam_idx == 0 else f"Camera {cam_idx}"
        )

        # Dev mode
        dev_mode = self.controller.settings.get("dev_mode", "Disabled")
        dev_idx = 1 if dev_mode == "Enabled" else 0
        self._dev_btns[dev_idx].setChecked(True)
        _apply_seg_styles(self._dev_btns, self._dev_group)

        self.status_lbl.setText("")

    def _on_theme_changed(self) -> None:
        self.status_lbl.setText("Theme updated.")

    def _on_lang_changed(self) -> None:
        self.status_lbl.setText("Speech language updated.")

    def _on_cam_changed(self) -> None:
        self.status_lbl.setText("Webcam source updated.")

    def _on_dev_changed(self) -> None:
        self.status_lbl.setText("Developer options updated.")

    def _apply_and_save(self) -> None:
        # Theme
        theme_values = ["Light Theme", "Dark Theme", "System Default"]
        checked_id = self._theme_group.checkedId()
        theme = theme_values[checked_id] if 0 <= checked_id < len(theme_values) else "Dark Theme"

        # Language
        lang_values = ["English Only", "Bilingual (Urdu)"]
        lang_id = self._lang_group.checkedId()
        language = lang_values[lang_id] if 0 <= lang_id < len(lang_values) else "Bilingual (Urdu)"

        # Camera
        camera_str = self.cam_combo.currentText()
        cam_idx = 0
        if "Camera 1" in camera_str:
            cam_idx = 1
        elif "Camera 2" in camera_str:
            cam_idx = 2
        elif "Camera 3" in camera_str:
            cam_idx = 3

        # Dev mode
        dev_id = self._dev_group.checkedId()
        dev_mode = "Enabled" if dev_id == 1 else "Disabled"

        self.controller.settings["theme"] = theme
        self.controller.settings["language"] = language
        self.controller.settings["camera_index"] = cam_idx
        self.controller.settings["dev_mode"] = dev_mode

        self.controller.save_settings()
        self.controller.apply_theme()
        self.status_lbl.setText("✓ Settings applied and saved successfully.")
