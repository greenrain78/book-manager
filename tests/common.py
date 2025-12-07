import unittest


class CommonTestMixin(unittest.TestCase):
    def run_prompt_test(func, inputs, expected_messages):
        with patch("builtins.input", side_effect=inputs), \
             patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            func()

        out = mock_stdout.getvalue()
        for msg in expected_messages:
            self.assertIn(msg, out)


import os
import io
import unittest
import tempfile
from unittest.mock import patch

from src.context import AppContext
from src.prompt.user import borrow_prompt
from src.service.book_service import BookService
from src.service.borrow_service import BorrowService


class PromptTestBase(unittest.TestCase):
    ENABLE_FILE_PRINT = True   # 확인용 출력 ON/OFF

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        base = self.tmpdir.name

        # 테스트 파일 경로
        self.paths = {
            "users": os.path.join(base, "users.txt"),
            "books": os.path.join(base, "books.txt"),
            "isbn": os.path.join(base, "isbn.txt"),
            "cats": os.path.join(base, "categories.txt"),
            "borrow": os.path.join(base, "borrow.txt"),
            "borrow_hist": os.path.join(base, "borrow_history.txt"),
        }

    def write_files(self, file_data):
        for key, lines in file_data.items():
            with open(self.paths[key], "w") as f:
                for line in lines:
                    f.write(line + "\n")

    def read_file(self, key):
        with open(self.paths[key], "r") as f:
            return f.read()

    # borrow_prompt 실행 전 AppContext + Service 설정
    def prepare_test_context(self, file_data, current_user, current_date):
        # 테스트용 파일 작성
        self.write_files(file_data)
        # patch context 생성을 테스트 객체에 저장
        self.patches = [
            patch("src.context.USER_DATA_PATH", self.paths["users"]),
            patch("src.context.BOOK_DATA_PATH", self.paths["books"]),
            patch("src.context.BORROW_DATA_PATH", self.paths["borrow"]),
            patch("src.context.BORROW_HISTORY_DATA_PATH", self.paths["borrow_hist"]),
            patch("src.context.ISBN_DATA_PATH", self.paths["isbn"]),
            patch("src.context.CATEGORY_DATA_PATH", self.paths["cats"]),
        ]
        self.active_patches = [p.start() for p in self.patches]

        # AppContext 생성 및 현재 사용자/날짜 설정
        app = AppContext()
        app.set_current_user(current_user)
        app.set_current_date(current_date)
        return app

    # borrow_prompt 실행 + 출력 캡처
    @staticmethod
    def execute_prompt(input_values, func, *args, **kwargs):
        with patch("builtins.input", side_effect=input_values):
            buffer = io.StringIO()
            with patch("sys.stdout", buffer):
                func(*args, **kwargs)
        return buffer.getvalue()  # 출력 문자열 반환

    # borrow_prompt 실행 후 파일/출력 검증
    def assert_after_prompt(self, output, expected_output_keywords,
                            file_expect_contains=None,
                            file_expect_not_contains=None):
        # 출력 검사
        for word in expected_output_keywords:
            self.assertIn(word, output)
        # 파일 포함 검사
        if file_expect_contains:
            for key, words in file_expect_contains.items():
                content = self.read_file(key)
                for word in words:
                    self.assertIn(word, content, f"{key}.txt must contain '{word}'")

        # 파일 미포함 검사
        if file_expect_not_contains:
            for key, words in file_expect_not_contains.items():
                content = self.read_file(key)
                for word in words:
                    self.assertNotIn(word, content, f"{key}.txt must NOT contain '{word}'")

        # 디버그용 파일 출력
        if not self.ENABLE_FILE_PRINT:
            return
        print("\n====== Final Files in Temp Directory ======")
        for key, path in self.paths.items():
            print(f"\n--- {key}.txt ---")
            if os.path.exists(path):
                with open(path, "r") as f:
                    content = f.read().strip()
                    print(content if content else "(empty)")
            else:
                print("(file missing)")
        print("==========================================\n")


    def tearDown(self):
        for p in self.patches:
            p.stop()
