"""Quiz 및 QuizGame의 핵심 동작을 확인하는 표준 unittest."""

import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from quiz import Quiz
from quiz_game import QuizGame


class QuizTests(unittest.TestCase):
    def test_quiz_answer_and_serialization(self):
        quiz = Quiz("문제", ["가", "나", "다", "라"], 2, "해설")
        self.assertTrue(quiz.check_answer(2))
        self.assertFalse(quiz.check_answer(1))
        restored = Quiz.from_dict(quiz.to_dict())
        self.assertEqual(restored.question, "문제")
        self.assertEqual(restored.answer, 2)

    def test_quiz_rejects_invalid_answer(self):
        with self.assertRaises(ValueError):
            Quiz("문제", ["가", "나", "다", "라"], 5)


class QuizGameTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.state_path = Path(self.temp_dir.name) / "state.json"

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_missing_state_creates_default_quizzes(self):
        with redirect_stdout(StringIO()):
            game = QuizGame(self.state_path)
        self.assertGreaterEqual(len(game.quizzes), 5)
        self.assertTrue(self.state_path.exists())
        data = json.loads(self.state_path.read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(data["quizzes"]), 5)

    def test_added_quiz_is_persisted(self):
        with redirect_stdout(StringIO()):
            game = QuizGame(self.state_path)
        game.quizzes.append(Quiz("추가 문제", ["1", "2", "3", "4"], 4))
        self.assertTrue(game.save_data())
        with redirect_stdout(StringIO()):
            reloaded = QuizGame(self.state_path)
        self.assertEqual(reloaded.quizzes[-1].question, "추가 문제")

    def test_corrupt_json_recovers_to_defaults(self):
        self.state_path.write_text("{broken json", encoding="utf-8")
        with redirect_stdout(StringIO()):
            game = QuizGame(self.state_path)
        self.assertGreaterEqual(len(game.quizzes), 5)
        self.assertIsNone(game.best_score)
        json.loads(self.state_path.read_text(encoding="utf-8"))

    def test_invalid_quiz_entry_is_skipped(self):
        data = {
            "quizzes": [
                {"question": "정상 문제", "choices": ["가", "나", "다", "라"], "answer": 1},
                {"question": "잘못된 문제", "choices": ["하나"], "answer": 9},
            ],
            "best_score": 1,
            "best_total": 1,
        }
        self.state_path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        with redirect_stdout(StringIO()):
            game = QuizGame(self.state_path)
        self.assertEqual(len(game.quizzes), 1)
        self.assertEqual(game.quizzes[0].question, "정상 문제")

    def test_empty_question_and_choice_are_rejected(self):
        with self.assertRaises(ValueError):
            Quiz("   ", ["가", "나", "다", "라"], 1)
        with self.assertRaises(ValueError):
            Quiz("문제", ["가", "", "다", "라"], 1)

    def test_invalid_menu_inputs_return_to_prompt(self):
        with redirect_stdout(StringIO()) as output:
            game = QuizGame(self.state_path)
            with patch("builtins.input", side_effect=["abc", "9", "", " 5 "]):
                game.run()
        message = output.getvalue()
        self.assertIn("숫자로 입력", message)
        self.assertIn("사이의 숫자", message)
        self.assertIn("비어 있습니다", message)
        self.assertIn("종료합니다", message)


if __name__ == "__main__":
    unittest.main()
