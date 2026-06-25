# Badge Engine for SignBridge
import json
import os
from typing import List, Dict, Any, Tuple
from database.db_manager import DatabaseManager

BADGES = {
    "first_sign": {
        "name": "First Sign",
        "description": "Complete your very first lesson",
        "emoji": "👋"
    },
    "alphabet_done": {
        "name": "Alphabet Master",
        "description": "Complete all 26 ASL alphabet lessons",
        "emoji": "🔤"
    },
    "week_warrior": {
        "name": "Week Warrior",
        "description": "Achieve a 7-day practice streak",
        "emoji": "🔥"
    },
    "quiz_ace": {
        "name": "Quiz Ace",
        "description": "Score 100% on any quiz",
        "emoji": "💯"
    },
    "speed_signer": {
        "name": "Speed Signer",
        "description": "Get 5 correct signs in Practice under 30 seconds",
        "emoji": "⚡"
    },
    "bilingual": {
        "name": "Bilingual Signer",
        "description": "Use Urdu TTS translation 10 times",
        "emoji": "🗣️"
    },
    "dedicated": {
        "name": "Dedicated Learner",
        "description": "Practice for 30 days in total",
        "emoji": "🎓"
    }
}

def check_and_award_badges(db: DatabaseManager, user_id: int) -> List[str]:
    """Evaluates user milestones and unlocks any eligible badges.
    Returns a list of badge_ids that were newly unlocked in this check.
    """
    unlocked = db.get_unlocked_badges(user_id)
    newly_unlocked = []
    
    # 1. First Sign
    if "first_sign" not in unlocked:
        progress = db.get_user_progress(user_id)
        # Check if at least one lesson is completed
        if any(p.get("completed") for p in progress.values()):
            if db.award_badge(user_id, "first_sign"):
                newly_unlocked.append("first_sign")

    # 2. Alphabet Master (Complete all 26 alphabet lessons, Unit 1)
    if "alphabet_done" not in unlocked:
        progress = db.get_user_progress(user_id)
        unit1_lessons = db.get_lessons_by_unit(1)
        if unit1_lessons:
            # Check if all lessons in Unit 1 are completed
            all_completed = True
            for lesson in unit1_lessons:
                l_id = lesson["id"]
                if l_id not in progress or not progress[l_id].get("completed"):
                    all_completed = False
                    break
            if all_completed:
                if db.award_badge(user_id, "alphabet_done"):
                    newly_unlocked.append("alphabet_done")

    # 3. Week Warrior (7-day streak)
    if "week_warrior" not in unlocked:
        user = db.get_user_by_id(user_id)
        if user and user.get("streak", 0) >= 7:
            if db.award_badge(user_id, "week_warrior"):
                newly_unlocked.append("week_warrior")

    # 4. Dedicated Learner (Practice 30 days total)
    # We can approximate this by the number of attempts or unique days in progress/quizzes
    if "dedicated" not in unlocked:
        progress = db.get_user_progress(user_id)
        total_attempts = sum(p.get("attempts", 0) for p in progress.values())
        if total_attempts >= 30:
            if db.award_badge(user_id, "dedicated"):
                newly_unlocked.append("dedicated")

    return newly_unlocked

def increment_urdu_tts_counter(db: DatabaseManager, user_id: int) -> bool:
    """Increments Urdu TTS usage counter. Awards 'bilingual' badge if it hits 10.
    Returns True if the 'bilingual' badge was unlocked.
    """
    unlocked = db.get_unlocked_badges(user_id)
    if "bilingual" in unlocked:
        return False

    # Store Urdu TTS count in a small local JSON or cache
    # To keep it simple, let's write to a local config file in the user's directory
    config_dir = os.path.dirname(db.db_path)
    counter_file = os.path.join(config_dir, f"user_{user_id}_counters.json")
    
    data = {}
    if os.path.exists(counter_file):
        try:
            with open(counter_file, "r") as f:
                data = json.load(f)
        except Exception:
            pass
            
    count = data.get("urdu_tts_count", 0) + 1
    data["urdu_tts_count"] = count
    
    try:
        with open(counter_file, "w") as f:
            json.dump(data, f)
    except Exception:
        pass

    if count >= 10:
        return db.award_badge(user_id, "bilingual")
    return False
