# Quiz Engine for SignBridge
import random
from typing import List, Dict, Any, Tuple
from database.db_manager import DatabaseManager
from modules.quiz.spaced_rep import get_spaced_repetition_lessons, handle_quiz_item_result
from modules.gamification.xp_engine import XP_QUIZ_CORRECT, XP_PERFECT_QUIZ_BONUS
from modules.gamification.badge_engine import check_and_award_badges

class QuizEngine:
    """Generates quiz questions (FLASHCARD and SIGN_IT) and processes results."""

    def __init__(self, db: DatabaseManager) -> None:
        self.db = db

    def generate_quiz(self, user_id: int, mode: str = "MIXED") -> List[Dict[str, Any]]:
        """Generates a 10-question quiz for the user, mixing FLASHCARD and SIGN_IT modes
        and incorporating spaced repetition.
        """
        # Get 10 target lessons using spaced repetition
        target_lessons = get_spaced_repetition_lessons(self.db, user_id, 10)
        
        # Get all lessons for generating distractors
        all_lessons = self.db.get_lessons()
        all_names = [l["sign_name"] for l in all_lessons]
        
        questions = []
        for i, lesson in enumerate(target_lessons):
            # Determine question type
            q_type = mode
            if mode == "MIXED":
                q_type = "FLASHCARD" if i % 2 == 0 else "SIGN_IT"
                
            question: Dict[str, Any] = {
                "lesson_id": lesson["id"],
                "sign_name": lesson["sign_name"],
                "letter": lesson["letter"],
                "type": q_type,
            }
            
            if q_type == "FLASHCARD":
                question["image_path"] = lesson["image_path"]
                question["description"] = lesson["description"]
                
                # Generate 3 distractors
                correct_ans = lesson["sign_name"]
                other_names = [name for name in all_names if name != correct_ans]
                distractors = random.sample(other_names, min(3, len(other_names)))
                
                choices = distractors + [correct_ans]
                random.shuffle(choices)
                
                question["choices"] = choices
                question["correct_answer"] = correct_ans
            else:
                # SIGN_IT mode: prompt the user to sign the target letter
                question["prompt"] = f"Sign the letter: {lesson['letter']}"
                question["correct_answer"] = lesson["letter"]
                
            questions.append(question)
            
        return questions

    def record_question_outcome(self, user_id: int, lesson_id: int, is_correct: bool) -> None:
        """Handles the outcome of an individual quiz question for spaced repetition."""
        handle_quiz_item_result(self.db, user_id, lesson_id, is_correct)

    def complete_quiz(self, user_id: int, score: int, total_questions: int, mode: str) -> Tuple[int, int, List[str]]:
        """Saves quiz results, awards XP, and evaluates badge unlocks.
        Returns (xp_earned, bonus_xp, newly_unlocked_badges).
        """
        # Calculate XP
        base_xp = score * XP_QUIZ_CORRECT
        bonus_xp = XP_PERFECT_QUIZ_BONUS if score == total_questions and total_questions > 0 else 0
        total_xp = base_xp + bonus_xp
        
        # Save results in DB
        self.db.save_quiz_result(user_id, score, total_questions, mode, total_xp)
        self.db.update_user_xp(user_id, total_xp)
        
        # Award quiz_ace badge if perfect score
        if score == total_questions and total_questions > 0:
            self.db.award_badge(user_id, "quiz_ace")
            
        # Check all badges
        newly_unlocked_badges = check_and_award_badges(self.db, user_id)
        
        return total_xp, bonus_xp, newly_unlocked_badges
