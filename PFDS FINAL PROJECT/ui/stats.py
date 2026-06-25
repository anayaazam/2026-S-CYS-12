# Stats Screen for SignBridge
import customtkinter as ctk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from typing import Dict, Any, List

class StatsScreen(ctk.CTkFrame):
    """Embeds Matplotlib charts inside CustomTkinter to show user progress analytics."""

    def __init__(self, parent: ctk.CTk, controller: any) -> None:
        super().__init__(parent, fg_color="#0d0d1a")
        self.controller = controller
        self.db = controller.db_manager
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=3)
        self.grid_columnconfigure(0, weight=1)

    def refresh(self) -> None:
        """Refreshes summary statistics and rebuilds Matplotlib charts."""
        for widget in self.winfo_children():
            widget.destroy()
            
        user_id = self.controller.current_user_id
        user = self.db.get_user_by_id(user_id)
        if not user:
            return

        # Fetch progress & quiz stats
        progress = self.db.get_user_progress(user_id)
        quiz_stats = self.db.get_quiz_stats(user_id)
        lessons = self.db.get_lessons()
        
        total_lessons = len(lessons)
        completed_lessons = sum(1 for p in progress.values() if p.get("completed"))
        
        best_practice_acc = max([p.get("best_accuracy", 0.0) for p in progress.values()] or [0.0])
        best_overall_acc = max(best_practice_acc, quiz_stats.get("best_quiz_accuracy", 0.0) * 100)

        # --- PANEL 1: SUMMARY TILES ---
        tiles_frame = ctk.CTkFrame(self, fg_color="transparent")
        tiles_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(15, 10))
        tiles_frame.grid_rowconfigure(0, weight=1)
        
        stats_list = [
            ("Total XP", f"{user['xp']}", "#00d4aa"),
            ("Streak", f"🔥 {user['streak']}", "#e94560"),
            ("Signs Learned", f"{completed_lessons}/{total_lessons}", "#0f3460"),
            ("Quizzes Taken", f"{quiz_stats['quizzes_taken']}", "#ffaa00"),
            ("Best Accuracy", f"{best_overall_acc:.1f}%", "#00d4aa")
        ]
        
        for i, (title, val, color) in enumerate(stats_list):
            tiles_frame.grid_columnconfigure(i, weight=1)
            tile = ctk.CTkFrame(tiles_frame, fg_color="#1a1a2e", corner_radius=10, height=85)
            tile.grid(row=0, column=i, padx=5, sticky="nsew")
            tile.grid_propagate(False)
            
            lbl_title = ctk.CTkLabel(tile, text=title.upper(), font=ctk.CTkFont(size=10, weight="bold"), text_color="#a0a0b0")
            lbl_title.pack(pady=(12, 2))
            
            lbl_val = ctk.CTkLabel(tile, text=val, font=ctk.CTkFont(size=20, weight="bold"), text_color=color)
            lbl_val.pack(pady=(2, 10))

        # --- PANEL 2: CHARTS CONTAINER ---
        charts_frame = ctk.CTkFrame(self, fg_color="transparent")
        charts_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        charts_frame.grid_rowconfigure(0, weight=1)
        charts_frame.grid_columnconfigure(0, weight=4) # Left side chart (Bar + Line)
        charts_frame.grid_columnconfigure(1, weight=3) # Right side chart (Donut)

        # Left Column for Bar/Line
        left_charts = ctk.CTkFrame(charts_frame, fg_color="transparent")
        left_charts.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        left_charts.grid_columnconfigure(0, weight=1)
        left_charts.grid_rowconfigure(0, weight=1)

        # Build combined Figure
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3.2))
        fig.patch.set_facecolor("#1a1a2e")
        
        # 1. Bar Chart: Signs practiced per day (last 7 days)
        self.plot_bar_chart(ax1, progress)
        
        # 2. Line Chart: Accuracy trend (last 10 practice sessions)
        self.plot_line_chart(ax2, progress)
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=left_charts)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        # Right Column for Donut
        right_chart = ctk.CTkFrame(charts_frame, fg_color="#1a1a2e", corner_radius=10)
        right_chart.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        right_chart.grid_columnconfigure(0, weight=1)
        right_chart.grid_rowconfigure(0, weight=1)

        fig2, ax3 = plt.subplots(figsize=(3.5, 3.2))
        fig2.patch.set_facecolor("#1a1a2e")
        
        # 3. Donut Chart: Completion
        self.plot_donut_chart(ax3, completed_lessons, total_lessons)
        
        plt.tight_layout()
        
        canvas2 = FigureCanvasTkAgg(fig2, master=right_chart)
        canvas2.draw()
        canvas2.get_tk_widget().grid(row=0, column=0, sticky="nsew")

    def plot_bar_chart(self, ax: plt.Axes, progress: Dict[int, Dict[str, Any]]) -> None:
        """Plots bar chart of practice attempts over the last 7 days."""
        ax.set_facecolor("#1a1a2e")
        
        # Calculate dates
        today = datetime.now().date()
        dates = [today - timedelta(days=i) for i in range(6, -1, -1)]
        date_strs = [d.strftime("%Y-%m-%d") for d in dates]
        date_labels = [d.strftime("%a") for d in dates]
        
        # Count attempts per date
        counts = {d_str: 0 for d_str in date_strs}
        for p in progress.values():
            if p.get("last_attempted"):
                try:
                    p_date = datetime.strptime(p["last_attempted"].split("T")[0], "%Y-%m-%d").date()
                    p_str = p_date.strftime("%Y-%m-%d")
                    if p_str in counts:
                        counts[p_str] += p.get("attempts", 1)
                except Exception:
                    pass
                    
        y_vals = [counts[d_str] for d_str in date_strs]
        
        ax.bar(date_labels, y_vals, color="#00d4aa", width=0.5)
        ax.set_title("Signs Practiced (7 Days)", color="#e0e0e0", fontsize=10, fontweight="bold")
        ax.tick_params(colors="#a0a0b0", labelsize=8)
        ax.spines["bottom"].set_color("#0f3460")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color("#0f3460")
        ax.grid(axis="y", color="#0f3460", linestyle="--", alpha=0.5)

    def plot_line_chart(self, ax: plt.Axes, progress: Dict[int, Dict[str, Any]]) -> None:
        """Plots a line chart of the user's accuracy trend across recent practice sessions."""
        ax.set_facecolor("#1a1a2e")
        
        # Sort progress sessions by last attempted
        sessions = []
        for p in progress.values():
            if p.get("last_attempted") and p.get("best_accuracy", 0.0) > 0:
                sessions.append((p["last_attempted"], p["best_accuracy"]))
                
        sessions.sort(key=lambda x: x[0])
        recent_sessions = sessions[-10:] # Last 10
        
        y_vals = [s[1] for s in recent_sessions]
        x_vals = list(range(1, len(y_vals) + 1))
        
        # If no data, show a flat line
        if not y_vals:
            y_vals = [0.0]
            x_vals = [1]
            
        ax.plot(x_vals, y_vals, marker="o", color="#e94560", linewidth=2)
        ax.set_title("Accuracy Trend (Practice)", color="#e0e0e0", fontsize=10, fontweight="bold")
        ax.tick_params(colors="#a0a0b0", labelsize=8)
        ax.spines["bottom"].set_color("#0f3460")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color("#0f3460")
        ax.grid(color="#0f3460", linestyle="--", alpha=0.5)
        ax.set_ylim(0, 105)

    def plot_donut_chart(self, ax: plt.Axes, completed: int, total: int) -> None:
        """Plots a donut chart representing curriculum completion percentage."""
        ax.set_facecolor("#1a1a2e")
        
        remaining = max(0, total - completed)
        if total == 0:
            remaining = 1
            
        labels = ["Learned", "Remaining"]
        sizes = [completed, remaining]
        colors = ["#00d4aa", "#0f3460"]
        
        # Plot pie
        wedges, texts, autotexts = ax.pie(
            sizes, labels=labels, colors=colors, autopct="%1.1f%%", 
            startangle=90, pctdistance=0.75,
            textprops=dict(color="#a0a0b0", size=8)
        )
        
        # Style percentages inside donut
        for autotext in autotexts:
            autotext.set_color("#e0e0e0")
            autotext.set_fontsize(8)
            autotext.set_weight("bold")
            
        # Draw center circle to form donut
        centre_circle = plt.Circle((0, 0), 0.55, fc="#1a1a2e")
        ax.add_artist(centre_circle)
        
        ax.set_title("Curriculum Mastery", color="#e0e0e0", fontsize=10, fontweight="bold")
        ax.axis("equal")
