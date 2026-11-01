import os
import tempfile
import unittest

from database.db_manager import DatabaseManager
from modules.learning.seed_lessons import seed_database
from modules.quiz.quiz_engine import QuizEngine
from modules.quiz.spaced_rep import (
    get_spaced_repetition_lessons,
    handle_quiz_item_result,
)
from modules.recognizer.letter_buffer import LetterBuffer


def make_database(seed=True):
    handle, path = tempfile.mkstemp(suffix=".db")
    os.close(handle)
    db = DatabaseManager(db_path=path)
    if seed:
        seed_database(db)
    return db, path


def remove_file(path):
    try:
        os.remove(path)
    except OSError:
        pass


class TestLetterBuffer(unittest.TestCase):
    def setUp(self):
        self.buffer = LetterBuffer()

    def feed(self, letter, times):
        result = None
        for _ in range(times):
            result = self.buffer.add_prediction(letter)
        return result

    def test_letter_is_not_stable_before_threshold(self):
        self.assertEqual(self.feed("A", 9), (None, False))

    def test_letter_becomes_stable_at_threshold(self):
        self.assertEqual(self.feed("A", 10), ("A", True))

    def test_same_letter_is_only_reported_once(self):
        self.feed("A", 10)
        self.assertEqual(self.buffer.add_prediction("A"), ("A", False))
        self.assertEqual(self.buffer.get_sentence(), "A")

    def test_empty_prediction_returns_nothing(self):
        self.assertEqual(self.buffer.add_prediction(None), (None, False))

    def test_new_letter_extends_sentence(self):
        self.feed("A", 10)
        self.feed("B", 10)
        self.assertEqual(self.buffer.get_sentence(), "AB")

    def test_repeated_letters_are_capped(self):
        for _ in range(8):
            self.buffer.map_extract("A")
        self.assertEqual(self.buffer.get_sentence(), "AAAA")

    def test_space_allows_same_letter_again(self):
        self.feed("A", 10)
        self.buffer.add_space()
        self.assertEqual(self.buffer.add_prediction("A"), ("A", True))
        self.assertEqual(self.buffer.get_sentence(), "A A")

    def test_space_is_not_duplicated(self):
        self.feed("A", 10)
        self.buffer.add_space()
        self.buffer.add_space()
        self.assertEqual(self.buffer.get_sentence(), "A ")

    def test_backspace_removes_last_character(self):
        self.feed("A", 10)
        self.feed("B", 10)
        self.buffer.backspace()
        self.assertEqual(self.buffer.get_sentence(), "A")

    def test_clear_resets_everything(self):
        self.feed("A", 10)
        self.buffer.clear()
        self.assertEqual(self.buffer.get_sentence(), "")
        self.assertEqual(self.buffer.window, [])


class DatabaseTestCase(unittest.TestCase):
    seed = True

    @classmethod
    def setUpClass(cls):
        cls.db, cls.db_path = make_database(cls.seed)
        cls.user_count = 0

    @classmethod
    def tearDownClass(cls):
        remove_file(cls.db_path)

    def new_user(self):
        type(self).user_count += 1
        name = "learner_%d" % type(self).user_count
        return self.db.create_user(name, name, "hash", name + "@signbridge.org")


