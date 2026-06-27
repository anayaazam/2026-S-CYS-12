# SignBridge - Gamified ASL Learning Platform

SignBridge is a full-featured, Duolingo-style desktop application for learning American Sign Language (ASL). It features real-time sign recognition from your webcam, interactive quizzes (Flashcards and real-time signing), comprehensive gamification (streaks, levels, badges, XP), Urdu and English text-to-speech, translation, and beautiful Matplotlib-driven analytics.

---

## Project Structure

```
signbridge/
├── main.py                    # App entry point, sidebar nav, screen router
├── requirements.txt           # Pinned dependencies
├── README.md                  # This setup guide
├── database/
│   ├── schema.sql             # All SQLite CREATE TABLE statements
│   └── db_manager.py         # All CRUD — users, progress, quizzes, badges
├── auth/
│   ├── login_screen.py       # Login UI + validation
│   └── register_screen.py    # Registration UI + bcrypt hashing
├── modules/
│   ├── recognizer/
│   │   ├── asl_detector.py   # Wrap Repo 2's ASLDetector class here
│   │   └── letter_buffer.py  # Port window_extract + map_extract from Repo 1
│   ├── tts/
│   │   ├── tts_engine.py     # gTTS (English+Urdu) + pyttsx3 fallback
│   │   └── translator.py     # deep_translator English→Urdu
│   ├── learning/
│   │   ├── lesson_manager.py # Load/save lesson progress, XP awarding
│   │   └── seed_lessons.py   # Populate DB with A–Z sign lessons on first run
│   ├── quiz/
│   │   ├── quiz_engine.py    # Generate questions, score, record results
│   │   └── spaced_rep.py     # Spaced repetition scheduler for weak signs
│   └── gamification/
│       ├── xp_engine.py      # XP award logic, level thresholds
│       ├── streak_tracker.py # Daily streak check + reset logic
│       └── badge_engine.py   # Badge unlock conditions + award
├── ui/
│   ├── home.py               # Dashboard: streak, XP bar, word of the day
│   ├── learn.py              # Unit/lesson browser, reference images
│   ├── practice.py           # Embedded webcam + ASLDetector + feedback
│   ├── speak.py              # ASL→Speech: sentence builder + TTS buttons
│   ├── stats.py              # Matplotlib charts embedded in CTk
│   ├── leaderboard.py        # Scrollable XP leaderboard table
│   ├── profile.py            # Avatar, stats summary, badges grid
│   ├── settings.py           # Theme, language, webcam device selector
│   └── quiz.py               # Interactive FLASHCARD and SIGN_IT quiz session UI
├── assets/
│   ├── signs/                # Reference images for each sign (A.png ... Z.png)
│   ├── fonts/                # Urdu-compatible font NotoNastaliqUrdu
│   └── icons/                # Sidebar icons
└── model/
    ├── asl_model.h5          # Repo 2's trained model (200×200 color)
    └── labels.txt            # A–Z labels
```

---

## Installation & Setup Guide

### 1. Prerequisites
Ensure you have Python 3.8+ installed on your machine.

### 2. Install Dependencies
Install all required libraries using the pinned `requirements.txt`:
```bash
pip install -r requirements.txt
```

> [!NOTE]
> If you do not have a working GPU or want to avoid heavy TensorFlow dependencies, you can still run and test the application. The system includes a **Mock/Simulation mode** that takes effect automatically if TensorFlow is not installed or if the model files are missing, allowing complete verification of all UI and gamification pathways.

### 3. Model Files Placement
To enable real-time ASL sign recognition using the deep learning model:
1. Obtain the pre-trained `asl_model.h5` and its class labels file `labels.txt` from your training run (Repo 2 structure).
2. Place these files inside the `model/` directory:
   - `signbridge/model/asl_model.h5`
   - `signbridge/model/labels.txt`
3. Ensure the labels in `labels.txt` match the model outputs (one uppercase letter/label per line).

---

## How to Add New Signs/Lessons to the Database

To expand the course curriculum beyond the default A–Z alphabet, common words, and numbers, you can modify the curriculum seed or insert records directly.

### Option A: Modify the Seed Script (Recommended for development)
1. Open [seed_lessons.py](file:///home/administrator/.gemini/antigravity/scratch/signbridge/modules/learning/seed_lessons.py).
2. Add your new signs to the corresponding list:
   - To add to **Unit 2: Common Words**, append a tuple containing `(sign_name, letter_association, instructions)` to `common_words`.
   - To add to **Unit 3: Numbers**, append to `numbers`.
   - Alternatively, create a new unit list (e.g. Unit 4) and insert them using `db.add_lesson(...)`.
3. If you already ran the app, delete the SQLite database file `signbridge/database/signbridge.db` to force a re-seed upon the next startup.

### Option B: Programmatic CRUD Insertion
You can add signs dynamically at runtime using the `DatabaseManager.add_lesson` method:
```python
from database.db_manager import DatabaseManager

db = DatabaseManager()
new_lesson_id = db.add_lesson(
    unit_id=2,                     # 1 = Alphabet, 2 = Common Words, 3 = Numbers
    sign_name="Thank You",         # Display name of the sign
    letter="T",                    # Target letter representing the sign shape
    description="Touch chin, then move hand forward and down.",
    image_path="assets/signs/THANK_YOU.png",
    difficulty=2,                  # Difficulty tier
    xp_reward=15                   # XP awarded to the user on completion
)
print(f"Added new lesson with ID: {new_lesson_id}")
```

---

## Running the Application

Launch the application using:
```bash
python main.py
```

### Features to Explore
- **Authentication**: Create a new account on the Register screen, or sign in with your credentials. Check "Remember me" to enable auto-login via `session.json`.
- **Home Dashboard**: View your streak 🔥, track XP milestones, look up the daily random "Word of the Day", and review your "Daily Challenge" card.
- **Learn Tab**: Browse lessons by unit. Click a lesson to read signing tips and view its reference card. Click **Practice This Sign** to open your webcam.
- **Real-time Practice**: Position your hand inside the highlighted ROI box. Hold the correct sign for 1.5 seconds to trigger a match, earn XP, increment your streak, and check for badge unlocks.
- **Quiz Mode**: Try 10-question mixed quizzes. Flashcard questions present signs and ask you to pick the meaning, while Sign It questions prompt you to demonstrate the sign before your camera.
- **Speak Screen**: Type or spell out sentences by signing letters sequentially. Translate your sentence to Urdu with a single click, and hear it spoken aloud in English or Urdu.
- **Stats Dashboard**: View your daily activity counts, practice accuracy trends, and curriculum completion metrics plotted dynamically on beautifully embedded Matplotlib canvases.
- **Leaderboard**: See how you rank against other local signers based on your total XP.
- **Profile**: Customize your avatar emoji and inspect your locked and unlocked achievement badges.
- **Settings**: Adjust app appearance themes, default translation preferences, and toggle between multiple connected webcam devices.
