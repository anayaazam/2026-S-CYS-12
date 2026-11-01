# SignBridge – Gamified ASL Learning Platform

SignBridge is a desktop application (PyQt5) for learning American Sign Language, in the style of Duolingo. It recognizes signs from your webcam in real time, teaches them through lessons and quizzes, and rewards progress with XP, levels, streaks and badges. It also builds sentences from signed letters and reads them aloud in English or Urdu.

> Semester project for **CMPE-112L – Programming Fundamentals and Data Science**.

---

## Features

- **Accounts** – Register and log in (passwords hashed with bcrypt). "Remember Me" keeps you signed in using a local `session.json`.
- **Learn** – Three units: Alphabet (A–Z), Common Words, and Numbers (0–9). Each lesson has a reference image and signing tips.
- **Practice** – Hold a sign in front of your webcam; the model checks it, and correct signs earn XP.
- **Quiz** – 10-question mixed quizzes: *Flashcard* (pick the meaning) and *Sign It* (show the sign on camera). Weak signs are scheduled for review with spaced repetition.
- **Speak** – Spell out sentences by signing letters, translate them to Urdu, and play them as speech (English or Urdu).
- **Gamification** – XP, five levels (Beginner to Expert), daily streaks, daily challenge, and badges.
- **Stats** – Matplotlib charts for daily activity, practice accuracy and curriculum progress.
- **Leaderboard, Profile, Settings** – XP ranking, avatar and badges, theme and webcam selection.

---

## Project Structure

```
sem_project/
├── main.py                    # App entry point, sidebar navigation, screen router
├── requirements.txt           # Python dependencies
├── test_SignBridge.py         # Unit tests (database, XP, streaks, translation, badges)
├── test_logic.py              # Unit tests (letter buffer, spaced repetition, quiz engine)
├── README.md
├── authorization/
│   ├── login_screen.py        # Login screen and validation
│   └── register_screen.py     # Registration screen (bcrypt hashing)
├── database/
│   ├── schema.sql             # SQLite table definitions
│   └── db_manager.py          # All database operations (users, progress, quizzes, badges)
├── modules/
│   ├── recognizer/
│   │   ├── asl_detector.py    # Loads the Keras model and predicts signs (mock mode if unavailable)
│   │   └── letter_buffer.py   # Smooths predictions and builds stable letters/sentences
│   ├── tts/
│   │   ├── tts_engine.py      # Text-to-speech (gTTS online, pyttsx3 offline fallback)
│   │   └── translator.py      # English to Urdu translation (deep-translator)
│   ├── learning/
│   │   ├── lesson_manager.py  # Lesson progress and XP awarding
│   │   └── seed_lessons.py    # Fills the database with lessons on first run
│   ├── quiz/
│   │   ├── quiz_engine.py     # Question generation and scoring
│   │   └── spaced_rep.py      # Spaced-repetition scheduler for weak signs
│   └── gamification/
│       ├── xp_engine.py       # XP rewards and level thresholds
│       ├── streak_tracker.py  # Daily streak logic
│       └── badge_engine.py    # Badge unlock conditions
├── ui/                        # One file per screen
│   ├── home.py  learn.py  practice.py  quiz.py  speak.py
│   └── stats.py  leaderboard.py  profile.py  settings.py
├── pyqt_screens/              # Qt Designer (.ui) layout files for each screen
├── assets/
│   ├── signs/                 # Reference images (A–Z, numbers, common words)
│   └── icons/                 # Avatars and badge icons
└── model/
    ├── asl_model.h5           # Trained sign-recognition model (200×200 RGB input)
    └── labels.txt             # Class labels: A–Z, delete, nothing, space
```

The database file `database/signbridge.db` is **not** stored in the repository. It is created and filled with lessons automatically the first time you run the app.

---

## Installation

### 1. Requirements

- Python 3.10 or newer (developed with 3.10 and 3.12)
- A webcam (for Practice, Quiz "Sign It" and Speak)
- Internet connection for Google TTS and Urdu translation (offline speech falls back to pyttsx3)

### 2. Install dependencies

From the `sem_project` folder:

```bash
pip install -r requirements.txt
```

### 3. Urdu font (optional)

The Speak screen displays Urdu text in **Noto Nastaliq Urdu**. Install it on your system for correct rendering; without it, Qt falls back to a default font.

### 4. Model files

The recognition model is included in `model/`:

- `model/asl_model.h5`
- `model/labels.txt` (one label per line, same order as the model outputs)

> **Mock mode:** If TensorFlow is not installed or the model file is missing, the app still starts. The recognizer switches to a simulation mode so you can try every screen (lessons, quizzes, gamification, stats) without real sign detection.

---

## Running the App

```bash
python main.py
```

Create an account on the Register screen, then use the sidebar to move between Home, Learn, Quiz, Speak, Stats, Leaderboard, Profile and Settings. Practice opens from a lesson in the Learn tab ("Practice This Sign").

For real-time practice, place your hand inside the highlighted box and hold the sign steady for about 1.5 seconds.

## Running the Tests

```bash
python -m unittest -v
```

This runs both test files. They use temporary databases and clean up after themselves.

---

## Adding New Signs or Lessons

### Option A – Edit the seed script

1. Open `modules/learning/seed_lessons.py`.
2. Add a tuple to the right list. Common Words and Numbers use this format:
   `(sign_name, letter, description, image_path)`
   Example:
   ```python
   ("Water", "W", "Tap the index side of a W-hand on your chin.", "assets/signs/water.png")
   ```
3. Add the image to `assets/signs/`.
4. Delete `database/signbridge.db` and restart the app so it is re-seeded.

### Option B – Add a lesson from code

```python
from database.db_manager import DatabaseManager

db = DatabaseManager()
lesson_id = db.add_lesson(
    unit_id=2,                  # 1 = Alphabet, 2 = Common Words, 3 = Numbers
    sign_name="Thank You",
    letter="T",
    description="Touch chin with fingertips, then move the hand forward and down.",
    image_path="assets/signs/T.png",
    difficulty=2,
    xp_reward=15,
)
print(f"Added lesson {lesson_id}")
```

---

## Credits

- **Sign-recognition model:** *add who trained it, or the repo and link it came from*
- **Dataset:** *add dataset name, link and license*
- **Letter smoothing logic (`letter_buffer.py`):** *add the original repo or author if it was adapted*
- **Sign reference images:** *add where the images in `assets/signs` came from*
- **Libraries:** PyQt5, TensorFlow/Keras, OpenCV, NumPy, Matplotlib, bcrypt, gTTS, pyttsx3, pygame, deep-translator.

## Author

*add your name, registration number and section*
