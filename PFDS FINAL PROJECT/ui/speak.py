# Speak (ASL-to-Speech) Screen for SignBridge
import os
import cv2
import customtkinter as ctk
from PIL import Image, ImageTk
from typing import Optional
from modules.recognizer.letter_buffer import LetterBuffer
from modules.tts.translator import UrduTranslator
from modules.tts.tts_engine import TTSEngine
from modules.gamification.badge_engine import increment_urdu_tts_counter

class SpeakScreen(ctk.CTkFrame):
    """Integrates real-time ASL spelling, temporal buffering, translation,
    and Urdu/English TTS into a unified speech builder interface.
    """

    def __init__(self, parent: ctk.CTk, controller: any) -> None:
        super().__init__(parent, fg_color="#0d0d1a")
        self.controller = controller
        self.db = controller.db_manager
        self.detector = controller.asl_detector
        
        self.letter_buffer = LetterBuffer(window_size=15, stability_threshold=10)
        self.translator = UrduTranslator()
        self.tts_engine = TTSEngine()
        
        self.cap: Optional[cv2.VideoCapture] = None
        self.is_running = False
        
        self.setup_ui()

    def setup_ui(self) -> None:
        """Configures the split camera and text builder panels."""
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=3) # Camera feed
        self.grid_columnconfigure(1, weight=2) # Text builder & TTS

        # LEFT SIDE: Camera panel
        self.cam_container = ctk.CTkFrame(self, fg_color="#1a1a2e", corner_radius=10)
        self.cam_container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.cam_container.pack_propagate(False)
        
        self.feed_label = ctk.CTkLabel(
            self.cam_container, text="Camera Offline\nClick 'Start Camera' to spell words.",
            font=ctk.CTkFont(size=16), text_color="#a0a0b0"
        )
        self.feed_label.pack(expand=True, fill="both")

        # RIGHT SIDE: Text builder & Translation & TTS
        right_panel = ctk.CTkScrollableFrame(self, fg_color="#1a1a2e", corner_radius=10)
        right_panel.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        right_panel.grid_columnconfigure(0, weight=1)

        # Sentence Builder Header
        header = ctk.CTkLabel(right_panel, text="SENTENCE BUILDER", font=ctk.CTkFont(size=11, weight="bold"), text_color="#00d4aa")
        header.pack(anchor="w", padx=15, pady=(15, 5))

        # Main Text Box
        self.text_box = ctk.CTkTextbox(
            right_panel, height=80, fg_color="#0d0d1a", border_color="#0f3460",
            border_width=1, text_color="#e0e0e0", font=ctk.CTkFont(family="Helvetica", size=16)
        )
        self.text_box.pack(fill="x", padx=15, pady=5)

        # Buffer Controls
        btn_frame = ctk.CTkFrame(right_panel, fg_color="transparent")
        btn_frame.pack(fill="x", padx=15, pady=5)
        
        space_btn = ctk.CTkButton(btn_frame, text="Space ␣", width=80, height=28, fg_color="#0f3460", command=self.add_space)
        space_btn.pack(side="left", padx=2)
        
        back_btn = ctk.CTkButton(btn_frame, text="Backspace ⌫", width=95, height=28, fg_color="#0f3460", command=self.backspace)
        back_btn.pack(side="left", padx=2)
        
        clear_btn = ctk.CTkButton(btn_frame, text="Clear ❌", width=75, height=28, fg_color="#e94560", hover_color="#0f3460", command=self.clear_buffer)
        clear_btn.pack(side="left", padx=2)

        # Translation Panel
        trans_header = ctk.CTkLabel(right_panel, text="URDU TRANSLATION", font=ctk.CTkFont(size=11, weight="bold"), text_color="#e94560")
        trans_header.pack(anchor="w", padx=15, pady=(15, 2))

        # Urdu-compatible font setup
        self.urdu_font = ctk.CTkFont(family="Noto Nastaliq Urdu", size=18)
        self.urdu_label = ctk.CTkLabel(
            right_panel, text="ہیلو (translation will appear here)", 
            font=self.urdu_font, text_color="#e0e0e0", wraplength=250, justify="right"
        )
        self.urdu_label.pack(fill="x", padx=15, pady=10)

        # Language Toggle & Speak Button
        self.lang_toggle = ctk.CTkSegmentedButton(
            right_panel, values=["English", "Urdu"], 
            selected_color="#0f3460", selected_hover_color="#e94560"
        )
        self.lang_toggle.set("English")
        self.lang_toggle.pack(fill="x", padx=15, pady=10)

        self.speak_btn = ctk.CTkButton(
            right_panel, text="Speak Sentence 🗣️", command=self.trigger_speak,
            height=40, fg_color="#00d4aa", hover_color="#0f3460", text_color="#0d0d1a", font=ctk.CTkFont(weight="bold")
        )
        self.speak_btn.pack(fill="x", padx=15, pady=10)

        # Camera control button
        self.start_btn = ctk.CTkButton(right_panel, text="Start Camera", command=self.toggle_camera, fg_color="#0f3460")
        self.start_btn.pack(fill="x", padx=15, pady=10)

    def on_enter(self) -> None:
        """Fires when entering the screen."""
        self.clear_buffer()
        self.start_camera()

    def on_leave(self) -> None:
        """Fires when leaving the screen."""
        self.stop_camera()
        self.tts_engine.cleanup()

    def toggle_camera(self) -> None:
        """Toggles webcam acquisition."""
        if self.is_running:
            self.stop_camera()
        else:
            self.start_camera()

    def start_camera(self) -> None:
        """Enables camera captures."""
        if self.is_running:
            return
        cam_idx = int(self.controller.settings.get("camera_index", 0))
        self.cap = cv2.VideoCapture(cam_idx)
        if not self.cap.isOpened():
            self.feed_label.configure(text="Webcam not found.\nPlease connect a camera.")
            self.cap = None
            return
        self.is_running = True
        self.start_btn.configure(text="Stop Camera", fg_color="#e94560")
        self.update_frame()

    def stop_camera(self) -> None:
        """Releases camera assets."""
        self.is_running = False
        if self.cap:
            self.cap.release()
            self.cap = None
        self.start_btn.configure(text="Start Camera", fg_color="#0f3460")
        self.feed_label.configure(text="Camera Offline\nClick 'Start Camera' to spell words.")

    def update_frame(self) -> None:
        """Grabs, runs predictions, debounces via temporal smoothing, and appends to builder."""
        if not self.is_running or not self.cap:
            return

        ret, frame = self.cap.read()
        if not ret:
            self.stop_camera()
            return

        frame = cv2.flip(frame, 1)
        annotated, pred_label, confidence = self.detector.process_frame(frame)
        
        # Buffering logic
        if pred_label and confidence >= 0.80:
            stable, is_new = self.letter_buffer.add_prediction(pred_label)
            if is_new and stable:
                # Update text box
                self.sync_textbox()

        # Render frame
        rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(rgb)
        w, h = img.size
        ratio = min(600/w, 400/h)
        img = img.resize((int(w*ratio), int(h*ratio)), Image.Resampling.LANCZOS)
        
        imgtk = ImageTk.PhotoImage(image=img)
        self.feed_label.configure(image=imgtk, text="")
        self.feed_label.image = imgtk

        self.after(15, self.update_frame)

    def sync_textbox(self) -> None:
        """Syncs the text box and translation with the internal letter buffer."""
        text = self.letter_buffer.get_sentence()
        self.text_box.delete("1.0", "end")
        self.text_box.insert("1.0", text)
        
        # Translate
        if text.strip():
            translation = self.translator.translate(text)
            self.urdu_label.configure(text=translation)
        else:
            self.urdu_label.configure(text="")

    def add_space(self) -> None:
        self.letter_buffer.add_space()
        self.sync_textbox()

    def backspace(self) -> None:
        self.letter_buffer.backspace()
        self.sync_textbox()

    def clear_buffer(self) -> None:
        self.letter_buffer.clear()
        self.sync_textbox()

    def trigger_speak(self) -> None:
        """Triggers the TTS engine in English or Urdu."""
        text = self.text_box.get("1.0", "end-1c").strip()
        if not text:
            return

        lang_sel = self.lang_toggle.get()
        user_id = self.controller.current_user_id
        
        if lang_sel == "Urdu":
            # Translate first
            urdu_text = self.translator.translate(text)
            # Speak Urdu
            success, msg = self.tts_engine.speak(urdu_text, lang="ur")
            if success:
                # Increment bilingual counter
                increment_urdu_tts_counter(self.db, user_id)
        else:
            # Speak English
            success, msg = self.tts_engine.speak(text, lang="en")
            
        if not success:
            # Display error message or log
            self.controller.show_toast(f"TTS Error: {msg}")
