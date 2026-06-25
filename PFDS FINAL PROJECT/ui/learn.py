# Learn Screen for SignBridge
import os
import customtkinter as ctk
from PIL import Image, ImageTk
from typing import List, Dict, Any, Optional

class LearnScreen(ctk.CTkFrame):
    """Provides a browser for learning units and lessons, complete with lesson details."""

    def __init__(self, parent: ctk.CTk, controller: any) -> None:
        super().__init__(parent, fg_color="#0d0d1a")
        self.controller = controller
        self.db = controller.db_manager
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=3) # Lesson browser
        self.grid_columnconfigure(1, weight=2) # Lesson detail pane
        
        self.selected_lesson: Optional[Dict[str, Any]] = None

    def refresh(self) -> None:
        """Reloads lessons and progress when entering the screen."""
        for widget in self.winfo_children():
            widget.destroy()
            
        user_id = self.controller.current_user_id
        progress = self.db.get_user_progress(user_id)
        
        # --- LEFT PANEL: scrollable units and lessons ---
        left_panel = ctk.CTkFrame(self, fg_color="transparent")
        left_panel.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        left_panel.grid_rowconfigure(1, weight=1)
        left_panel.grid_columnconfigure(0, weight=1)
        
        title = ctk.CTkLabel(
            left_panel, text="Course Curriculum", 
            font=ctk.CTkFont(family="Helvetica", size=22, weight="bold"),
            text_color="#e0e0e0"
        )
        title.grid(row=0, column=0, sticky="w", pady=(0, 15))
        
        scroll = ctk.CTkScrollableFrame(left_panel, fg_color="#1a1a2e", corner_radius=10)
        scroll.grid(row=1, column=0, sticky="nsew")
        scroll.grid_columnconfigure(0, weight=1)

        # Draw units
        units = [
            (1, "Unit 1: ASL Alphabet"),
            (2, "Unit 2: Common Words"),
            (3, "Unit 3: Numbers")
        ]
        
        row_idx = 0
        first_lesson = None

        for u_id, u_title in units:
            unit_lbl = ctk.CTkLabel(
                scroll, text=u_title.upper(), 
                font=ctk.CTkFont(size=12, weight="bold"), 
                text_color="#00d4aa"
            )
            unit_lbl.grid(row=row_idx, column=0, sticky="w", padx=15, pady=(15, 5))
            row_idx += 1
            
            unit_lessons = self.db.get_lessons_by_unit(u_id)
            for lesson in unit_lessons:
                if not first_lesson:
                    first_lesson = lesson
                    
                l_id = lesson["id"]
                is_done = l_id in progress and progress[l_id]["completed"]
                
                # Lesson row frame
                row_frame = ctk.CTkFrame(scroll, fg_color="#0d0d1a" if not is_done else "#0f3460", height=45, corner_radius=6)
                row_frame.grid(row=row_idx, column=0, sticky="ew", padx=10, pady=4)
                row_frame.grid_columnconfigure(1, weight=1)
                
                status_char = "✓" if is_done else "•"
                status_color = "#00d4aa" if is_done else "#a0a0b0"
                
                status_lbl = ctk.CTkLabel(
                    row_frame, text=status_char, 
                    font=ctk.CTkFont(size=18, weight="bold"), 
                    text_color=status_color
                )
                status_lbl.grid(row=0, column=0, padx=(15, 10))
                
                name_lbl = ctk.CTkLabel(
                    row_frame, text=f"{lesson['sign_name']} (Sign)", 
                    font=ctk.CTkFont(size=14, weight="bold" if is_done else "normal"),
                    text_color="#e0e0e0"
                )
                name_lbl.grid(row=0, column=1, sticky="w")
                
                view_btn = ctk.CTkButton(
                    row_frame, text="View", width=60, height=26,
                    fg_color="#0f3460" if not is_done else "#e94560",
                    hover_color="#e94560",
                    command=lambda l=lesson: self.display_lesson_details(l)
                )
                view_btn.grid(row=0, column=2, padx=15)
                row_idx += 1

        # --- RIGHT PANEL: lesson detail ---
        self.right_panel = ctk.CTkFrame(self, fg_color="#1a1a2e", corner_radius=10)
        self.right_panel.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        # Display the first lesson by default if nothing selected yet
        if self.selected_lesson:
            # Re-display the currently selected lesson to update completion checkmarks
            current_id = self.selected_lesson["id"]
            updated_lesson = self.db.get_lesson_by_id(current_id)
            self.display_lesson_details(updated_lesson)
        elif first_lesson:
            self.display_lesson_details(first_lesson)

    def display_lesson_details(self, lesson: Dict[str, Any]) -> None:
        """Renders the detailed description and reference image for the selected lesson."""
        self.selected_lesson = lesson
        
        # Clear right panel
        for widget in self.right_panel.winfo_children():
            widget.destroy()

        self.right_panel.grid_columnconfigure(0, weight=1)
        
        # Sign Name Header
        title = ctk.CTkLabel(
            self.right_panel, text=lesson["sign_name"], 
            font=ctk.CTkFont(family="Helvetica", size=24, weight="bold"),
            text_color="#e0e0e0"
        )
        title.pack(pady=(25, 10))
        
        # Subtitle
        sub = ctk.CTkLabel(
            self.right_panel, text=f"Target sign: '{lesson['letter']}' · Unit {lesson['unit_id']}", 
            font=ctk.CTkFont(size=13, slant="italic"),
            text_color="#00d4aa"
        )
        sub.pack(pady=(0, 20))

        # Reference Image Area
        img_container = ctk.CTkFrame(self.right_panel, fg_color="#0d0d1a", width=220, height=220, corner_radius=8)
        img_container.pack(pady=10)
        img_container.pack_propagate(False)
        
        # Attempt to load the sign image, otherwise show text placeholder
        img_loaded = False
        if lesson["image_path"]:
            # Correct absolute path resolver
            abs_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), lesson["image_path"])
            if os.path.exists(abs_path):
                try:
                    pil_img = Image.open(abs_path)
                    ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(200, 200))
                    img_label = ctk.CTkLabel(img_container, image=ctk_img, text="")
                    img_label.pack(expand=True)
                    img_loaded = True
                except Exception:
                    pass
                    
        if not img_loaded:
            placeholder_label = ctk.CTkLabel(
                img_container, 
                text=f"[ Sign {lesson['letter']} ]\n(Image file missing)", 
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="#ffaa00"
            )
            placeholder_label.pack(expand=True)

        # Description Card
        desc_frame = ctk.CTkFrame(self.right_panel, fg_color="transparent")
        desc_frame.pack(fill="x", padx=30, pady=15)
        
        desc_title = ctk.CTkLabel(desc_frame, text="HOW TO SIGN:", font=ctk.CTkFont(size=11, weight="bold"), text_color="#a0a0b0")
        desc_title.pack(anchor="w", pady=(0, 4))
        
        desc_body = ctk.CTkLabel(
            desc_frame, text=lesson["description"], 
            font=ctk.CTkFont(size=14),
            text_color="#e0e0e0",
            wraplength=280,
            justify="left"
        )
        desc_body.pack(anchor="w")

        # Action Button
        practice_btn = ctk.CTkButton(
            self.right_panel, text="Practice This Sign", 
            command=lambda: self.controller.show_screen("practice", lesson_id=lesson["id"]),
            height=40,
            fg_color="#0f3460",
            hover_color="#e94560",
            text_color="#e0e0e0",
            font=ctk.CTkFont(weight="bold")
        )
        practice_btn.pack(pady=20, fill="x", padx=30)
