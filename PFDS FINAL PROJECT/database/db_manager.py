import os
import sqlite3
import json
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "signbridge.db")
SCHEMA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "schema.sql")

class DatabaseManager:
    """Manages SQLite database connections and executes CRUD operations for SignBridge."""

    def __init__(self, db_path: str = DB_PATH) -> None:
        self.db_path = db_path
        self.init_db()

    def get_connection(self) -> sqlite3.Connection:
        """Returns a connection to the SQLite database with row factory enabled."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def init_db(self) -> None:
        """Initializes the database schema if the tables do not already exist."""
        if not os.path.exists(SCHEMA_PATH):
            raise FileNotFoundError(f"Schema file not found at {SCHEMA_PATH}")
        
        with self.get_connection() as conn:
            with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
                conn.executescript(f.read())
            conn.commit()

    # --- USER CRUD ---
    def create_user(self, username: str, display_name: str, password_hash: str, email: str) -> Optional[int]:
        """Creates a new user and returns their ID, or None if the username exists."""
        sql = """
        INSERT INTO users (username, display_name, password_hash, email, date_created, last_login)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        now_str = datetime.now().isoformat()
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(sql, (username, display_name, password_hash, email, now_str, now_str))
                conn.commit()
                return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None

    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Retrieves user data by user ID."""
        sql = "SELECT * FROM users WHERE id = ?"
        with self.get_connection() as conn:
            row = conn.execute(sql, (user_id,)).fetchone()
            return dict(row) if row else None

    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Retrieves user data by username."""
        sql = "SELECT * FROM users WHERE username = ?"
        with self.get_connection() as conn:
            row = conn.execute(sql, (username,)).fetchone()
            return dict(row) if row else None

    def update_user_xp(self, user_id: int, xp_to_add: int) -> int:
        """Adds XP to the user's total and returns the new total."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            row = cursor.execute("SELECT xp FROM users WHERE id = ?", (user_id,)).fetchone()
            current_xp = row["xp"] if row else 0
            new_xp = current_xp + xp_to_add
            cursor.execute("UPDATE users SET xp = ? WHERE id = ?", (new_xp, user_id))
            conn.commit()
            return new_xp

    def update_user_streak(self, user_id: int, streak: int, last_practice_date: Optional[str]) -> None:
        """Updates the user's practice streak and the last practice date."""
        sql = "UPDATE users SET streak = ?, last_practice_date = ? WHERE id = ?"
        with self.get_connection() as conn:
            conn.execute(sql, (streak, last_practice_date, user_id))
            conn.commit()

    def update_user_last_login(self, user_id: int) -> None:
        """Updates the user's last login timestamp."""
        now_str = datetime.now().isoformat()
        sql = "UPDATE users SET last_login = ? WHERE id = ?"
        with self.get_connection() as conn:
            conn.execute(sql, (now_str, user_id))
            conn.commit()

    def update_total_signs_learned(self, user_id: int) -> int:
        """Updates and returns the count of unique signs learned (completed lessons)."""
        sql_count = "SELECT COUNT(DISTINCT lesson_id) as cnt FROM user_progress WHERE user_id = ? AND completed = 1"
        sql_update = "UPDATE users SET total_signs_learned = ? WHERE id = ?"
        with self.get_connection() as conn:
            cursor = conn.cursor()
            row = cursor.execute(sql_count, (user_id,)).fetchone()
            count = row["cnt"] if row else 0
            cursor.execute(sql_update, (count, user_id))
            conn.commit()
            return count

    def get_leaderboard(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Returns the top users sorted by XP."""
        sql = "SELECT id, username, display_name, xp, streak, avatar_id FROM users ORDER BY xp DESC LIMIT ?"
        with self.get_connection() as conn:
            rows = conn.execute(sql, (limit,)).fetchall()
            return [dict(r) for r in rows]

    # --- LESSONS CRUD ---
    def add_lesson(self, unit_id: int, sign_name: str, letter: str, description: str, image_path: str, difficulty: int, xp_reward: int) -> int:
        """Adds a lesson to the catalog."""
        sql = """
        INSERT INTO lessons (unit_id, sign_name, letter, description, image_path, difficulty, xp_reward)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (unit_id, sign_name, letter, description, image_path, difficulty, xp_reward))
            conn.commit()
            return cursor.lastrowid

    def get_lessons(self) -> List[Dict[str, Any]]:
        """Retrieves all lessons."""
        sql = "SELECT * FROM lessons ORDER BY unit_id, id"
        with self.get_connection() as conn:
            rows = conn.execute(sql).fetchall()
            return [dict(r) for r in rows]

    def get_lessons_by_unit(self, unit_id: int) -> List[Dict[str, Any]]:
        """Retrieves all lessons in a unit."""
        sql = "SELECT * FROM lessons WHERE unit_id = ? ORDER BY id"
        with self.get_connection() as conn:
            rows = conn.execute(sql, (unit_id,)).fetchall()
            return [dict(r) for r in rows]

    def get_lesson_by_id(self, lesson_id: int) -> Optional[Dict[str, Any]]:
        """Retrieves a single lesson by ID."""
        sql = "SELECT * FROM lessons WHERE id = ?"
        with self.get_connection() as conn:
            row = conn.execute(sql, (lesson_id,)).fetchone()
            return dict(row) if row else None

    # --- PROGRESS CRUD ---
    def save_progress(self, user_id: int, lesson_id: int, completed: bool, accuracy: float) -> Tuple[bool, float]:
        """Saves user progress. Returns (newly_completed, best_accuracy)."""
        now_str = datetime.now().isoformat()
        select_sql = "SELECT completed, best_accuracy, attempts FROM user_progress WHERE user_id = ? AND lesson_id = ?"
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            row = cursor.execute(select_sql, (user_id, lesson_id)).fetchone()
            
            if row:
                prev_completed = bool(row["completed"])
                prev_accuracy = row["best_accuracy"]
                attempts = row["attempts"] + 1
                
                new_completed = prev_completed or completed
                new_accuracy = max(prev_accuracy, accuracy)
                
                update_sql = """
                UPDATE user_progress 
                SET completed = ?, best_accuracy = ?, attempts = ?, last_attempted = ?
                WHERE user_id = ? AND lesson_id = ?
                """
                cursor.execute(update_sql, (new_completed, new_accuracy, attempts, now_str, user_id, lesson_id))
                newly_done = new_completed and not prev_completed
                res_accuracy = new_accuracy
            else:
                insert_sql = """
                INSERT INTO user_progress (user_id, lesson_id, completed, best_accuracy, attempts, last_attempted)
                VALUES (?, ?, ?, ?, 1, ?)
                """
                cursor.execute(insert_sql, (user_id, lesson_id, completed, accuracy, now_str))
                newly_done = completed
                res_accuracy = accuracy
            
            conn.commit()
            
        self.update_total_signs_learned(user_id)
        return newly_done, res_accuracy

    def get_user_progress(self, user_id: int) -> Dict[int, Dict[str, Any]]:
        """Returns map of lesson_id -> progress details for the user."""
        sql = "SELECT lesson_id, completed, best_accuracy, attempts, last_attempted FROM user_progress WHERE user_id = ?"
        with self.get_connection() as conn:
            rows = conn.execute(sql, (user_id,)).fetchall()
            return {r["lesson_id"]: dict(r) for r in rows}

    # --- QUIZ RESULTS CRUD ---
    def save_quiz_result(self, user_id: int, score: int, total_questions: int, mode: str, xp_earned: int) -> int:
        """Saves a quiz result and returns the record ID."""
        sql = """
        INSERT INTO quiz_results (user_id, quiz_date, score, total_questions, mode, xp_earned)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        now_str = datetime.now().isoformat()
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (user_id, now_str, score, total_questions, mode, xp_earned))
            conn.commit()
            return cursor.lastrowid

    def get_quiz_stats(self, user_id: int) -> Dict[str, Any]:
        """Returns summary of quizzes taken, best quiz accuracy, and total quiz XP."""
        sql = """
        SELECT COUNT(*) as taken, 
               MAX(CAST(score AS REAL) / total_questions) as best_acc,
               SUM(xp_earned) as total_xp
        FROM quiz_results WHERE user_id = ?
        """
        with self.get_connection() as conn:
            row = conn.execute(sql, (user_id,)).fetchone()
            return {
                "quizzes_taken": row["taken"] if row else 0,
                "best_quiz_accuracy": row["best_acc"] if row and row["best_acc"] is not None else 0.0,
                "quiz_xp": row["total_xp"] if row and row["total_xp"] is not None else 0
            }

    # --- ACHIEVEMENTS CRUD ---
    def award_badge(self, user_id: int, badge_id: str) -> bool:
        """Awards a badge to the user. Returns True if successfully unlocked, False if already unlocked."""
        sql = "INSERT INTO achievements (user_id, badge_id, date_earned) VALUES (?, ?, ?)"
        now_str = datetime.now().isoformat()
        try:
            with self.get_connection() as conn:
                conn.execute(sql, (user_id, badge_id, now_str))
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False

    def get_unlocked_badges(self, user_id: int) -> List[str]:
        """Returns the list of badge IDs unlocked by the user."""
        sql = "SELECT badge_id FROM achievements WHERE user_id = ?"
        with self.get_connection() as conn:
            rows = conn.execute(sql, (user_id,)).fetchall()
            return [r["badge_id"] for r in rows]

    # --- WEAK SIGNS CRUD ---
    def add_weak_sign(self, user_id: int, lesson_id: int) -> None:
        """Adds a weak sign or increments its fail count."""
        now_str = datetime.now().isoformat()
        select_sql = "SELECT fail_count FROM weak_signs WHERE user_id = ? AND lesson_id = ?"
        with self.get_connection() as conn:
            cursor = conn.cursor()
            row = cursor.execute(select_sql, (user_id, lesson_id)).fetchone()
            if row:
                count = row["fail_count"] + 1
                cursor.execute("UPDATE weak_signs SET fail_count = ?, last_failed = ? WHERE user_id = ? AND lesson_id = ?",
                               (count, now_str, user_id, lesson_id))
            else:
                cursor.execute("INSERT INTO weak_signs (user_id, lesson_id, fail_count, last_failed) VALUES (?, ?, 1, ?)",
                               (user_id, lesson_id, now_str))
            conn.commit()

    def remove_weak_sign(self, user_id: int, lesson_id: int) -> None:
        """Removes a sign from the user's weak signs list."""
        sql = "DELETE FROM weak_signs WHERE user_id = ? AND lesson_id = ?"
        with self.get_connection() as conn:
            conn.execute(sql, (user_id, lesson_id))
            conn.commit()

    def get_weak_signs(self, user_id: int) -> List[Dict[str, Any]]:
        """Retrieves the list of weak signs for the user."""
        sql = """
        SELECT w.lesson_id, w.fail_count, w.last_failed, l.sign_name, l.letter, l.unit_id
        FROM weak_signs w
        JOIN lessons l ON w.lesson_id = l.id
        WHERE w.user_id = ?
        ORDER BY w.fail_count DESC
        """
        with self.get_connection() as conn:
            rows = conn.execute(sql, (user_id,)).fetchall()
            return [dict(r) for r in rows]

    # --- DAILY CHALLENGE CRUD ---
    def get_daily_challenge(self, user_id: int, date_str: str) -> Optional[Dict[str, Any]]:
        """Retrieves daily challenge details for a user on a given date."""
        sql = "SELECT * FROM daily_challenges WHERE user_id = ? AND challenge_date = ?"
        with self.get_connection() as conn:
            row = conn.execute(sql, (user_id, date_str)).fetchone()
            return dict(row) if row else None

    def save_daily_challenge(self, user_id: int, date_str: str, signs_json: str) -> None:
        """Saves a daily challenge for a user."""
        sql = "INSERT INTO daily_challenges (user_id, challenge_date, signs_json) VALUES (?, ?, ?)"
        with self.get_connection() as conn:
            conn.execute(sql, (user_id, date_str, signs_json))
            conn.commit()

    def complete_daily_challenge(self, user_id: int, date_str: str, xp_earned: int) -> None:
        """Marks today's daily challenge as completed and records XP earned."""
        sql = "UPDATE daily_challenges SET completed = 1, xp_earned = ? WHERE user_id = ? AND challenge_date = ?"
        with self.get_connection() as conn:
            conn.execute(sql, (xp_earned, user_id, date_str))
            conn.commit()
