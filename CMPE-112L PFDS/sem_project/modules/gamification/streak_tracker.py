# Streak Tracker for SignBridge
from datetime import datetime, timedelta
from typing import Tuple
from database.db_manager import DatabaseManager

def check_and_update_streak(db: DatabaseManager, user_id: int) -> Tuple[int, bool]:
    """Checks the user's last practice date. Resets streak to 0 if they missed a day.
    Returns (current_streak, was_reset).
    """
    user = db.get_user_by_id(user_id)
    if not user:
        return 0, False

    last_practice_str = user.get("last_practice_date")
    current_streak = user.get("streak", 0)
    
    if not last_practice_str:
        if current_streak > 0:
            db.update_user_streak(user_id, 0, None)
            return 0, True
        return 0, False

    try:
        last_practice = datetime.strptime(last_practice_str, "%Y-%m-%d").date()
    except ValueError:
        # Invalid date format, reset
        db.update_user_streak(user_id, 0, None)
        return 0, True

    today = datetime.now().date()
    yesterday = today - timedelta(days=1)

    if last_practice == today or last_practice == yesterday:
        # Streak is maintained
        return current_streak, False
    else:
        # Missed a day, streak resets to 0
        db.update_user_streak(user_id, 0, last_practice_str)
        return 0, True

def record_practice_activity(db: DatabaseManager, user_id: int) -> Tuple[int, bool, int]:
    """Records that the user practiced today. Increments streak if appropriate.
    Returns (new_streak, streak_incremented, xp_rewarded).
    """
    user = db.get_user_by_id(user_id)
    if not user:
        return 0, False, 0

    last_practice_str = user.get("last_practice_date")
    current_streak = user.get("streak", 0)
    today_str = datetime.now().strftime("%Y-%m-%d")

    if last_practice_str == today_str:
        # Already practiced today, streak doesn't change
        return current_streak, False, 0

    # Determine new streak
    if not last_practice_str:
        new_streak = 1
    else:
        try:
            last_practice = datetime.strptime(last_practice_str, "%Y-%m-%d").date()
        except ValueError:
            last_practice = None

        today = datetime.now().date()
        yesterday = today - timedelta(days=1)

        if last_practice == yesterday:
            new_streak = current_streak + 1
        elif last_practice == today:
            new_streak = current_streak
        else:
            new_streak = 1

    # Check for 7-day streak bonus
    xp_bonus = 0
    if new_streak > 0 and new_streak % 7 == 0:
        # Award 7-day streak bonus (+100 XP)
        db.update_user_xp(user_id, 100)
        xp_bonus = 100

    db.update_user_streak(user_id, new_streak, today_str)
    return new_streak, True, xp_bonus
