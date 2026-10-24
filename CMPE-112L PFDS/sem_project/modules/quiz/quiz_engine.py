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
        """Generates a 10-question quiz using spaced repetition."""
        target_lessons = get_spaced_repetition_lessons(self.db, user_id, 10)
        all_lessons = self.db.get_lessons()
        all_names = [l["sign_name"] for l in all_lessons]
        return self._build_questions(target_lessons, all_names, mode)

    def generate_quiz_from_completed(self, user_id: int, completed_ids: List[int],
                                     mode: str = "MIXED") -> List[Dict[str, Any]]:
        """Generates a quiz using only completed lessons as question targets."""
        # Get all lesson objects for completed ids
        all_lessons = self.db.get_lessons()
        completed_lessons = [l for l in all_lessons if l["id"] in completed_ids]
        all_names = [l["sign_name"] for l in all_lessons]

        if not completed_lessons:
            return []

        # Pick up to 10 questions from completed lessons
        target_count = min(10, len(completed_lessons))
        target_lessons = random.sample(completed_lessons, target_count)

        return self._build_questions(target_lessons, all_names, mode)

    def _build_questions(self, target_lessons: List[Dict], all_names: List[str],
                         mode: str) -> List[Dict[str, Any]]:
        questions = []
        for i, lesson in enumerate(target_lessons):
            q_type = mode
            if mode == "MIXED":
                q_type = "FLASHCARD" if i % 2 == 0 else "SIGN_IT"

            question: Dict[str, Any] = {
                "lesson_id": lesson["id"],
                "sign_name": lesson["sign_name"],
                "letter": lesson["letter"],
                "type": q_type,
                "image_path": lesson.get("image_path", ""),
            }

            if q_type == "FLASHCARD":
                question["description"] = lesson["description"]
                correct_ans = lesson["sign_name"]
                other_names = [name for name in all_names if name != correct_ans]
                distractors = random.sample(other_names, min(3, len(other_names)))
                choices = distractors + [correct_ans]
                random.shuffle(choices)
                question["choices"] = choices
                question["correct_answer"] = correct_ans
            else:
                question["prompt"] = f"Sign the letter: {lesson['letter']}"
                question["correct_answer"] = lesson["letter"]

            questions.append(question)

        return questions

    def record_question_outcome(self, user_id: int, lesson_id: int, is_correct: bool) -> None:
        handle_quiz_item_result(self.db, user_id, lesson_id, is_correct)

    def complete_quiz(self, user_id: int, score: int, total_questions: int,
                      mode: str) -> Tuple[int, int, List[str]]:
        base_xp = score * XP_QUIZ_CORRECT
        bonus_xp = XP_PERFECT_QUIZ_BONUS if score == total_questions and total_questions > 0 else 0
        total_xp = base_xp + bonus_xp

        self.db.save_quiz_result(user_id, score, total_questions, mode, total_xp)
        self.db.update_user_xp(user_id, total_xp)

        if score == total_questions and total_questions > 0:
            self.db.award_badge(user_id, "quiz_ace")

        newly_unlocked_badges = check_and_award_badges(self.db, user_id)
        return total_xp, bonus_xp, newly_unlocked_badges
