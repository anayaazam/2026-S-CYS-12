# Settings Screen for SignBridge
import customtkinter as ctk
from typing import Dict, Any

class SettingsScreen(ctk.CTkFrame):
    """Provides configuration settings for theme, language translation,
    and webcam camera selection.
    """

    def __init__(self, parent: ctk.CTk, controller: any) -> None:
        super().__init__(parent, fg_color="#0d0d1a")
        self.controller = controller
        
        self.setup_ui()

    def setup_ui(self) -> None:
        """Configures the settings panel layout."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Title
        title_lbl = ctk.CTkLabel(
            self, text="Application Settings", 
            font=ctk.CTkFont(family="Helvetica", size=24, weight="bold"),
            text_color="#e0e0e0"
        )
        title_lbl.grid(row=0, column=0, sticky="w", padx=30, pady=(25, 10))

        # Settings Card Container
        settings_container = ctk.CTkFrame(self, fg_color="#1a1a2e", corner_radius=12)
        settings_container.grid(row=1, column=0, sticky="nsew", padx=30, pady=15)
        settings_container.grid_columnconfigure(0, weight=1)

        # 1. Appearance Mode
        mode_lbl = ctk.CTkLabel(
            settings_container, text="APPEARANCE THEME", 
            font=ctk.CTkFont(size=11, weight="bold"), text_color="#00d4aa"
        )
        mode_lbl.pack(anchor="w", padx=30, pady=(25, 5))
        
        self.theme_segmented = ctk.CTkSegmentedButton(
            settings_container, values=["Dark Theme", "System Default"],
            selected_color="#0f3460", selected_hover_color="#e94560",
            command=self.change_theme
        )
        self.theme_segmented.set("Dark Theme")
        self.theme_segmented.pack(anchor="w", padx=30, pady=5)

        # 2. Translation Language
        lang_lbl = ctk.CTkLabel(
            settings_container, text="DEFAULT SPEECH LANGUAGE", 
            font=ctk.CTkFont(size=11, weight="bold"), text_color="#e94560"
        )
        lang_lbl.pack(anchor="w", padx=30, pady=(20, 5))
        
        self.lang_segmented = ctk.CTkSegmentedButton(
            settings_container, values=["English Only", "Bilingual (Urdu)"],
            selected_color="#0f3460", selected_hover_color="#e94560",
            command=self.change_language
        )
        self.lang_segmented.set("Bilingual (Urdu)")
        self.lang_segmented.pack(anchor="w", padx=30, pady=5)

        # 3. Webcam Input Selector
        cam_lbl = ctk.CTkLabel(
            settings_container, text="WEBCAM INPUT DEVICE", 
            font=ctk.CTkFont(size=11, weight="bold"), text_color="#ffaa00"
        )
        cam_lbl.pack(anchor="w", padx=30, pady=(20, 5))
        
        self.cam_dropdown = ctk.CTkComboBox(
            settings_container, values=["Camera 0 (Default)", "Camera 1", "Camera 2", "Camera 3"],
            fg_color="#0d0d1a", border_color="#0f3460", button_color="#0f3460",
            button_hover_color="#e94560", dropdown_fg_color="#1a1a2e",
            command=self.change_camera
        )
        self.cam_dropdown.set("Camera 0 (Default)")
        self.cam_dropdown.pack(anchor="w", padx=30, pady=5)

        # Status text for feedback
        self.status_lbl = ctk.CTkLabel(
            settings_container, text="", 
            font=ctk.CTkFont(size=12, slant="italic"), text_color="#00d4aa"
        )
        self.status_lbl.pack(anchor="w", padx=30, pady=20)

        # Save Button
        save_btn = ctk.CTkButton(
            settings_container, text="Apply & Save Settings", command=self.apply_and_save,
            height=38, fg_color="#0f3460", hover_color="#e94560", text_color="#e0e0e0",
            font=ctk.CTkFont(weight="bold")
        )
        save_btn.pack(anchor="w", padx=30, pady=(10, 30))

    def refresh(self) -> None:
        """Loads and syncs UI inputs with active controller settings."""
        # Theme
        theme = self.controller.settings.get("theme", "Dark Theme")
        self.theme_segmented.set(theme)
        
        # Language
        lang = self.controller.settings.get("language", "Bilingual (Urdu)")
        self.lang_segmented.set(lang)
        
        # Camera
        cam_idx = self.controller.settings.get("camera_index", 0)
        self.cam_dropdown.set(f"Camera {cam_idx}" if cam_idx > 0 else "Camera 0 (Default)")
        self.status_lbl.configure(text="")

    def change_theme(self, value: str) -> None:
        if value == "System Default":
            ctk.set_appearance_mode("system")
        else:
            ctk.set_appearance_mode("dark")
        self.status_lbl.configure(text="Theme updated.")

    def change_language(self, value: str) -> None:
        self.status_lbl.configure(text="Speech language updated.")

    def change_camera(self, value: str) -> None:
        self.status_lbl.configure(text="Webcam source updated.")

    def apply_and_save(self) -> None:
        """Persists settings into the global session and settings file."""
        theme = self.theme_segmented.get()
        language = self.lang_segmented.get()
        camera_str = self.cam_dropdown.get()
        
        # Parse camera index
        cam_idx = 0
        if "Camera 1" in camera_str:
            cam_idx = 1
        elif "Camera 2" in camera_str:
            cam_idx = 2
        elif "Camera 3" in camera_str:
            cam_idx = 3
            
        # Update controller settings dict
        self.controller.settings["theme"] = theme
        self.controller.settings["language"] = language
        self.controller.settings["camera_index"] = cam_idx
        
        self.controller.save_settings()
        self.status_lbl.configure(text="✓ Settings applied and saved successfully.")
