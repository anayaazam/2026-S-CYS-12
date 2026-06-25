# Quiz Screen for SignBridge
import os
import cv2
import customtkinter as ctk
from PIL import Image, ImageTk
from typing import List, Dict, Any, Optional
from modules.quiz.quiz_engine import QuizEngine
from modules.recognizer.asl_detector import ASLDetector

class QuizScreen(ctk.CTkFrame):
    """Interactive quiz session interface supporting FLASHCARD and SIGN_IT questions."""

    def __init__(self, parent: ctk.CTk, controller: any) -> None:
        super().__init__(parent, fg_color="#0d0d1a")
        self.controller = controller
        self.db = controller.db_manager
        self.detector = controller.asl_detector
        self.quiz_engine = QuizEngine(self.db)
        
        self.questions: List[Dict[str, Any]] = []
        self.current_idx = 0
        self.score = 0
        
        # State for SIGN_IT webcam
        self.cap: Optional[cv2.VideoCapture] = None
        self.is_running = False
        self.matching_frames = 0
        self.required_frames = 15
        self.best_confidence = 0.0
        self.question_answered = False

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def refresh(self) -> None:
        """Starts a new quiz session by default when entering without parameters."""
        self.start_new_quiz()

    def start_new_quiz(self, mode: str = "MIXED") -> None:
        """Generates a fresh 10-question quiz and resets scoring states."""
        user_id = self.controller.current_user_id
        self.questions = self.quiz_engine.generate_quiz(user_id, mode)
        self.current_idx = 0
        self.score = 0
        self.question_answered = False
        
        self.show_current_question()

    def show_current_question(self) -> None:
        """Renders the current question based on its type (FLASHCARD or SIGN_IT)."""
        self.stop_camera()
        self.question_answered = False
        
        for w in self.winfo_children():
            w.destroy()

        if self.current_idx >= len(self.questions):
            self.show_score_screen()
            return

        q = self.questions[self.current_idx]
        
        # Header Progress
        hdr = ctk.CTkLabel(
            self, text=f"Question {self.current_idx + 1} of {len(self.questions)}  ·  Score: {self.score}", 
            font=ctk.CTkFont(size=14, weight="bold"), text_color="#00d4aa"
        )
        hdr.pack(pady=(20, 10))

        # Main Question Frame
        q_frame = ctk.CTkFrame(self, fg_color="#1a1a2e", corner_radius=12, width=600, height=450)
        q_frame.pack(pady=10, padx=40, fill="both", expand=True)
        q_frame.pack_propagate(False)

        if q["type"] == "FLASHCARD":
            self.build_flashcard_ui(q_frame, q)
        else:
            self.build_sign_it_ui(q_frame, q)

    def build_flashcard_ui(self, parent: ctk.CTkFrame, q: Dict[str, Any]) -> None:
        """Constructs choice selection layout for FLASHCARD questions."""
        lbl = ctk.CTkLabel(parent, text="Identify the correct sign name:", font=ctk.CTkFont(size=16, weight="bold"), text_color="#e0e0e0")
        lbl.pack(pady=10)

        # Image Container
        img_frame = ctk.CTkFrame(parent, fg_color="#0d0d1a", width=180, height=180, corner_radius=8)
        img_frame.pack(pady=5)
        img_frame.pack_propagate(False)

        img_loaded = False
        if q["image_path"]:
            abs_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), q["image_path"])
            if os.path.exists(abs_path):
                try:
                    pil_img = Image.open(abs_path)
                    ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(160, 160))
                    img_label = ctk.CTkLabel(img_frame, image=ctk_img, text="")
                    img_label.pack(expand=True)
                    img_loaded = True
                except Exception:
                    pass

        if not img_loaded:
            ctk.CTkLabel(img_frame, text=f"[ Sign {q['letter']} ]", font=ctk.CTkFont(size=14, weight="bold"), text_color="#ffaa00").pack(expand=True)

        # Choice buttons grid
        choices_frame = ctk.CTkFrame(parent, fg_color="transparent")
        choices_frame.pack(fill="x", padx=40, pady=10)
        
        # Grid layout for 4 buttons (2x2)
        choices_frame.grid_columnconfigure(0, weight=1)
        choices_frame.grid_columnconfigure(1, weight=1)

        self.choice_btns = []
        for idx, choice in enumerate(q["choices"]):
            r = idx // 2
            c = idx % 2
            
            btn = ctk.CTkButton(
                choices_frame, text=choice, height=42,
                fg_color="#0f3460", hover_color="#e94560",
                command=lambda ch=choice: self.submit_flashcard_answer(ch)
            )
            btn.grid(row=r, column=c, padx=5, pady=5, sticky="ew")
            self.choice_btns.append(btn)

    def submit_flashcard_answer(self, choice: str) -> None:
        """Evaluates choice selection and colors buttons for feedback."""
        if self.question_answered:
            return
        self.question_answered = True

        q = self.questions[self.current_idx]
        correct_ans = q["correct_answer"]
        is_correct = (choice == correct_ans)
        
        # Record outcome in engine
        user_id = self.controller.current_user_id
        self.quiz_engine.record_question_outcome(user_id, q["lesson_id"], is_correct)

        if is_correct:
            self.score += 1

        # Color the buttons
        for btn in self.choice_btns:
            btn_text = btn.cget("text")
            if btn_text == correct_ans:
                btn.configure(fg_color="#00d4aa", text_color="#0d0d1a") # Success Green
            elif btn_text == choice and not is_correct:
                btn.configure(fg_color="#e94560") # Highlight Pink (Incorrect)
            btn.configure(state="disabled")

        # Next button
        next_btn = ctk.CTkButton(self, text="Next Question ➔", command=self.next_question, fg_color="#00d4aa", text_color="#0d0d1a")
        next_btn.pack(pady=10)

    def build_sign_it_ui(self, parent: ctk.CTkFrame, q: Dict[str, Any]) -> None:
        """Constructs webcam alignment layout for SIGN_IT questions."""
        lbl = ctk.CTkLabel(parent, text=f"SIGN IT: Demonstrate letter '{q['letter']}'", font=ctk.CTkFont(size=16, weight="bold"), text_color="#e0e0e0")
        lbl.pack(pady=10)

        # Split: camera on left, controls on right
        split_frame = ctk.CTkFrame(parent, fg_color="transparent")
        split_frame.pack(fill="both", expand=True, padx=15, pady=5)
        split_frame.grid_columnconfigure(0, weight=3)
        split_frame.grid_columnconfigure(1, weight=2)

        # Cam label
        self.cam_lbl = ctk.CTkLabel(split_frame, text="Camera Offline\nClick 'Start Camera'", fg_color="#0d0d1a", corner_radius=6)
        self.cam_lbl.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.cam_lbl.pack_propagate(False)

        # Controls
        ctrl = ctk.CTkFrame(split_frame, fg_color="transparent")
        ctrl.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        self.q_progress = ctk.CTkProgressBar(ctrl, fg_color="#0d0d1a", progress_color="#00d4aa", height=10)
        self.q_progress.set(0)
        self.q_progress.pack(fill="x", pady=15)

        self.q_status = ctk.CTkLabel(ctrl, text="Ready...", font=ctk.CTkFont(size=13), text_color="#a0a0b0")
        self.q_status.pack(pady=5)

        self.cam_btn = ctk.CTkButton(ctrl, text="Start Camera", command=self.toggle_camera, fg_color="#0f3460")
        self.cam_btn.pack(fill="x", pady=5)

        sim_btn = ctk.CTkButton(ctrl, text="Simulate Correct", command=self.simulate_correct_sign, fg_color="transparent", border_width=1, border_color="#e94560", text_color="#e94560")
        sim_btn.pack(fill="x", pady=5)

        # Set up camera states
        self.matching_frames = 0
        self.best_confidence = 0.0
        self.start_camera()

    def toggle_camera(self) -> None:
        if self.is_running:
            self.stop_camera()
        else:
            self.start_camera()

    def start_camera(self) -> None:
        if self.is_running:
            return
        cam_idx = int(self.controller.settings.get("camera_index", 0))
        self.cap = cv2.VideoCapture(cam_idx)
        if not self.cap.isOpened():
            if hasattr(self, 'cam_lbl'):
                self.cam_lbl.configure(text="Webcam not found.")
            self.cap = None
            return
        self.is_running = True
        if hasattr(self, 'cam_btn'):
            self.cam_btn.configure(text="Stop Camera", fg_color="#e94560")
        self.update_camera_loop()

    def stop_camera(self) -> None:
        self.is_running = False
        if self.cap:
            self.cap.release()
            self.cap = None
        if hasattr(self, 'cam_btn'):
            self.cam_btn.configure(text="Start Camera", fg_color="#0f3460")
        if hasattr(self, 'cam_lbl'):
            self.cam_lbl.configure(text="Camera Offline\nClick 'Start Camera'")

    def update_camera_loop(self) -> None:
        if not self.is_running or not self.cap or self.question_answered:
            return

        ret, frame = self.cap.read()
        if not ret:
            self.stop_camera()
            return

        frame = cv2.flip(frame, 1)
        annotated, pred_label, confidence = self.detector.process_frame(frame)
        q = self.questions[self.current_idx]

        if pred_label and pred_label == q["letter"].upper() and confidence >= 0.80:
            self.matching_frames += 1
            self.best_confidence = max(self.best_confidence, confidence)
            progress = min(1.0, self.matching_frames / self.required_frames)
            self.q_progress.set(progress)
            self.q_status.configure(text=f"Matching... ({self.matching_frames}/{self.required_frames})", text_color="#00d4aa")

            if self.matching_frames >= self.required_frames:
                self.submit_sign_it_answer(True)
                return
        else:
            if self.matching_frames > 0:
                self.matching_frames -= 1
                self.q_progress.set(self.matching_frames / self.required_frames)

        # Display frame
        rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(rgb)
        img = img.resize((320, 240), Image.Resampling.LANCZOS)
        imgtk = ImageTk.PhotoImage(image=img)
        self.cam_lbl.configure(image=imgtk, text="")
        self.cam_lbl.image = imgtk

        self.after(15, self.update_camera_loop)

    def simulate_correct_sign(self) -> None:
        self.best_confidence = 0.90
        self.submit_sign_it_answer(True)

    def submit_sign_it_answer(self, is_correct: bool) -> None:
        self.question_answered = True
        self.stop_camera()
        
        q = self.questions[self.current_idx]
        user_id = self.controller.current_user_id
        self.quiz_engine.record_question_outcome(user_id, q["lesson_id"], is_correct)

        if is_correct:
            self.score += 1
            self.q_status.configure(text="✓ Correct! Sign matched.", text_color="#00d4aa")
        else:
            self.q_status.configure(text="❌ Skip/Incorrect", text_color="#e94560")

        self.q_progress.set(1.0)

        # Next button
        next_btn = ctk.CTkButton(self, text="Next Question ➔", command=self.next_question, fg_color="#00d4aa", text_color="#0d0d1a")
        next_btn.pack(pady=10)

    def next_question(self) -> None:
        self.current_idx += 1
        self.show_current_question()

    def show_score_screen(self) -> None:
        """Displays summary score screen and awards quiz session XP/badges."""
        for w in self.winfo_children():
            w.destroy()

        user_id = self.controller.current_user_id
        q = self.questions[0] if self.questions else None
        
        # Complete quiz in engine
        mode = "MIXED"
        xp_earned, bonus, badges = self.quiz_engine.complete_quiz(user_id, self.score, len(self.questions), mode)

        # Re-query user to show fresh XP levels
        user = self.db.get_user_by_id(user_id)

        title = ctk.CTkLabel(
            self, text="Quiz Completed! 🎉", 
            font=ctk.CTkFont(family="Helvetica", size=28, weight="bold"), text_color="#00d4aa"
        )
        title.pack(pady=30)

        score_lbl = ctk.CTkLabel(
            self, text=f"Your Score: {self.score} / {len(self.questions)}", 
            font=ctk.CTkFont(size=20, weight="bold"), text_color="#e0e0e0"
        )
        score_lbl.pack(pady=10)

        xp_lbl = ctk.CTkLabel(
            self, text=f"Base XP: +{self.score * 5} XP\nBonus XP: +{bonus} XP\nTotal Earned: +{xp_earned} XP", 
            font=ctk.CTkFont(size=14), text_color="#a0a0b0", justify="center"
        )
        xp_lbl.pack(pady=15)

        if badges:
            badge_lbl = ctk.CTkLabel(
                self, text=f"🏆 Newly Unlocked Badges: {', '.join(badges)}", 
                font=ctk.CTkFont(size=14, weight="bold"), text_color="#ffaa00"
            )
            badge_lbl.pack(pady=10)

        finish_btn = ctk.CTkButton(
            self, text="Finish & Go Home", 
            command=lambda: self.controller.show_screen("home"),
            height=40, fg_color="#00d4aa", text_color="#0d0d1a", font=ctk.CTkFont(weight="bold")
        )
        finish_btn.pack(pady=30)

    def on_leave(self) -> None:
        self.stop_camera()
