"""퀴즈 게임의 기능 및 통합 흐름 테스트."""

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
    def test_check_answer(self):
        quiz = Quiz("질문", ["A", "B", "C", "D"], 2)
        self.assertTrue(quiz.check_answer(2))
        self.assertFalse(quiz.check_answer(1))

    def test_quiz_rejects_invalid_choice_count(self):
        with self.assertRaises(ValueError):
            Quiz("질문", ["A", "B", "C"], 1)


class QuizGameTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.state_path = self.root / "state.json"
        with redirect_stdout(StringIO()):
            self.game = QuizGame(self.state_path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_default_quiz_count_is_at_least_five_and_is_twelve(self):
        self.assertEqual(len(QuizGame.default_quizzes()), 12)
        self.assertGreaterEqual(len(self.game.quizzes), 5)

    def test_save_writes_schema_version_and_round_trips(self):
        self.game.best_score = 4
        self.game.best_total = 12
        self.assertTrue(self.game.save_data())
        saved = json.loads(self.state_path.read_text(encoding="utf-8"))
        self.assertEqual(saved["schema_version"], QuizGame.SCHEMA_VERSION)
        with redirect_stdout(StringIO()):
            loaded = QuizGame(self.state_path)
        self.assertEqual(len(loaded.quizzes), 12)
        self.assertEqual(loaded.best_score, 4)
        self.assertEqual(loaded.best_total, 12)

    def test_legacy_file_without_schema_version_is_migrated(self):
        legacy = {
            "quizzes": [self.game.quizzes[0].to_dict()],
            "best_score": 1,
            "best_total": 1,
        }
        self.state_path.write_text(json.dumps(legacy, ensure_ascii=False), encoding="utf-8")
        with redirect_stdout(StringIO()):
            loaded = QuizGame(self.state_path)
        migrated = json.loads(self.state_path.read_text(encoding="utf-8"))
        self.assertEqual(migrated["schema_version"], 1)
        self.assertEqual(len(loaded.quizzes), 1)
        self.assertTrue(loaded.backup_path.exists())

    def test_invalid_input_boundaries_retry_then_accept(self):
        output = StringIO()
        # blank, nonnumeric, below range, above range, then valid with whitespace
        with patch("builtins.input", side_effect=["", "abc", "0", "7", " 3 "]), redirect_stdout(output):
            value = QuizGame.input_number("선택: ", 1, 6)
        self.assertEqual(value, 3)
        rendered = output.getvalue()
        self.assertIn("입력이 비어 있습니다", rendered)
        self.assertIn("숫자로 입력해 주세요", rendered)
        self.assertIn("1부터 6 사이", rendered)

    def test_menu_integration_list_then_exit(self):
        output = StringIO()
        with patch("builtins.input", side_effect=["3", "5"]), redirect_stdout(output):
            self.game.run()
        self.assertIn("등록된 퀴즈 목록", output.getvalue())
        self.assertIn("저장 성공", output.getvalue())

    def test_backup_can_be_restored_after_a_later_save(self):
        self.assertTrue(self.game.save_data(create_backup=False))
        original_count = len(self.game.quizzes)
        self.game.quizzes.append(Quiz("임시 문제", ["가", "나", "다", "라"], 1))
        self.assertTrue(self.game.save_data())  # 이전 파일이 .bak에 보관됨
        self.assertEqual(len(self.game.quizzes), original_count + 1)
        with patch("builtins.input", return_value="1"), redirect_stdout(StringIO()):
            restored = self.game.restore_backup()
        self.assertTrue(restored)
        self.assertEqual(len(self.game.quizzes), original_count)

    def test_corrupt_file_falls_back_to_defaults(self):
        self.state_path.write_text("{깨진 JSON", encoding="utf-8")
        with redirect_stdout(StringIO()):
            recovered = QuizGame(self.state_path)
        self.assertEqual(len(recovered.quizzes), 12)
        saved = json.loads(self.state_path.read_text(encoding="utf-8"))
        self.assertEqual(len(saved["quizzes"]), 12)


if __name__ == "__main__":
    unittest.main()
