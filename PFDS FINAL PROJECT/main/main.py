# Main Application Entry Point and Screen Router for SignBridge
import os
import json
import customtkinter as ctk
from typing import Dict, Any, Optional

from database.db_manager import DatabaseManager
from modules.learning.seed_lessons import seed_database
from modules.recognizer.asl_detector import ASLDetector

# Import Screens
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

# Global style configuration
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class SignBridgeApp(ctk.CTk):
    """The root window for the SignBridge application, serving as the main
    session manager and router between GUI screens.
    """

    def __init__(self) -> None:
        super().__init__()
        self.title("SignBridge - ASL Learning Platform")
        self.geometry("1280x720")
        self.minsize(1280, 720)
        
        # Configure grid layout: sidebar on left, main content on right
        self.grid_columnconfigure(0, weight=0) # Sidebar
        self.grid_columnconfigure(1, weight=1) # Main area
        self.grid_rowconfigure(0, weight=1)

        # File Paths
        self.app_dir = os.path.dirname(os.path.abspath(__file__))
        self.session_path = os.path.join(self.app_dir, "session.json")
        self.settings_path = os.path.join(self.app_dir, "settings.json")
        
        # Initialize Core Engines
        self.db_manager = DatabaseManager()
        seed_database(self.db_manager)
        
        # Instantiate detector once (takes a few seconds if model exists)
        self.asl_detector = ASLDetector(model_dir=os.path.join(self.app_dir, "model"))
        
        # Session and Settings State
        self.current_user_id: Optional[int] = None
        self.settings: Dict[str, Any] = {
            "theme": "Dark Theme",
            "language": "Bilingual (Urdu)",
            "camera_index": 0
        }
        self.load_settings()

        # Screens container and active pointer
        self.screens: Dict[str, ctk.CTkFrame] = {}
        self.active_screen_name: Optional[str] = None
        
        self.setup_layout()
        self.check_persistent_session()

    def setup_layout(self) -> None:
        """Sets up the layout frames for the sidebar and main content area."""
        # 1. SIDEBAR (Navigation panel)
        self.sidebar = ctk.CTkFrame(self, width=200, fg_color="#1a1a2e", corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)
        self.build_sidebar_widgets()

        # 2. MAIN CONTENT AREA
        self.container = ctk.CTkFrame(self, fg_color="#0d0d1a", corner_radius=0)
        self.container.grid(row=0, column=1, sticky="nsew")
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)

        # Instantiate all screens inside the container
        self.screens["login"] = LoginScreen(self.container, self)
        self.screens["register"] = RegisterScreen(self.container, self)
        self.screens["home"] = HomeScreen(self.container, self)
        self.screens["learn"] = LearnScreen(self.container, self)
        self.screens["practice"] = PracticeScreen(self.container, self)
        self.screens["speak"] = SpeakScreen(self.container, self)
        self.screens["stats"] = StatsScreen(self.container, self)
        self.screens["leaderboard"] = LeaderboardScreen(self.container, self)
        self.screens["profile"] = ProfileScreen(self.container, self)
        self.screens["settings"] = SettingsScreen(self.container, self)
        self.screens["quiz"] = QuizScreen(self.container, self)

    def build_sidebar_widgets(self) -> None:
        """Constructs buttons for the sidebar navigation panel."""
        # Logo
        logo = ctk.CTkLabel(
            self.sidebar, text="SignBridge", 
            font=ctk.CTkFont(family="Helvetica", size=22, weight="bold"),
            text_color="#00d4aa"
        )
        logo.pack(pady=(30, 25))

        # Navigation buttons config
        nav_config = [
            ("Home", "🏠 Home", "home"),
            ("Learn", "📚 Learn", "learn"),
            ("Speak", "🗣️ Speak", "speak"),
            ("Stats", "📊 Stats", "stats"),
            ("Leaderboard", "🏆 Leaderboard", "leaderboard"),
            ("Profile", "👤 Profile", "profile"),
            ("Settings", "⚙️ Settings", "settings")
        ]
        
        self.nav_buttons = {}
        for key, label, screen_name in nav_config:
            btn = ctk.CTkButton(
                self.sidebar, text=label, anchor="w",
                fg_color="transparent", text_color="#e0e0e0",
                hover_color="#0f3460", height=40,
                font=ctk.CTkFont(size=14, weight="bold"),
                command=lambda s=screen_name: self.show_screen(s)
            )
            btn.pack(fill="x", padx=15, pady=4)
            self.nav_buttons[screen_name] = btn

        # Separator/Spacer
        spacer = ctk.CTkLabel(self.sidebar, text="")
        spacer.pack(fill="both", expand=True)

        # Logout button
        logout_btn = ctk.CTkButton(
            self.sidebar, text="🚪 Logout", anchor="w",
            fg_color="transparent", text_color="#e94560",
            hover_color="#0f3460", height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.logout_user
        )
        logout_btn.pack(fill="x", padx=15, pady=(5, 25))

    def show_screen(self, screen_name: str, **kwargs) -> None:
        """Transitions the interface to the designated screen frame, managing lifecycles."""
        if self.active_screen_name == screen_name and not kwargs:
            return

        # 1. Clean up old screen lifecycle
        if self.active_screen_name:
            old_screen = self.screens[self.active_screen_name]
            if hasattr(old_screen, "on_leave"):
                old_screen.on_leave()
            old_screen.grid_forget()

        # 2. Highlight active sidebar tab
        self.update_sidebar_highlight(screen_name)

        # 3. Present new screen and trigger lifecycle
        new_screen = self.screens[screen_name]
        new_screen.grid(row=0, column=0, sticky="nsew")
        
        self.active_screen_name = screen_name
        
        if hasattr(new_screen, "on_enter"):
            new_screen.on_enter(**kwargs)
        elif hasattr(new_screen, "refresh"):
            new_screen.refresh()

    def update_sidebar_highlight(self, active_name: str) -> None:
        """Highlights the active navigation button and dims others."""
        for name, btn in self.nav_buttons.items():
            if name == active_name:
                btn.configure(fg_color="#0f3460", text_color="#00d4aa")
            else:
                btn.configure(fg_color="transparent", text_color="#e0e0e0")

    # --- SESSION & SETTINGS PERSISTENCE ---
    def check_persistent_session(self) -> None:
        """Checks for a valid 'Remember me' session file on startup."""
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
        
        # Force login screen
        self.sidebar.grid_forget() # Hide sidebar during auth
        self.show_screen("login")

    def login_user(self, user_id: int, remember_me: bool = False, auto_login: bool = False) -> None:
        """Authenticates session, updates database log times, and routes to Dashboard."""
        self.current_user_id = user_id
        self.db_manager.update_user_last_login(user_id)
        
        # Save session file
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

        # Show navigation sidebar and route home
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.show_screen("home")

    def logout_user(self) -> None:
        """Clears active session, releases camera/TTS assets, and routes to Login."""
        self.current_user_id = None
        if os.path.exists(self.session_path):
            try:
                os.remove(self.session_path)
            except Exception:
                pass
                
        self.sidebar.grid_forget()
        self.show_screen("login")

    def load_settings(self) -> None:
        """Loads app settings from disk."""
        if os.path.exists(self.settings_path):
            try:
                with open(self.settings_path, "r") as f:
                    self.settings.update(json.load(f))
            except Exception:
                pass
        self.apply_theme_setting()

    def save_settings(self) -> None:
        """Saves app settings to disk."""
        try:
            with open(self.settings_path, "w") as f:
                json.dump(self.settings, f)
        except Exception:
            pass
        self.apply_theme_setting()

    def apply_theme_setting(self) -> None:
        """Applies CustomTkinter appearance theme from settings."""
        theme = self.settings.get("theme", "Dark Theme")
        if theme == "System Default":
            ctk.set_appearance_mode("system")
        else:
            ctk.set_appearance_mode("dark")

    def show_toast(self, message: str) -> None:
        """Displays a brief notice banner in the console or status bar."""
        # Simple print fallback for debugging, can be extended to an overlay popup
        print(f"[SignBridge Toast] {message}")

if __name__ == "__main__":
    app = SignBridgeApp()
    app.mainloop()