class TestSpacedRepetition(DatabaseTestCase):
    def weak_ids(self, user_id):
        return [row["lesson_id"] for row in self.db.get_weak_signs(user_id)]

    def test_returns_requested_number_of_unique_lessons(self):
        user_id = self.new_user()
        lessons = get_spaced_repetition_lessons(self.db, user_id, 10)
        ids = [lesson["id"] for lesson in lessons]
        self.assertEqual(len(ids), 10)
        self.assertEqual(len(set(ids)), 10)

    def test_weak_signs_are_prioritised(self):
        user_id = self.new_user()
        for lesson_id in (1, 2, 3):
            self.db.add_weak_sign(user_id, lesson_id)
        lessons = get_spaced_repetition_lessons(self.db, user_id, 10)
        ids = {lesson["id"] for lesson in lessons}
        self.assertTrue({1, 2, 3}.issubset(ids))

    def test_wrong_answer_marks_sign_as_weak(self):
        user_id = self.new_user()
        handle_quiz_item_result(self.db, user_id, 1, False)
        self.assertEqual(self.weak_ids(user_id), [1])

    def test_repeated_wrong_answers_increase_fail_count(self):
        user_id = self.new_user()
        handle_quiz_item_result(self.db, user_id, 1, False)
        handle_quiz_item_result(self.db, user_id, 1, False)
        self.assertEqual(self.db.get_weak_signs(user_id)[0]["fail_count"], 2)

    def test_correct_answer_clears_weak_sign(self):
        user_id = self.new_user()
        self.db.add_weak_sign(user_id, 1)
        handle_quiz_item_result(self.db, user_id, 1, True)
        self.assertEqual(self.weak_ids(user_id), [])

    def test_correct_answer_on_normal_sign_changes_nothing(self):
        user_id = self.new_user()
        handle_quiz_item_result(self.db, user_id, 5, True)
        self.assertEqual(self.weak_ids(user_id), [])


class TestSpacedRepetitionWithoutLessons(DatabaseTestCase):
    seed = False

    def test_empty_database_returns_no_lessons(self):
        user_id = self.new_user()
        self.assertEqual(get_spaced_repetition_lessons(self.db, user_id), [])


class TestQuizEngine(DatabaseTestCase):
    def setUp(self):
        self.engine = QuizEngine(self.db)
        self.user_id = self.new_user()

    def test_quiz_has_ten_questions(self):
        self.assertEqual(len(self.engine.generate_quiz(self.user_id)), 10)

    def test_mixed_quiz_alternates_question_types(self):
        types = [q["type"] for q in self.engine.generate_quiz(self.user_id)]
        self.assertEqual(types[:4], ["FLASHCARD", "SIGN_IT", "FLASHCARD", "SIGN_IT"])

    def test_flashcard_choices_contain_the_answer(self):
        quiz = self.engine.generate_quiz(self.user_id, mode="FLASHCARD")
        for question in quiz:
            self.assertEqual(question["type"], "FLASHCARD")
            self.assertEqual(len(question["choices"]), 4)
            self.assertEqual(len(set(question["choices"])), 4)
            self.assertIn(question["correct_answer"], question["choices"])

    def test_sign_it_question_asks_for_the_letter(self):
        quiz = self.engine.generate_quiz(self.user_id, mode="SIGN_IT")
        for question in quiz:
            self.assertEqual(question["type"], "SIGN_IT")
            self.assertEqual(question["correct_answer"], question["letter"])
            self.assertIn(question["letter"], question["prompt"])

    def test_completed_quiz_without_lessons_is_empty(self):
        self.assertEqual(
            self.engine.generate_quiz_from_completed(self.user_id, []), []
        )

    def test_completed_quiz_only_uses_completed_lessons(self):
        quiz = self.engine.generate_quiz_from_completed(self.user_id, [1, 2, 3])
        self.assertEqual(len(quiz), 3)
        self.assertEqual({q["lesson_id"] for q in quiz}, {1, 2, 3})

    def test_perfect_quiz_gives_bonus_xp_and_badge(self):
        xp, bonus, _ = self.engine.complete_quiz(self.user_id, 10, 10, "MIXED")
        self.assertEqual((xp, bonus), (80, 30))
        self.assertEqual(self.db.get_user_by_id(self.user_id)["xp"], 80)
        self.assertIn("quiz_ace", self.db.get_unlocked_badges(self.user_id))

    def test_imperfect_quiz_gives_no_bonus(self):
        xp, bonus, _ = self.engine.complete_quiz(self.user_id, 7, 10, "MIXED")
        self.assertEqual((xp, bonus), (35, 0))
        self.assertNotIn("quiz_ace", self.db.get_unlocked_badges(self.user_id))

    def test_empty_quiz_gives_nothing(self):
        xp, bonus, _ = self.engine.complete_quiz(self.user_id, 0, 0, "MIXED")
        self.assertEqual((xp, bonus), (0, 0))


if __name__ == "__main__":
    unittest.main()
