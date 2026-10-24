# XP and Level Engine for SignBridge
from typing import Tuple, Dict, Any

# XP Rewards constants
XP_LESSON_COMPLETE = 10
XP_QUIZ_CORRECT = 5
XP_PERFECT_QUIZ_BONUS = 30
XP_DAILY_CHALLENGE_COMPLETE = 50
XP_STREAK_7DAY_BONUS = 100

# Level Thresholds
LEVELS = [
    {"name": "Beginner", "min_xp": 0, "max_xp": 499, "level": 1},
    {"name": "Learner", "min_xp": 500, "max_xp": 1999, "level": 2},
    {"name": "Intermediate", "min_xp": 2000, "max_xp": 4999, "level": 3},
    {"name": "Advanced", "min_xp": 5000, "max_xp": 9999, "level": 4},
    {"name": "Expert", "min_xp": 10000, "max_xp": 9999999, "level": 5}
]

def get_level_info(xp: int) -> Dict[str, Any]:
    """Returns level tier name, level number, progress percentage within the level,
    and XP remaining for the next level.
    """
    for tier in LEVELS:
        if tier["min_xp"] <= xp <= tier["max_xp"]:
            lvl_range = tier["max_xp"] - tier["min_xp"] + 1
            xp_in_lvl = xp - tier["min_xp"]
            progress = min(1.0, max(0.0, xp_in_lvl / lvl_range)) if lvl_range > 0 else 1.0
            next_xp = tier["max_xp"] + 1 if tier["level"] < 5 else xp
            xp_needed = max(0, next_xp - xp)
            
            return {
                "level": tier["level"],
                "tier_name": tier["name"],
                "progress": progress,
                "xp_needed": xp_needed,
                "level_min": tier["min_xp"],
                "level_max": tier["max_xp"]
            }
    
    # Fallback
    return {
        "level": 5,
        "tier_name": "Expert",
        "progress": 1.0,
        "xp_needed": 0,
        "level_min": 10000,
        "level_max": 9999999
    }
