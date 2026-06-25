# Database Seeding Script for SignBridge
import os
import json
from database.db_manager import DatabaseManager

def seed_database(db: DatabaseManager) -> None:
    """Seeds the database with lessons for Alphabet (Unit 1), Common Words (Unit 2),
    and Numbers (Unit 3) if they do not already exist.
    """
    existing = db.get_lessons()
    if existing:
        return # Already seeded

    # Unit 1: ASL Alphabet (A-Z)
    alphabet_lessons = [
        ("A", "Make a fist, with the thumb resting against the side of the index finger."),
        ("B", "Open hand, fingers together, thumb folded across the palm."),
        ("C", "Curved hand forming the letter 'C' shape."),
        ("D", "Index finger pointing straight up, other fingers touching thumb to form a circle."),
        ("E", "Curl fingers down to rest lightly on top of the thumb, which is folded across palm."),
        ("F", "Touch index finger and thumb together, other three fingers spread straight up."),
        ("G", "Point index finger and thumb parallel to the ground, like pinching something."),
        ("H", "Index and middle fingers extended straight out together horizontally."),
        ("I", "Pinky finger pointing straight up, other fingers folded into a fist with thumb over them."),
        ("J", "Pinky finger extended, drawing a 'J' shape in the air."),
        ("K", "Index and middle fingers pointing up in a 'V', thumb touching middle finger's joint."),
        ("L", "Index finger pointing up, thumb pointing out, forming an 'L' shape."),
        ("M", "Fist with the thumb tucked under the first three fingers (index, middle, ring)."),
        ("N", "Fist with the thumb tucked under the first two fingers (index, middle)."),
        ("O", "Form an 'O' shape with all fingers and thumb touching at the tips."),
        ("P", "A 'K' sign pointed downwards towards the ground."),
        ("Q", "A 'G' sign pointed downwards towards the ground."),
        ("R", "Index and middle fingers crossed over each other."),
        ("S", "Make a fist, with the thumb resting across the front of the fingers."),
        ("T", "Fist with the thumb tucked under the index finger."),
        ("U", "Index and middle fingers extended straight up together."),
        ("V", "Index and middle fingers extended straight up, spread apart in a 'V' shape."),
        ("W", "Index, middle, and ring fingers extended and spread apart in a 'W' shape."),
        ("X", "Index finger hooked like a claw, other fingers folded into a fist."),
        ("Y", "Thumb and pinky finger extended, other fingers folded down."),
        ("Z", "Index finger extended, drawing a 'Z' shape in the air.")
    ]

    for letter, desc in alphabet_lessons:
        db.add_lesson(
            unit_id=1,
            sign_name=letter,
            letter=letter,
            description=desc,
            image_path=f"assets/signs/{letter}.png",
            difficulty=1,
            xp_reward=10
        )

    # Unit 2: Common Words
    common_words = [
        ("Hello", "H", "Open hand, palm facing down/out, moving from temple outward in a salute."),
        ("Please", "P", "Flat hand rub on chest in a circular motion clockwise."),
        ("Thank You", "T", "Touch fingertips of active flat hand to chin, then move hand forward and down."),
        ("Yes", "Y", "Make a fist and nod it up and down like a head nodding yes."),
        ("No", "N", "Snap index and middle fingers down onto the thumb."),
        ("Help", "H", "Place closed hand, thumb up, on open palm of the other hand, lift both together."),
        ("Sorry", "S", "Make a fist with thumb over fingers, rub in a circular motion over chest.")
    ]

    for name, letter, desc in common_words:
        db.add_lesson(
            unit_id=2,
            sign_name=name,
            letter=letter,
            description=desc,
            image_path=f"assets/signs/{name.upper()}.png",
            difficulty=2,
            xp_reward=15
        )

    # Unit 3: Numbers (0-9)
    numbers = [
        ("0", "O", "Form an O shape with fingers and thumb, looking like a zero."),
        ("1", "1", "Extend index finger up, palm facing inward."),
        ("2", "2", "Extend index and middle fingers up, palm facing inward."),
        ("3", "3", "Extend thumb, index, and middle fingers, palm facing inward."),
        ("4", "4", "Extend four fingers (index, middle, ring, pinky) up, thumb folded in, palm facing outward."),
        ("5", "5", "Open hand, all five fingers extended and spread apart, palm facing outward."),
        ("6", "6", "Touch thumb and pinky finger tips together, other fingers extended up."),
        ("7", "7", "Touch thumb and ring finger tips together, other fingers extended up."),
        ("8", "8", "Touch thumb and middle finger tips together, other fingers extended up."),
        ("9", "9", "Touch thumb and index finger tips together (F shape), other fingers extended up.")
    ]

    for name, letter, desc in numbers:
        db.add_lesson(
            unit_id=3,
            sign_name=name,
            letter=letter,
            description=desc,
            image_path=f"assets/signs/NUM_{name}.png",
            difficulty=2,
            xp_reward=15
        )
