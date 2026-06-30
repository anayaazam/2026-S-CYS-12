# Test suite to verify database, gamification, and translation logic for SignBridge
import unittest
import os
import shutil
import json
from database.db_manager import DatabaseManager
from modules.gamification.xp_engine import get_level_info
from modules.gamification.streak_tracker import check_and_update_streak, record_practice_activity
from modules.gamification.badge_engine import check_and_award_badges, increment_urdu_tts_counter
from modules.tts.translator import UrduTranslator
from modules.learning.seed_lessons import seed_database
TEST_DB = "test_signbridge.db"
class TestSignBridgeBackend(unittest.TestCase):
    """Verifies all database operations, gamification algorithms, and translation logic."""
    @classmethod
    def setUpClass(cls) -> None:
        # Resolve test database path
        cls.db_dir = os.path.dirname(os.path.abspath(__file__))
        cls.db_path = os.path.join(cls.db_dir, TEST_DB)
        # Clean up any leftover test database
        if os.path.exists(cls.db_path):
            os.remove(cls.db_path)
        cls.db = DatabaseManager(db_path=cls.db_path)
        seed_database(cls.db)
    @classmethod
    def tearDownClass(cls) -> None:
        # Close connection and delete test database
        if os.path.exists(cls.db_path):
            try:
                os.remove(cls.db_path)
            except Exception:
                pass
        # Clean up user counter test files
        counter_file = os.path.join(cls.db_dir, "user_1_counters.json")
        if os.path.exists(counter_file):
            try:
                os.remove(counter_file)
            except Exception:
                pass
    def test_1_database_seeding(self) -> None:
        """Verifies that lessons are seeded correctly on first launch."""
        lessons = self.db.get_lessons()
        self.assertGreater(len(lessons), 0, "Lessons database should not be empty after seeding.")
        # Check units
        unit1 = self.db.get_lessons_by_unit(1)
        self.assertEqual(len(unit1), 26, "Unit 1 should contain exactly 26 Alphabet lessons.")
        unit2 = self.db.get_lessons_by_unit(2)
        self.assertGreater(len(unit2), 0, "Unit 2 should contain seeded Common Words.")
    def test_2_user_crud_and_auth(self) -> None:
        """Verifies user creation, password hash handling, and session queries."""
        username = "test_signer"
        display = "Test Signer"
        pw_hash = "mock_bcrypt_hash_value"
        email = "test@signbridge.org"
        user_id = self.db.create_user(username, display, pw_hash, email)
        self.assertIsNotNone(user_id, "User creation should return a valid user ID.")
        # Duplicate user check
        dup_id = self.db.create_user(username, "Another Display", "hash", "email")
        self.assertIsNone(dup_id, "Duplicate usernames should be rejected by unique constraints.")
        # Fetch user
        user = self.db.get_user_by_id(user_id)
        self.assertEqual(user["username"], username)
        self.assertEqual(user["display_name"], display)
        self.assertEqual(user["xp"], 0)
    def test_3_xp_and_levels(self) -> None:
        """Verifies level tier thresholds and progress math."""
        # Test level 1 (Beginner)
        info1 = get_level_info(150)
        self.assertEqual(info1["level"], 1)
        self.assertEqual(info1["tier_name"], "Beginner")
        self.assertAlmostEqual(info1["progress"], 150/500)
        # Test level 2 (Learner)
        info2 = get_level_info(750)
        self.assertEqual(info2["level"], 2)
        self.assertEqual(info2["tier_name"], "Learner")
        self.assertEqual(info2["xp_needed"], 1250)
    def test_4_streak_tracking(self) -> None:
        """Verifies streak preservation, increments, and daily reset triggers."""
        user_id = 1 # The test user we created
        # Set last practice to yesterday to simulate active streak increment
        from datetime import datetime, timedelta
        yesterday_str = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        self.db.update_user_streak(user_id, streak=3, last_practice_date=yesterday_str)
        # Record practice for today
        new_streak, incremented, bonus = record_practice_activity(self.db, user_id)
        self.assertEqual(new_streak, 4, "Streak should increment to 4.")
        self.assertTrue(incremented)
        self.assertEqual(bonus, 0)
    def test_5_translation(self) -> None:
        """Verifies Urdu translation caching and offline fallbacks."""
        translator = UrduTranslator()
        # Test cache hit
        trans_hello = translator.translate("hello")
        self.assertEqual(trans_hello, "ہیلو")
        # Test phrase word-by-word fallback
        trans_phrase = translator.translate("hello please")
        self.assertIn("ہیلو", trans_phrase)
        self.assertIn("براہ مہربانی", trans_phrase)
    def test_6_badges(self) -> None:
        """Verifies achievement badge unlock rules and counter triggers."""
        user_id = 1
        # Unlock 'first_sign' by saving a completed lesson progress
        self.db.save_progress(user_id, lesson_id=1, completed=True, accuracy=88.5)
        newly_unlocked = check_and_award_badges(self.db, user_id)
        self.assertIn("first_sign", newly_unlocked, "first_sign badge should unlock on completing the first lesson.")
        
        # Check bilingual counter increment
        for _ in range(9):
            increment_urdu_tts_counter(self.db, user_id)
        
        # The 10th Urdu TTS should unlock bilingual badge
        unlocked = increment_urdu_tts_counter(self.db, user_id)
        self.assertTrue(unlocked, "10th Urdu TTS translation usage should unlock the Bilingual badge.")
if __name__ == "__main__":
    unittest.main()
