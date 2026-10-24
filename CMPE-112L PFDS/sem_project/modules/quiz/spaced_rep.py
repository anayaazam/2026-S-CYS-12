# Spaced Repetition Scheduler for SignBridge
import random
from typing import List, Dict, Any
from database.db_manager import DatabaseManager

def get_spaced_repetition_lessons(db: DatabaseManager, user_id: int, total_count: int = 10) -> List[Dict[str, Any]]:
    """Selects a mix of lessons, prioritizing weak signs that the user has failed,
    supplemented with random/new lessons.
    """
    # 1. Get user's weak signs
    weak_records = db.get_weak_signs(user_id)
    weak_lesson_ids = [r["lesson_id"] for r in weak_records]
    
    # 2. Get all lessons
    all_lessons = db.get_lessons()
    if not all_lessons:
        return []

    # Map lessons for easy lookup
    lessons_by_id = {l["id"]: l for l in all_lessons}
    
    selected_lessons = []
    
    # 3. Add weak signs first, up to 50% of the quiz count to avoid overwhelming
    max_weak = min(total_count // 2, len(weak_lesson_ids))
    shuffled_weak = list(weak_lesson_ids)
    random.shuffle(shuffled_weak)
    
    for l_id in shuffled_weak[:max_weak]:
        if l_id in lessons_by_id:
            selected_lessons.append(lessons_by_id[l_id])

    # 4. Fill the remaining spots with other lessons the user has unlocked/practiced or random
    remaining_needed = total_count - len(selected_lessons)
    
    # Exclude already selected lessons from candidates
    candidates = [l for l in all_lessons if l not in selected_lessons]
    
    if len(candidates) >= remaining_needed:
        selected_lessons.extend(random.sample(candidates, remaining_needed))
    else:
        selected_lessons.extend(candidates)
        
    # Shuffle the final selection
    random.shuffle(selected_lessons)
    return selected_lessons[:total_count]

def handle_quiz_item_result(db: DatabaseManager, user_id: int, lesson_id: int, is_correct: bool) -> None:
    """Updates spaced repetition records based on a quiz question outcome.
    If correct, decreases fail count (or removes weak sign).
    If incorrect, adds/increments weak sign fail count.
    """
    if is_correct:
        # Check if it was a weak sign
        weak_signs = db.get_weak_signs(user_id)
        is_weak = any(r["lesson_id"] == lesson_id for r in weak_signs)
        if is_weak:
            # We can either decrement the count or remove it. Let's remove it once they get it right!
            db.remove_weak_sign(user_id, lesson_id)
    else:
        # User failed the sign, add to weak signs or increment fail count
        db.add_weak_sign(user_id, lesson_id)
