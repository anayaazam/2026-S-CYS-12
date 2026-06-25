# Practice Screen for SignBridge
import os
import cv2
import customtkinter as ctk
from PIL import Image, ImageTk
from typing import Optional, Dict, Any
from database.db_manager import DatabaseManager
from modules.recognizer.asl_detector import ASLDetector
from modules.learning.lesson_manager import LessonManager

class PracticeScreen(ctk.CTkFrame):
    """Enables real-time sign language practice using the webcam and the ASLDetector."""

    def __init__(self, parent: ctk.CTk, controller: any) -> None:
        super().__init__(parent, fg_color="#0d0d1a")
        self.controller = controller
        self.db = controller.db_manager
        self.detector = controller.asl_detector
        self.lesson_manager = LessonManager(self.db)
        
        self.cap: Optional[cv2.VideoCapture] = None
        self.is_running = False
        self.lesson: Optional[Dict[str, Any]] = None
        
        # State tracking for matching the sign
        self.matching_frames = 0
        self.required_frames = 15
        self.best_confidence = 0.0
        self.practice_finished = False

        self.setup_ui()

    def setup_ui(self) -> None:
        """Sets up the layout split between camera feed and instructions."""
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=3) # Camera feed
        self.grid_columnconfigure(1, weight=2) # Progress panel

        # LEFT SIDE: Camera feed container
        self.cam_container = ctk.CTkFrame(self, fg_color="#1a1a2e", corner_radius=10)
        self.cam_container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.cam_container.pack_propagate(False)
        
        # Camera Feed Placeholder Label
        self.feed_label = ctk.CTkLabel(
            self.cam_container, 
            text="Camera Offline\nClick 'Start Camera' to begin.",
            font=ctk.CTkFont(size=16),
            text_color="#a0a0b0"
        )
        self.feed_label.pack(expand=True, fill="both")

        # RIGHT SIDE: Instructions and matching progress
        self.progress_panel = ctk.CTkFrame(self, fg_color="#1a1a2e", corner_radius=10)
        self.progress_panel.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.build_default_instructions()

    def build_default_instructions(self) -> None:
        """Builds default side panel when no lesson is active."""
        for w in self.progress_panel.winfo_children():
            w.destroy()
        self.progress_panel.grid_columnconfigure(0, weight=1)
        
        lbl = ctk.CTkLabel(
            self.progress_panel, 
            text="No sign selected.\nPlease select a lesson to practice from the Course Curriculum.",
            wraplength=250,
            text_color="#a0a0b0"
        )
        lbl.pack(expand=True, padx=20)

    def on_enter(self, lesson_id: Optional[int] = None) -> None:
        """Called by the main router when this screen is activated."""
        if not lesson_id:
            self.build_default_instructions()
            return
            
        self.lesson = self.db.get_lesson_by_id(lesson_id)
        if not self.lesson:
            return

        # Reset states
        self.matching_frames = 0
        self.best_confidence = 0.0
        self.practice_finished = False
        
        # Rebuild progress panel for the selected lesson
        for w in self.progress_panel.winfo_children():
            w.destroy()
            
        title = ctk.CTkLabel(
            self.progress_panel, text=f"Practice: {self.lesson['sign_name']}",
            font=ctk.CTkFont(size=20, weight="bold"), text_color="#e0e0e0"
        )
        title.pack(pady=(25, 10))
        
        prompt_lbl = ctk.CTkLabel(
            self.progress_panel, text=f"Hold the sign for letter '{self.lesson['letter']}' in front of the camera.",
            font=ctk.CTkFont(size=13, slant="italic"), text_color="#00d4aa", wraplength=250
        )
        prompt_lbl.pack(pady=(0, 20))

        # Progress elements
        self.match_progress = ctk.CTkProgressBar(self.progress_panel, fg_color="#0d0d1a", progress_color="#00d4aa", height=12)
        self.match_progress.set(0)
        self.match_progress.pack(fill="x", padx=25, pady=10)
        
        self.status_lbl = ctk.CTkLabel(
            self.progress_panel, text="Analyzing camera feed...",
            font=ctk.CTkFont(size=14), text_color="#a0a0b0"
        )
        self.status_lbl.pack(pady=10)

        # Action Buttons
        self.start_btn = ctk.CTkButton(
            self.progress_panel, text="Start Camera", command=self.toggle_camera,
            fg_color="#0f3460", hover_color="#e94560"
        )
        self.start_btn.pack(fill="x", padx=25, pady=10)

        # Developer simulation button
        sim_btn = ctk.CTkButton(
            self.progress_panel, text="Simulate Success (Dev)", command=self.simulate_success,
            fg_color="transparent", border_width=1, border_color="#e94560", text_color="#e94560"
        )
        sim_btn.pack(fill="x", padx=25, pady=5)
        
        # Start camera automatically
        self.start_camera()

    def on_leave(self) -> None:
        """Stops the camera when navigating away from this screen."""
        self.stop_camera()

    def toggle_camera(self) -> None:
        """Starts or stops the webcam feed."""
        if self.is_running:
            self.stop_camera()
        else:
            self.start_camera()

    def start_camera(self) -> None:
        """Initializes webcam capture and starts the update loop."""
        if self.is_running or not self.lesson:
            return
            
        # Try to open default camera (index 0)
        # In a production app, the camera index can be loaded from settings
        cam_idx = int(self.controller.settings.get("camera_index", 0))
        self.cap = cv2.VideoCapture(cam_idx)
        
        if not self.cap.isOpened():
            self.feed_label.configure(text="Webcam not found.\nPlease ensure your camera is connected.")
            self.cap = None
            return
            
        self.is_running = True
        if hasattr(self, 'start_btn'):
            self.start_btn.configure(text="Stop Camera", fg_color="#e94560")
        self.update_frame()

    def stop_camera(self) -> None:
        """Stops the camera loop and releases resources."""
        self.is_running = False
        if self.cap:
            self.cap.release()
            self.cap = None
        if hasattr(self, 'start_btn'):
            self.start_btn.configure(text="Start Camera", fg_color="#0f3460")
        self.feed_label.configure(text="Camera Offline\nClick 'Start Camera' to begin.")

    def update_frame(self) -> None:
        """Webcam loop: grabs, predicts, and renders frame in CustomTkinter."""
        if not self.is_running or not self.cap or self.practice_finished:
            return

        ret, frame = self.cap.read()
        if not ret:
            self.stop_camera()
            return

        # Flip horizontally for mirroring
        frame = cv2.flip(frame, 1)

        # Run detection
        annotated, pred_label, confidence = self.detector.process_frame(frame)
        
        # Check matching logic
        if pred_label and self.lesson:
            target = self.lesson["letter"].upper()
            if pred_label == target and confidence >= 0.80:
                self.matching_frames += 1
                self.best_confidence = max(self.best_confidence, confidence)
                progress = min(1.0, self.matching_frames / self.required_frames)
                self.match_progress.set(progress)
                self.status_lbl.configure(text=f"Holding sign... ({self.matching_frames}/{self.required_frames})", text_color="#00d4aa")
                
                if self.matching_frames >= self.required_frames:
                    self.finish_practice()
            else:
                # Slowly decay match progress if they lose the sign
                if self.matching_frames > 0:
                    self.matching_frames -= 1
                    self.match_progress.set(self.matching_frames / self.required_frames)

        # Convert to TK image
        rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(rgb)
        
        # Resize to fit container neatly while maintaining aspect ratio
        w, h = img.size
        ratio = min(600/w, 400/h)
        img = img.resize((int(w * ratio), int(h * ratio)), Image.Resampling.LANCZOS)
        
        imgtk = ImageTk.PhotoImage(image=img)
        self.feed_label.configure(image=imgtk, text="")
        self.feed_label.image = imgtk  # Keep a reference

        # Keep running
        self.after(15, self.update_frame)

    def simulate_success(self) -> None:
        """Helper for developers without a webcam to simulate a successful practice run."""
        self.best_confidence = 0.95
        self.finish_practice()

    def finish_practice(self) -> None:
        """Handles completion of the sign: saves progress, awards XP, and displays feedback."""
        self.practice_finished = True
        self.stop_camera()
        
        user_id = self.controller.current_user_id
        lesson_id = self.lesson["id"]
        accuracy = self.best_confidence * 100 if self.best_confidence > 0 else 85.0
        
        # Complete attempt via lesson manager
        completed, xp_earned, badges = self.lesson_manager.complete_lesson_attempt(user_id, lesson_id, accuracy)
        
        # Update progress UI
        self.match_progress.set(1.0)
        self.status_lbl.configure(text=f"Success! Accuracy: {accuracy:.1f}%", text_color="#00d4aa")
        
        feedback_lbl = ctk.CTkLabel(
            self.progress_panel, 
            text=f"🎉 Sign Matched!\n+{xp_earned} XP earned!", 
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#00d4aa"
        )
        feedback_lbl.pack(pady=15)
        
        if badges:
            badge_names = [self.db.get_unlocked_badges(user_id) for b in badges] # Or show badge notifications
            badge_lbl = ctk.CTkLabel(
                self.progress_panel, 
                text=f"Unlocked Badges: {', '.join(badges)}", 
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#ffaa00"
            )
            badge_lbl.pack(pady=5)

        # "Next" navigation button
        next_btn = ctk.CTkButton(
            self.progress_panel, text="Continue to Curriculum", 
            command=lambda: self.controller.show_screen("learn"),
            fg_color="#00d4aa", hover_color="#0f3460", text_color="#0d0d1a", font=ctk.CTkFont(weight="bold")
        )
        next_btn.pack(fill="x", padx=25, pady=15)
