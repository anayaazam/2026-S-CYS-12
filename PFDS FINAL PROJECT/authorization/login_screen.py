# Login Screen for SignBridge
import os
import bcrypt
import customtkinter as ctk
from typing import Optional

class LoginScreen(ctk.CTkFrame):
    """CustomTkinter frame providing user login interface and credential validation."""

    def __init__(self, parent: ctk.CTk, controller: any) -> None:
        # Use dark panel color (#1a1a2e) as the background for the login card
        super().__init__(parent, fg_color="#1a1a2e", corner_radius=15)
        self.controller = controller
        self.db = controller.db_manager
        
        self.setup_ui()

    def setup_ui(self) -> None:
        """Configures the UI layout and widgets."""
        # Main Title
        title_label = ctk.CTkLabel(
            self, 
            text="SignBridge", 
            font=ctk.CTkFont(family="Helvetica", size=32, weight="bold"),
            text_color="#e0e0e0"
        )
        title_label.pack(pady=(40, 5), padx=20)

        subtitle_label = ctk.CTkLabel(
            self, 
            text="Bridge the gap, one sign at a time.", 
            font=ctk.CTkFont(family="Helvetica", size=14, slant="italic"),
            text_color="#00d4aa"
        )
        subtitle_label.pack(pady=(0, 30), padx=20)

        # Form Frame
        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=40, pady=10)

        # Username
        self.username_entry = ctk.CTkEntry(
            form_frame, 
            placeholder_text="Username",
            height=45,
            fg_color="#0d0d1a",
            border_color="#0f3460",
            text_color="#e0e0e0"
        )
        self.username_entry.pack(fill="x", pady=10)

        # Password
        self.password_entry = ctk.CTkEntry(
            form_frame, 
            placeholder_text="Password",
            show="*",
            height=45,
            fg_color="#0d0d1a",
            border_color="#0f3460",
            text_color="#e0e0e0"
        )
        self.password_entry.pack(fill="x", pady=10)

        # Remember Me
        self.remember_var = ctk.StringVar(value="off")
        self.remember_checkbox = ctk.CTkCheckBox(
            form_frame, 
            text="Remember me",
            variable=self.remember_var,
            onvalue="on",
            offvalue="off",
            text_color="#e0e0e0",
            fg_color="#0f3460",
            hover_color="#e94560",
            border_color="#0f3460"
        )
        self.remember_checkbox.pack(anchor="w", pady=10)

        # Error Message Label
        self.error_label = ctk.CTkLabel(
            form_frame, 
            text="", 
            text_color="#e94560", 
            font=ctk.CTkFont(size=12)
        )
        self.error_label.pack(pady=5)

        # Buttons
        login_btn = ctk.CTkButton(
            form_frame, 
            text="Login", 
            command=self.handle_login,
            height=45,
            fg_color="#0f3460",
            hover_color="#e94560",
            text_color="#e0e0e0",
            font=ctk.CTkFont(weight="bold")
        )
        login_btn.pack(fill="x", pady=(15, 10))

        register_btn = ctk.CTkButton(
            form_frame, 
            text="Create New Account", 
            command=lambda: self.controller.show_screen("register"),
            height=40,
            fg_color="transparent",
            hover_color="#0f3460",
            text_color="#00d4aa",
            border_color="#00d4aa",
            border_width=1
        )
        register_btn.pack(fill="x", pady=10)

    def handle_login(self) -> None:
        """Validates credentials and logs the user in."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not username or not password:
            self.error_label.configure(text="Please fill in all fields.")
            return

        user = self.db.get_user_by_username(username)
        if not user:
            self.error_label.configure(text="Invalid username or password.")
            return

        # Verify password hash
        stored_hash = user["password_hash"]
        # Convert password to bytes
        password_bytes = password.encode('utf-8')
        
        try:
            # Handle string or bytes stored hash
            if isinstance(stored_hash, str):
                stored_hash_bytes = stored_hash.encode('utf-8')
            else:
                stored_hash_bytes = stored_hash

            if bcrypt.checkpw(password_bytes, stored_hash_bytes):
                # Clear error and entries
                self.error_label.configure(text="")
                self.username_entry.delete(0, "end")
                self.password_entry.delete(0, "end")
                
                # Successful login
                remember_me = (self.remember_var.get() == "on")
                self.controller.login_user(user["id"], remember_me)
            else:
                self.error_label.configure(text="Invalid username or password.")
        except Exception as e:
            self.error_label.configure(text="Error authenticating. Try again.")
            logging.error("Login verification error: %s", str(e))
