# Registration Screen for SignBridge
import re
import bcrypt
import customtkinter as ctk
import logging
from typing import Optional

class RegisterScreen(ctk.CTkFrame):
    """CustomTkinter frame providing user registration and account creation."""

    def __init__(self, parent: ctk.CTk, controller: any) -> None:
        super().__init__(parent, fg_color="#1a1a2e", corner_radius=15)
        self.controller = controller
        self.db = controller.db_manager
        
        self.setup_ui()

    def setup_ui(self) -> None:
        """Configures the registration form layout."""
        # Title
        title_label = ctk.CTkLabel(
            self, 
            text="Join SignBridge", 
            font=ctk.CTkFont(family="Helvetica", size=28, weight="bold"),
            text_color="#e0e0e0"
        )
        title_label.pack(pady=(30, 5), padx=20)

        subtitle_label = ctk.CTkLabel(
            self, 
            text="Begin your sign language journey today.", 
            font=ctk.CTkFont(family="Helvetica", size=13),
            text_color="#00d4aa"
        )
        subtitle_label.pack(pady=(0, 20), padx=20)

        # Form scroll container for smaller screens
        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=40, pady=5)

        # Username
        self.username_entry = ctk.CTkEntry(
            form_frame, placeholder_text="Username (unique)", height=40,
            fg_color="#0d0d1a", border_color="#0f3460", text_color="#e0e0e0"
        )
        self.username_entry.pack(fill="x", pady=6)

        # Display Name
        self.display_entry = ctk.CTkEntry(
            form_frame, placeholder_text="Display Name", height=40,
            fg_color="#0d0d1a", border_color="#0f3460", text_color="#e0e0e0"
        )
        self.display_entry.pack(fill="x", pady=6)

        # Email
        self.email_entry = ctk.CTkEntry(
            form_frame, placeholder_text="Email Address", height=40,
            fg_color="#0d0d1a", border_color="#0f3460", text_color="#e0e0e0"
        )
        self.email_entry.pack(fill="x", pady=6)

        # Password
        self.password_entry = ctk.CTkEntry(
            form_frame, placeholder_text="Password", show="*", height=40,
            fg_color="#0d0d1a", border_color="#0f3460", text_color="#e0e0e0"
        )
        self.password_entry.pack(fill="x", pady=6)

        # Confirm Password
        self.confirm_entry = ctk.CTkEntry(
            form_frame, placeholder_text="Confirm Password", show="*", height=40,
            fg_color="#0d0d1a", border_color="#0f3460", text_color="#e0e0e0"
        )
        self.confirm_entry.pack(fill="x", pady=6)

        # Error Message Label
        self.error_label = ctk.CTkLabel(
            form_frame, text="", text_color="#e94560", font=ctk.CTkFont(size=11)
        )
        self.error_label.pack(pady=3)

        # Buttons
        register_btn = ctk.CTkButton(
            form_frame, text="Register & Sign In", command=self.handle_registration,
            height=45, fg_color="#00d4aa", hover_color="#0f3460", text_color="#0d0d1a",
            font=ctk.CTkFont(weight="bold")
        )
        register_btn.pack(fill="x", pady=10)

        back_btn = ctk.CTkButton(
            form_frame, text="Back to Login", command=lambda: self.controller.show_screen("login"),
            height=35, fg_color="transparent", hover_color="#0f3460", text_color="#e0e0e0"
        )
        back_btn.pack(fill="x", pady=5)

    def handle_registration(self) -> None:
        """Validates the input fields, hashes the password, and creates the account."""
        username = self.username_entry.get().strip()
        display_name = self.display_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        confirm = self.confirm_entry.get()

        # 1. Validation checks
        if not all([username, display_name, email, password, confirm]):
            self.error_label.configure(text="Please fill in all fields.")
            return

        if len(username) < 3:
            self.error_label.configure(text="Username must be at least 3 characters.")
            return

        # Simple email validation
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            self.error_label.configure(text="Please enter a valid email address.")
            return

        if len(password) < 6:
            self.error_label.configure(text="Password must be at least 6 characters.")
            return

        if password != confirm:
            self.error_label.configure(text="Passwords do not match.")
            return

        # 2. Hash password using bcrypt
        try:
            salt = bcrypt.gensalt()
            pw_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
            # Store hash as a string for safety in sqlite text column
            pw_hash_str = pw_hash.decode('utf-8')
        except Exception as e:
            self.error_label.configure(text="Error secure-hashing password.")
            logging.error("Password hashing failed: %s", str(e))
            return

        # 3. Create user in database
        user_id = self.db.create_user(
            username=username,
            display_name=display_name,
            password_hash=pw_hash_str,
            email=email
        )

        if user_id is None:
            self.error_label.configure(text="Username already exists.")
            return

        # Successful registration, log in directly
        self.error_label.configure(text="")
        self.clear_form()
        self.controller.login_user(user_id, remember_me=False)

    def clear_form(self) -> None:
        """Clears all input fields."""
        self.username_entry.delete(0, "end")
        self.display_entry.delete(0, "end")
        self.email_entry.delete(0, "end")
        self.password_entry.delete(0, "end")
        self.confirm_entry.delete(0, "end")
        self.error_label.configure(text="")
