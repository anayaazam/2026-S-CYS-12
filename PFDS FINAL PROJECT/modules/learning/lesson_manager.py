# Lesson Manager for SignBridge
from typing import List, Dict, Any, Tuple
from database.db_manager import DatabaseManager
from modules.gamification.xp_engine import XP_LESSON_COMPLETE, XP_DAILY_CHALLENGE_COMPLETE
from modules.gamification.streak_tracker import record_practice_activity
from modules.gamification.badge_engine import check_and_award_badges
import json
from datetime import datetime

class LessonManager:
    """Manages lessons, saves user progress, awards XP, and coordinates with gamification engines."""

    def __init__(self, db: DatabaseManager) -> None:
        self.db = db

    def get_lesson(self, lesson_id: int) -> Dict[str, Any]:
        """Retrieves a single lesson."""
        lesson = self.db.get_lesson_by_id(lesson_id)
        if not lesson:
            raise ValueError(f"Lesson {lesson_id} not found.")
        return lesson

    def get_unit_lessons(self, unit_id: int) -> List[Dict[str, Any]]:
        """Retrieves all lessons in a unit."""
        return self.db.get_lessons_by_unit(unit_id)

    def complete_lesson_attempt(self, user_id: int, lesson_id: int, accuracy: float) -> Tuple[bool, int, List[str]]:
        """Records a practice attempt for a lesson. If accuracy > 75%, marks the lesson completed.
        Awards XP and checks for badge unlocks.
        Returns (completed, xp_earned, newly_unlocked_badges).
        """
        lesson = self.get_lesson(lesson_id)
        target_accuracy = 75.0
        completed = (accuracy >= target_accuracy)
        
        # 1. Save progress in DB
        newly_completed, best_acc = self.db.save_progress(user_id, lesson_id, completed, accuracy)
        
        xp_earned = 0
        newly_unlocked_badges = []

        if newly_completed:
            # 2. Award lesson completion XP
            xp_reward = lesson.get("xp_reward", XP_LESSON_COMPLETE)
            self.db.update_user_xp(user_id, xp_reward)
            xp_earned += xp_reward
            
            # 3. Record practice activity for streak increment
            _, _, streak_xp = record_practice_activity(self.db, user_id)
            xp_earned += streak_xp
            
            # 4. Check and update daily challenge progress
            dc_xp = self.check_and_update_daily_challenge(user_id, lesson_id)
            xp_earned += dc_xp
            
            # 5. Evaluate and award badges
            newly_unlocked_badges = check_and_award_badges(self.db, user_id)
        else:
            # If not completed but they failed a sign (accuracy < 70%), update weak signs
            if accuracy < 70.0:
                self.db.add_weak_sign(user_id, lesson_id)
            elif accuracy >= 75.0:
                # If they passed but it wasn't a "new" completion, they still get a tiny participation XP
                # Let's say +2 XP or just record the activity for streak
                _, _, streak_xp = record_practice_activity(self.db, user_id)
                xp_earned += streak_xp
                
                # Check daily challenge in case this was a re-run of a challenge sign
                dc_xp = self.check_and_update_daily_challenge(user_id, lesson_id)
                xp_earned += dc_xp

        return completed, xp_earned, newly_unlocked_badges

    def check_and_update_daily_challenge(self, user_id: int, lesson_id: int) -> int:
        """Checks if the completed lesson is part of today's daily challenge.
        If it completes the daily challenge, awards 50 XP.
        """
        today_str = datetime.now().strftime("%Y-%m-%d")
        challenge = self.db.get_daily_challenge(user_id, today_str)
        if not challenge or challenge["completed"]:
            return 0

        try:
            signs_list = json.loads(challenge["signs_json"])
        except Exception:
            return 0

        if lesson_id in signs_list:
            # Let's see if the user has completed all 5 signs of the challenge
            progress = self.db.get_user_progress(user_id)
            
            all_completed = True
            for s_id in signs_list:
                # Must be completed and the last attempt must be today to count towards today's challenge
                # Or simply completed. Let's check if they have completed it.
                if s_id not in progress or not progress[s_id]["completed"]:
                    all_completed = False
                    break
            
            if all_completed:
                # Mark daily challenge as completed
                self.db.complete_daily_challenge(user_id, today_str, XP_DAILY_CHALLENGE_COMPLETE)
                self.db.update_user_xp(user_id, XP_DAILY_CHALLENGE_COMPLETE)
                return XP_DAILY_CHALLENGE_COMPLETE

        return 0
