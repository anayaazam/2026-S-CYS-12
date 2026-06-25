# Home Dashboard Screen for SignBridge
import json
import random
import os
from datetime import datetime
import customtkinter as ctk
from typing import Dict, Any, List
from database.db_manager import DatabaseManager
from modules.gamification.xp_engine import get_level_info

class HomeScreen(ctk.CTkFrame):
    """The landing dashboard showcasing user streak, XP level progress,
    Word of the Day, and the Daily Challenge.
    """

    def __init__(self, parent: ctk.CTk, controller: any) -> None:
        super().__init__(parent, fg_color="#0d0d1a")
        self.controller = controller
        self.db = controller.db_manager
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
    def refresh(self) -> None:
        """Refreshes dashboard data whenever this screen becomes active."""
        # Clear existing widgets and rebuild to show fresh progress/streaks
        for widget in self.winfo_children():
            widget.destroy()
            
        user_id = self.controller.current_user_id
        user = self.db.get_user_by_id(user_id)
        if not user:
            return

        # Header Frame
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, columnspan=2, fill="x", padx=30, pady=(25, 10))
        
        welcome_lbl = ctk.CTkLabel(
            header_frame, 
            text=f"Welcome back, {user['display_name']}!", 
            font=ctk.CTkFont(family="Helvetica", size=24, weight="bold"),
            text_color="#e0e0e0"
        )
        welcome_lbl.pack(side="left")
        
        # Streak Badge
        streak_val = user.get("streak", 0)
        streak_lbl = ctk.CTkLabel(
            header_frame, 
            text=f"🔥 {streak_val} Day Streak", 
            font=ctk.CTkFont(family="Helvetica", size=16, weight="bold"),
            text_color="#e94560"
        )
        streak_lbl.pack(side="right")

        # Column 0: XP Progress & Word of the Day
        left_col = ctk.CTkFrame(self, fg_color="transparent")
        left_col.grid(row=1, column=0, sticky="nsew", padx=(30, 15), pady=15)
        left_col.grid_columnconfigure(0, weight=1)
        
        # XP Card
        self.build_xp_card(left_col, user["xp"])
        
        # Word of the Day Card
        self.build_wotd_card(left_col)

        # Column 1: Daily Challenge & Recent Activity
        right_col = ctk.CTkFrame(self, fg_color="transparent")
        right_col.grid(row=1, column=1, sticky="nsew", padx=(15, 30), pady=15)
        right_col.grid_columnconfigure(0, weight=1)
        
        # Daily Challenge Card
        self.build_challenge_card(right_col, user_id)
        
        # Recent Activity Feed
        self.build_activity_card(right_col, user_id)

    def build_xp_card(self, parent: ctk.CTkFrame, xp: int) -> None:
        """Constructs the XP level progress card."""
        lvl_info = get_level_info(xp)
        
        card = ctk.CTkFrame(parent, fg_color="#1a1a2e", corner_radius=12)
        card.pack(fill="x", pady=(0, 15), ipady=10)
        
        lbl = ctk.CTkLabel(card, text="YOUR LEVEL PROGRESS", font=ctk.CTkFont(size=11, weight="bold"), text_color="#00d4aa")
        lbl.pack(anchor="w", padx=20, pady=(15, 5))
        
        lvl_title = ctk.CTkLabel(
            card, 
            text=f"Level {lvl_info['level']}: {lvl_info['tier_name']}", 
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#e0e0e0"
        )
        lvl_title.pack(anchor="w", padx=20, pady=2)
        
        # Progress Bar
        p_bar = ctk.CTkProgressBar(card, fg_color="#0d0d1a", progress_color="#00d4aa", height=10)
        p_bar.set(lvl_info["progress"])
        p_bar.pack(fill="x", padx=20, pady=10)
        
        xp_text = f"{xp} XP Total · {lvl_info['xp_needed']} XP to next level" if lvl_info['xp_needed'] > 0 else f"{xp} XP Total (Max Level)"
        xp_lbl = ctk.CTkLabel(card, text=xp_text, font=ctk.CTkFont(size=12), text_color="#a0a0b0")
        xp_lbl.pack(anchor="w", padx=20, pady=(0, 10))

    def build_wotd_card(self, parent: ctk.CTkFrame) -> None:
        """Picks and displays the 'Word of the Day'."""
        card = ctk.CTkFrame(parent, fg_color="#1a1a2e", corner_radius=12)
        card.pack(fill="x", pady=5, ipady=15)
        
        header = ctk.CTkLabel(card, text="WORD OF THE DAY", font=ctk.CTkFont(size=11, weight="bold"), text_color="#e94560")
        header.pack(anchor="w", padx=20, pady=(15, 5))
        
        lessons = self.db.get_lessons()
        if not lessons:
            no_lbl = ctk.CTkLabel(card, text="No lessons seeded yet.", text_color="#e0e0e0")
            no_lbl.pack(padx=20, pady=10)
            return

        # Seed random based on date string so it changes exactly once per day
        today_str = datetime.now().strftime("%Y-%m-%d")
        state = random.getstate() # Save random state
        random.seed(today_str)
        wotd = random.choice(lessons)
        random.setstate(state) # Restore random state
        
        title = ctk.CTkLabel(
            card, 
            text=f"{wotd['sign_name']} (Letter: {wotd['letter']})", 
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#e0e0e0"
        )
        title.pack(anchor="w", padx=20, pady=5)
        
        desc = ctk.CTkLabel(
            card, 
            text=wotd["description"], 
            font=ctk.CTkFont(size=13),
            text_color="#a0a0b0",
            wraplength=350,
            justify="left"
        )
        desc.pack(anchor="w", padx=20, pady=5)
        
        practice_btn = ctk.CTkButton(
            card, 
            text="Practice Sign", 
            command=lambda: self.controller.show_screen("practice", lesson_id=wotd["id"]),
            fg_color="#0f3460",
            hover_color="#e94560",
            height=30
        )
        practice_btn.pack(anchor="w", padx=20, pady=(10, 5))

    def build_challenge_card(self, parent: ctk.CTkFrame, user_id: int) -> None:
        """Loads or generates today's daily challenge."""
        card = ctk.CTkFrame(parent, fg_color="#1a1a2e", corner_radius=12)
        card.pack(fill="x", pady=(0, 15), ipady=15)
        
        header = ctk.CTkLabel(card, text="DAILY CHALLENGE", font=ctk.CTkFont(size=11, weight="bold"), text_color="#00d4aa")
        header.pack(anchor="w", padx=20, pady=(15, 5))
        
        today_str = datetime.now().strftime("%Y-%m-%d")
        challenge = self.db.get_daily_challenge(user_id, today_str)
        lessons = self.db.get_lessons()
        
        if not lessons:
            return

        if not challenge:
            # Generate 5 random lesson IDs
            sample_size = min(5, len(lessons))
            selected = random.sample(lessons, sample_size)
            ids = [l["id"] for l in selected]
            self.db.save_daily_challenge(user_id, today_str, json.dumps(ids))
            challenge = self.db.get_daily_challenge(user_id, today_str)
            
        try:
            challenge_ids = json.loads(challenge["signs_json"])
        except Exception:
            challenge_ids = []
            
        progress = self.db.get_user_progress(user_id)
        completed_count = 0
        for l_id in challenge_ids:
            if l_id in progress and progress[l_id]["completed"]:
                completed_count += 1
                
        status_text = "5 signs today — Complete!" if challenge["completed"] or completed_count >= 5 else f"5 signs today — {completed_count}/5 completed"
        
        title = ctk.CTkLabel(
            card, 
            text=status_text, 
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#e0e0e0"
        )
        title.pack(anchor="w", padx=20, pady=5)
        
        desc = ctk.CTkLabel(
            card, 
            text="Practice the selected signs today to earn a +50 XP bonus reward.", 
            font=ctk.CTkFont(size=13),
            text_color="#a0a0b0",
            wraplength=350,
            justify="left"
        )
        desc.pack(anchor="w", padx=20, pady=5)

    def build_activity_card(self, parent: ctk.CTkFrame, user_id: int) -> None:
        """Displays a summary card of recent user practice and quiz activity."""
        card = ctk.CTkFrame(parent, fg_color="#1a1a2e", corner_radius=12)
        card.pack(fill="x", pady=5, ipady=15)
        
        header = ctk.CTkLabel(card, text="RECENT ACTIVITY", font=ctk.CTkFont(size=11, weight="bold"), text_color="#a0a0b0")
        header.pack(anchor="w", padx=20, pady=(15, 5))
        
        # Fetch progress and quizzes
        progress = self.db.get_user_progress(user_id)
        
        recent_items = []
        # Sort progress items by last_attempted
        for l_id, p in progress.items():
            if p.get("last_attempted"):
                recent_items.append((p["last_attempted"], f"Practiced sign: {self.db.get_lesson_by_id(l_id)['sign_name']}"))
                
        # Sort and take top 3
        recent_items.sort(reverse=True, key=lambda x: x[0])
        
        if not recent_items:
            no_lbl = ctk.CTkLabel(card, text="No recent activity yet. Start learning!", font=ctk.CTkFont(size=13), text_color="#a0a0b0")
            no_lbl.pack(anchor="w", padx=20, pady=10)
        else:
            for _, text in recent_items[:3]:
                item_lbl = ctk.CTkLabel(card, text=f"✓ {text}", font=ctk.CTkFont(size=13), text_color="#00d4aa")
                item_lbl.pack(anchor="w", padx=20, pady=3)
