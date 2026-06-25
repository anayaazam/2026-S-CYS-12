# Profile and Badges Screen for SignBridge
import customtkinter as ctk
from typing import List, Dict, Any
from database.db_manager import DatabaseManager
from modules.gamification.badge_engine import BADGES
from modules.gamification.xp_engine import get_level_info

AVATARS = {
    1: "🦊",
    2: "🐻",
    3: "🦁",
    4: "🐯",
    5: "🐼",
    6: "🐨"
}

class ProfileScreen(ctk.CTkFrame):
    """Displays the user's profile card, stats summary, avatar selector,
    and a grid showcasing unlocked and locked achievements/badges.
    """

    def __init__(self, parent: ctk.CTk, controller: any) -> None:
        super().__init__(parent, fg_color="#0d0d1a")
        self.controller = controller
        self.db = controller.db_manager
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=2) # Profile and stats
        self.grid_columnconfigure(1, weight=3) # Achievements grid

    def refresh(self) -> None:
        """Reloads user details, active avatar, and badges whenever profile loads."""
        for widget in self.winfo_children():
            widget.destroy()
            
        user_id = self.controller.current_user_id
        user = self.db.get_user_by_id(user_id)
        if not user:
            return

        lvl_info = get_level_info(user["xp"])
        unlocked_badges = self.db.get_unlocked_badges(user_id)

        # --- LEFT COLUMN: PROFILE CARD & AVATAR SELECTOR ---
        left_panel = ctk.CTkFrame(self, fg_color="#1a1a2e", corner_radius=12)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        # Current Avatar & Name
        current_avatar_idx = user.get("avatar_id", 1)
        current_avatar = AVATARS.get(current_avatar_idx, "🦊")
        
        avatar_lbl = ctk.CTkLabel(left_panel, text=current_avatar, font=ctk.CTkFont(size=72))
        avatar_lbl.pack(pady=(30, 10))
        
        display_lbl = ctk.CTkLabel(
            left_panel, text=user["display_name"], 
            font=ctk.CTkFont(family="Helvetica", size=22, weight="bold"),
            text_color="#e0e0e0"
        )
        display_lbl.pack()
        
        username_lbl = ctk.CTkLabel(
            left_panel, text=f"@{user['username']}", 
            font=ctk.CTkFont(family="Helvetica", size=14, slant="italic"),
            text_color="#a0a0b0"
        )
        username_lbl.pack(pady=(0, 20))

        # Avatar Selector Frame
        selector_hdr = ctk.CTkLabel(left_panel, text="CHOOSE AVATAR", font=ctk.CTkFont(size=11, weight="bold"), text_color="#00d4aa")
        selector_hdr.pack(anchor="center", pady=(10, 5))
        
        selector_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        selector_frame.pack(pady=5)
        
        for av_id, av_emoji in AVATARS.items():
            av_btn = ctk.CTkButton(
                selector_frame, text=av_emoji, width=36, height=36,
                fg_color="transparent" if av_id != current_avatar_idx else "#0f3460",
                hover_color="#0f3460",
                font=ctk.CTkFont(size=16),
                command=lambda aid=av_id: self.update_avatar(aid)
            )
            av_btn.pack(side="left", padx=3)

        # Stats breakdown inside Left Panel
        stats_box = ctk.CTkFrame(left_panel, fg_color="#0d0d1a", corner_radius=8)
        stats_box.pack(fill="x", padx=25, pady=20, ipady=10)
        
        lvl_lbl = ctk.CTkLabel(stats_box, text=f"Level {lvl_info['level']} · {lvl_info['tier_name']}", font=ctk.CTkFont(size=14, weight="bold"), text_color="#00d4aa")
        lvl_lbl.pack(pady=(10, 5))
        
        xp_lbl = ctk.CTkLabel(stats_box, text=f"Total XP: {user['xp']} XP", font=ctk.CTkFont(size=13), text_color="#e0e0e0")
        xp_lbl.pack(pady=2)
        
        streak_lbl = ctk.CTkLabel(stats_box, text=f"Active Streak: 🔥 {user['streak']} Days", font=ctk.CTkFont(size=13), text_color="#e94560")
        streak_lbl.pack(pady=2)

        # --- RIGHT COLUMN: ACHIEVEMENTS / BADGES GRID ---
        right_panel = ctk.CTkFrame(self, fg_color="transparent")
        right_panel.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        right_panel.grid_rowconfigure(1, weight=1)
        right_panel.grid_columnconfigure(0, weight=1)
        
        title_badges = ctk.CTkLabel(
            right_panel, text="Achievements & Badges", 
            font=ctk.CTkFont(family="Helvetica", size=22, weight="bold"),
            text_color="#e0e0e0"
        )
        title_badges.grid(row=0, column=0, sticky="w", pady=(0, 15))
        
        scroll_grid = ctk.CTkScrollableFrame(right_panel, fg_color="#1a1a2e", corner_radius=12)
        scroll_grid.grid(row=1, column=0, sticky="nsew")
        scroll_grid.grid_columnconfigure(0, weight=1)
        scroll_grid.grid_columnconfigure(1, weight=1)

        # Build badges grid
        col_idx = 0
        row_idx = 0
        
        for badge_id, details in BADGES.items():
            is_unlocked = badge_id in unlocked_badges
            
            # Badge Card Frame
            badge_card = ctk.CTkFrame(scroll_grid, fg_color="#0d0d1a" if is_unlocked else "#151525", corner_radius=10, height=120)
            badge_card.grid(row=row_idx, column=col_idx, padx=8, pady=8, sticky="nsew")
            badge_card.grid_propagate(False)
            
            # Emoji (colored or grayed out if locked)
            emoji_char = details["emoji"] if is_unlocked else "🔒"
            emoji_color = "#e0e0e0" if is_unlocked else "#505060"
            
            emoji_lbl = ctk.CTkLabel(badge_card, text=emoji_char, font=ctk.CTkFont(size=36), text_color=emoji_color)
            emoji_lbl.pack(pady=(12, 2))
            
            name_lbl = ctk.CTkLabel(
                badge_card, text=details["name"], 
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color="#ffaa00" if is_unlocked else "#606070"
            )
            name_lbl.pack(pady=1)
            
            desc_lbl = ctk.CTkLabel(
                badge_card, text=details["description"], 
                font=ctk.CTkFont(size=10),
                text_color="#a0a0b0" if is_unlocked else "#454555",
                wraplength=140,
                justify="center"
            )
            desc_lbl.pack(pady=(1, 10))
            
            # Toggle grid column
            col_idx += 1
            if col_idx > 1:
                col_idx = 0
                row_idx += 1

    def update_avatar(self, avatar_id: int) -> None:
        """Updates the user's avatar ID in the database and refreshes the view."""
        user_id = self.controller.current_user_id
        sql = "UPDATE users SET avatar_id = ? WHERE id = ?"
        with self.db.get_connection() as conn:
            conn.execute(sql, (avatar_id, user_id))
            conn.commit()
            
        self.refresh()
