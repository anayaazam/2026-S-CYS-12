# Database Seeding Script for SignBridge
import os
import json
from database.db_manager import DatabaseManager

def seed_database(db: DatabaseManager) -> None:
    """Seeds the database with lessons for Alphabet (Unit 1), Common Words (Unit 2),
    and Numbers (Unit 3) if they do not already exist.
    """
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

    with db.get_connection() as conn:
        for letter, desc in alphabet_lessons:
            row = conn.execute("SELECT id FROM lessons WHERE sign_name = ? AND unit_id = ?", (letter, 1)).fetchone()
            if not row:
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
        # Has dedicated sign image
        ("Hello", "H", "Open hand, palm facing down/out, moving from temple outward in a salute.", "assets/signs/H.png"),
        ("Please", "P", "Flat hand rub on chest in a circular motion clockwise.", "assets/signs/please.png"),
        ("Thank You", "T", "Touch fingertips of active flat hand to chin, then move hand forward and down.", "assets/signs/T.png"),
        ("Yes", "Y", "Make a fist and nod it up and down like a head nodding yes.", "assets/signs/yes.png"),
        ("No", "N", "Snap index and middle fingers down onto the thumb.", "assets/signs/no.png"),
        ("Help", "H", "Place closed hand, thumb up, on open palm of the other hand, lift both together.", "assets/signs/help.png"),
        ("Sorry", "S", "Make a fist with thumb over fingers, rub in a circular motion over chest.", "assets/signs/S.png"),
        ("Good", "G", "Flat hand moves from mouth down to the palm of the other hand.", "assets/signs/G.png"),
        ("Happy", "H", "Flat hands pat the chest in an upward circular motion.", "assets/signs/H.png"),
        ("Sad", "S", "Bring both hands down in front of your face, palms facing in, with a sad expression.", "assets/signs/S.png"),
        ("Love", "L", "Cross both fists over your chest, palms facing in.", "assets/signs/L.png"),
        ("More", "M", "Bring both hands together, touching the fingertips of your flattened O-shaped hands.", "assets/signs/M.png"),
        ("Eat", "E", "Bring your dominant hand, formed into a flat O-shape, to your mouth twice.", "assets/signs/E.png"),
        ("Drink", "D", "Form a C-shape with your dominant hand and move it to your mouth as if drinking from a cup.", "assets/signs/D.png")
    ]

    with db.get_connection() as conn:
        for name, letter, desc, img in common_words:
            row = conn.execute("SELECT id FROM lessons WHERE sign_name = ? AND unit_id = ?", (name, 2)).fetchone()
            if not row:
                db.add_lesson(
                    unit_id=2,
                    sign_name=name,
                    letter=letter,
                    description=desc,
                    image_path=img,
                    difficulty=2,
                    xp_reward=15
                )

    # Unit 3: Numbers (0-9)
    numbers = [
        ("0", "O", "Form an O shape with fingers and thumb, looking like a zero.", "assets/signs/ten.png"),
        ("1", "D", "Extend index finger up, palm facing inward.", "assets/signs/one.png"),
        ("2", "V", "Extend index and middle fingers up, palm facing inward.", "assets/signs/two.png"),
        ("3", "W", "Extend thumb, index, and middle fingers, palm facing inward.", "assets/signs/three.png"),
        ("4", "B", "Extend four fingers (index, middle, ring, pinky) up, thumb folded in, palm facing outward.", "assets/signs/four.png"),
        ("5", "B", "Open hand, all five fingers extended and spread apart, palm facing outward.", "assets/signs/five.png"),
        ("6", "W", "Touch thumb and pinky finger tips together, other fingers extended up.", "assets/signs/six.png"),
        ("7", "F", "Touch thumb and ring finger tips together, other fingers extended up.", "assets/signs/seven.png"),
        ("8", "F", "Touch thumb and middle finger tips together, other fingers extended up.", "assets/signs/eight.png"),
        ("9", "F", "Touch thumb and index finger tips together (F shape), other fingers extended up.", "assets/signs/nine.png")
    ]

    with db.get_connection() as conn:
        for name, letter, desc, img in numbers:
            row = conn.execute("SELECT id FROM lessons WHERE sign_name = ? AND unit_id = ?", (name, 3)).fetchone()
            if not row:
                db.add_lesson(
                    unit_id=3,
                    sign_name=name,
                    letter=letter,
                    description=desc,
                    image_path=img,
                    difficulty=2,
                    xp_reward=15
                )
