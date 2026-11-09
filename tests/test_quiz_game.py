"""퀴즈 게임 자동 테스트 (표준 라이브러리 unittest 사용)

실행 방법 (프로젝트 루트에서):
    python -m unittest discover -s tests -v
"""

import builtins
import contextlib
import io
import json
import os
import shutil
import sys
import tempfile
import time
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import main  # noqa: E402


def quiet(func, *args):
    """화면 출력을 숨기고 함수를 실행한 뒤 (결과, 출력 문자열)을 돌려준다"""
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        result = func(*args)
    return result, buffer.getvalue()


class FakeInput:
    """input()을 대신해 미리 정한 값을 차례대로 돌려준다"""

    def __init__(self, values):
        self.values = list(values)

    def __call__(self, prompt=""):
        return self.values.pop(0)


class QuizTest(unittest.TestCase):
    """Quiz 클래스 테스트"""

    def test_is_correct(self):
        quiz = main.Quiz("문제", ["a", "b", "c", "d"], 2)
        self.assertTrue(quiz.is_correct(2))
        self.assertFalse(quiz.is_correct(1))

    def test_to_dict_includes_all_fields(self):
        quiz = main.Quiz("문제", ["a", "b", "c", "d"], 3, "힌트")
        self.assertEqual(
            quiz.to_dict(),
            {"question": "문제", "choices": ["a", "b", "c", "d"], "answer": 3, "hint": "힌트"},
        )

    def test_default_quizzes(self):
        quizzes = main.create_default_quizzes()
        self.assertGreaterEqual(len(quizzes), 5)
        for quiz in quizzes:
            self.assertEqual(len(quiz.choices), 4)
            self.assertIn(quiz.answer, [1, 2, 3, 4])


class QuizGameFileTest(unittest.TestCase):
    """저장 / 불러오기 / 백업 / 복구 테스트 (임시 폴더 사용)"""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.original_state = main.STATE_FILE
        main.STATE_FILE = os.path.join(self.temp_dir, "state.json")

    def tearDown(self):
        main.STATE_FILE = self.original_state
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_no_file_uses_default_quizzes(self):
        game, output = quiet(main.QuizGame)
        self.assertEqual(len(game.quizzes), 5)
        self.assertIsNone(game.best_score)
        self.assertIn("기본 퀴즈", output)

    def test_save_and_load_round_trip(self):
        game, _ = quiet(main.QuizGame)
        game.quizzes.append(main.Quiz("새 문제", ["1", "2", "3", "4"], 4, "힌트"))
        game.best_score = 80
        game.history.append({"date": "2026-11-09 10:00", "total": 3, "correct": 2, "score": 66, "hints": 0})
        quiet(game.save_data)

        with open(main.STATE_FILE, encoding="utf-8") as file:
            self.assertIn("새 문제", file.read())  # 한글이 그대로 저장되는지 (UTF-8)

        loaded, _ = quiet(main.QuizGame)
        self.assertEqual(len(loaded.quizzes), 6)
        self.assertEqual(loaded.quizzes[-1].hint, "힌트")
        self.assertEqual(loaded.best_score, 80)
        self.assertEqual(len(loaded.history), 1)

    def test_old_file_without_hint_and_history(self):
        data = {"quizzes": [{"question": "옛날 문제", "choices": ["a", "b", "c", "d"], "answer": 1}],
                "best_score": 50}
        with open(main.STATE_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False)
        game, _ = quiet(main.QuizGame)
        self.assertEqual(game.quizzes[0].hint, "")
        self.assertEqual(game.history, [])

    def test_backup_created_on_save(self):
        game, _ = quiet(main.QuizGame)
        quiet(game.save_data)  # 첫 저장: state.json 생성
        quiet(game.save_data)  # 두 번째 저장: 이전 파일을 .bak으로 백업
        self.assertTrue(os.path.exists(main.get_backup_file()))

    def test_corrupted_file_restored_from_backup(self):
        game, _ = quiet(main.QuizGame)
        game.quizzes.append(main.Quiz("백업될 문제", ["a", "b", "c", "d"], 1))
        quiet(game.save_data)
        quiet(game.save_data)  # 6개짜리 상태가 .bak에도 남음
        with open(main.STATE_FILE, "w", encoding="utf-8") as file:
            file.write("{ 손상")
        restored, output = quiet(main.QuizGame)
        self.assertIn("백업 파일에서 복구", output)
        self.assertEqual(len(restored.quizzes), 6)

    def test_corrupted_file_and_backup_use_default(self):
        for path in (main.STATE_FILE, main.get_backup_file()):
            with open(path, "w", encoding="utf-8") as file:
                file.write("깨진 파일")
        game, output = quiet(main.QuizGame)
        self.assertIn("기본 퀴즈로 복구", output)
        self.assertEqual(len(game.quizzes), 5)

    def test_1000_quizzes_save_and_load_fast(self):
        game, _ = quiet(main.QuizGame)
        game.quizzes = [main.Quiz(f"문제 {i}", ["a", "b", "c", "d"], 1) for i in range(1000)]
        start = time.perf_counter()
        quiet(game.save_data)
        loaded, _ = quiet(main.QuizGame)
        elapsed = time.perf_counter() - start
        self.assertEqual(len(loaded.quizzes), 1000)
        self.assertLess(elapsed, 1.0)  # 1,000개 저장 + 불러오기가 1초 안에 끝나야 함


class InputValidationTest(unittest.TestCase):
    """입력 검증 테스트"""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.original_state = main.STATE_FILE
        main.STATE_FILE = os.path.join(self.temp_dir, "state.json")
        self.game, _ = quiet(main.QuizGame)
        self.original_input = builtins.input

    def tearDown(self):
        builtins.input = self.original_input
        main.STATE_FILE = self.original_state
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_get_number_retries_until_valid(self):
        # 빈 입력, 글자, 범위 밖 숫자는 다시 묻고, 앞뒤 공백은 제거
        builtins.input = FakeInput(["", "abc", "9", "0", "  3  "])
        number, output = quiet(self.game.get_number, "선택: ", 1, 5)
        self.assertEqual(number, 3)
        self.assertEqual(output.count("⚠️"), 4)

    def test_get_text_rejects_empty(self):
        builtins.input = FakeInput(["", "   ", "내용"])
        text, output = quiet(self.game.get_text, "문제: ")
        self.assertEqual(text, "내용")
        self.assertEqual(output.count("⚠️"), 2)

    def test_play_quiz_with_no_quizzes(self):
        self.game.quizzes = []
        _, output = quiet(self.game.play_quiz)
        self.assertIn("등록된 퀴즈가 없습니다", output)

    def test_play_quiz_score_and_hint(self):
        self.game.quizzes = [main.Quiz("문제", ["a", "b", "c", "d"], 2, "힌트")]
        self.game.best_score = None
        builtins.input = FakeInput(["1", "0", "2"])  # 1문제, 힌트 보기, 정답 2
        _, output = quiet(self.game.play_quiz)
        self.assertIn("💡 힌트: 힌트", output)
        self.assertEqual(self.game.best_score, 50)  # 힌트를 보고 맞히면 0.5점 → 50점
        self.assertEqual(self.game.history[-1]["hints"], 1)

    def test_keyboard_interrupt_saves_and_exits(self):
        def raise_interrupt(prompt=""):
            raise KeyboardInterrupt
        builtins.input = raise_interrupt
        _, output = quiet(main.main)
        self.assertIn("안전하게 종료", output)
        self.assertTrue(os.path.exists(main.STATE_FILE))


if __name__ == "__main__":
    unittest.main()
