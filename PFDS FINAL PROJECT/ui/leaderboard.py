# Leaderboard Screen for SignBridge
import customtkinter as ctk
from typing import List, Dict, Any

class LeaderboardScreen(ctk.CTkFrame):
    """Displays a scrollable table of top users ranked by total XP."""

    def __init__(self, parent: ctk.CTk, controller: any) -> None:
        super().__init__(parent, fg_color="#0d0d1a")
        self.controller = controller
        self.db = controller.db_manager
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

    def refresh(self) -> None:
        """Loads and renders the leaderboard table."""
        for widget in self.winfo_children():
            widget.destroy()
            
        current_user_id = self.controller.current_user_id
        
        # Title
        title_lbl = ctk.CTkLabel(
            self, text="Global Leaderboard", 
            font=ctk.CTkFont(family="Helvetica", size=24, weight="bold"),
            text_color="#e0e0e0"
        )
        title_lbl.grid(row=0, column=0, sticky="w", padx=30, pady=(25, 10))

        # Main scroll table container
        table_container = ctk.CTkFrame(self, fg_color="#1a1a2e", corner_radius=12)
        table_container.grid(row=1, column=0, sticky="nsew", padx=30, pady=15)
        table_container.grid_columnconfigure(0, weight=1)
        table_container.grid_rowconfigure(1, weight=1)

        # Header Row
        header_row = ctk.CTkFrame(table_container, fg_color="transparent", height=40)
        header_row.grid(row=0, column=0, sticky="ew", padx=15, pady=(10, 5))
        header_row.grid_columnconfigure(1, weight=1) # Name column expands
        
        headers = [
            ("Rank", 60, "w"),
            ("Signer", 200, "w"),
            ("Streak", 100, "c"),
            ("Total XP", 100, "e")
        ]
        
        # Draw headers
        rank_hdr = ctk.CTkLabel(header_row, text="RANK", font=ctk.CTkFont(size=11, weight="bold"), text_color="#00d4aa", width=60, anchor="w")
        rank_hdr.pack(side="left", padx=10)
        
        name_hdr = ctk.CTkLabel(header_row, text="SIGNER", font=ctk.CTkFont(size=11, weight="bold"), text_color="#00d4aa", anchor="w")
        name_hdr.pack(side="left", fill="x", expand=True, padx=10)
        
        streak_hdr = ctk.CTkLabel(header_row, text="STREAK", font=ctk.CTkFont(size=11, weight="bold"), text_color="#00d4aa", width=100, anchor="center")
        streak_hdr.pack(side="left", padx=10)
        
        xp_hdr = ctk.CTkLabel(header_row, text="TOTAL XP", font=ctk.CTkFont(size=11, weight="bold"), text_color="#00d4aa", width=100, anchor="e")
        xp_hdr.pack(side="left", padx=10)

        # Separator line
        sep = ctk.CTkFrame(table_container, fg_color="#0f3460", height=2)
        sep.grid(row=1, column=0, sticky="ew", padx=15)

        # Scrollable table body
        scroll_body = ctk.CTkScrollableFrame(table_container, fg_color="transparent")
        scroll_body.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        scroll_body.grid_columnconfigure(0, weight=1)
        table_container.grid_rowconfigure(2, weight=1)

        # Fetch top users from DB
        top_users = self.db.get_leaderboard(limit=25)
        
        for idx, user in enumerate(top_users):
            rank = idx + 1
            is_current = (user["id"] == current_user_id)
            
            # Row Frame
            row_bg = "#0f3460" if is_current else "transparent"
            row_frame = ctk.CTkFrame(scroll_body, fg_color=row_bg, height=45, corner_radius=6)
            row_frame.pack(fill="x", pady=2, ipady=4)
            
            # Rank with medal emojis for top 3
            rank_text = f" {rank}"
            if rank == 1:
                rank_text = "🥇 1"
            elif rank == 2:
                rank_text = "🥈 2"
            elif rank == 3:
                rank_text = "🥉 3"
                
            rank_lbl = ctk.CTkLabel(
                row_frame, text=rank_text, 
                font=ctk.CTkFont(size=14, weight="bold" if rank <= 3 else "normal"),
                text_color="#ffaa00" if rank <= 3 else "#e0e0e0",
                width=60, anchor="w"
            )
            rank_lbl.pack(side="left", padx=10)
            
            # User Name with a small avatar icon placeholder
            name_text = user["display_name"]
            if is_current:
                name_text += " (You)"
                
            name_lbl = ctk.CTkLabel(
                row_frame, text=name_text, 
                font=ctk.CTkFont(size=14, weight="bold" if is_current else "normal"),
                text_color="#00d4aa" if is_current else "#e0e0e0",
                anchor="w"
            )
            name_lbl.pack(side="left", fill="x", expand=True, padx=10)
            
            # Streak
            streak_text = f"🔥 {user['streak']}" if user['streak'] > 0 else "-"
            streak_lbl = ctk.CTkLabel(
                row_frame, text=streak_text, 
                font=ctk.CTkFont(size=13),
                text_color="#e94560" if user['streak'] > 0 else "#a0a0b0",
                width=100, anchor="center"
            )
            streak_lbl.pack(side="left", padx=10)
            
            # XP
            xp_lbl = ctk.CTkLabel(
                row_frame, text=f"{user['xp']} XP", 
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="#00d4aa",
                width=100, anchor="e"
            )
            xp_lbl.pack(side="left", padx=10)
