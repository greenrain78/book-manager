import unittest
from io import StringIO
from unittest.mock import patch

from src.prompt.menu import admin_prompt

class TestAdminPrompt(unittest.TestCase):

    # ============================================================
    # 정상 입력 케이스
    # ============================================================
    @patch("builtins.input", return_value="1")
    @patch("sys.stdout", new_callable=StringIO)
    def test_admin_prompt_a1(self, mock_stdout, mock_input):
        result = admin_prompt()
        self.assertIn("Admin", mock_stdout.getvalue())
        self.assertIn("1. 도서 추가", mock_stdout.getvalue())
        self.assertIn("2. 도서 삭제", mock_stdout.getvalue())
        self.assertIn("3. 도서 수정", mock_stdout.getvalue())
        self.assertIn("4. 카테고리 관리", mock_stdout.getvalue())
        self.assertIn("5. 로그아웃", mock_stdout.getvalue())
        self.assertEqual(result.name, "ADMIN_BOOK_ADD")

    @patch("builtins.input", return_value="2")
    @patch("sys.stdout", new_callable=StringIO)
    def test_admin_prompt_a2(self, mock_stdout, mock_input):
        result = admin_prompt()
        self.assertEqual(result.name, "ADMIN_BOOK_DELETE")

    @patch("builtins.input", return_value="3")
    @patch("sys.stdout", new_callable=StringIO)
    def test_admin_prompt_a3(self, mock_stdout, mock_input):
        result = admin_prompt()
        self.assertEqual(result.name, "ADMIN_BOOK_MODIFY")

    @patch("builtins.input", return_value="4")
    @patch("sys.stdout", new_callable=StringIO)
    def test_admin_prompt_a4(self, mock_stdout, mock_input):
        result = admin_prompt()
        self.assertEqual(result.name, "CATEGORY_MENU")


    # ============================================================
    # 로그아웃(Y 처리)
    # ============================================================
    @patch("builtins.input", side_effect=["5", "Y"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_admin_prompt_logout_y(self, mock_stdout, mock_input):
        result = admin_prompt()
        self.assertEqual(result.name, "LOGOUT")

    # 로그아웃(N 처리 → 다시 명령 선택으로 돌아감)
    @patch("builtins.input", side_effect=["5", "N", "1"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_admin_prompt_logout_n(self, mock_stdout, mock_input):
        result = admin_prompt()
        self.assertEqual(result.name, "ADMIN_BOOK_ADD")


    # ============================================================
    # 공백 포함 입력 → 정상 처리 (strip() 적용 확인)
    # ============================================================
    @patch("builtins.input", return_value=" 1")
    @patch("sys.stdout", new_callable=StringIO)
    def test_admin_prompt_b1(self, mock_stdout, mock_input):
        result = admin_prompt()
        self.assertEqual(result.name, "ADMIN_BOOK_ADD")

    @patch("builtins.input", return_value="1 ")
    @patch("sys.stdout", new_callable=StringIO)
    def test_admin_prompt_b2(self, mock_stdout, mock_input):
        result = admin_prompt()
        self.assertEqual(result.name, "ADMIN_BOOK_ADD")

    @patch("builtins.input", return_value=" 1 ")
    @patch("sys.stdout", new_callable=StringIO)
    def test_admin_prompt_b3(self, mock_stdout, mock_input):
        result = admin_prompt()
        self.assertEqual(result.name, "ADMIN_BOOK_ADD")


    # ============================================================
    # 잘못된 입력 후 정상 입력
    # ============================================================
    @patch("builtins.input", side_effect=["0", "1"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_admin_prompt_c1(self, mock_stdout, mock_input):
        result = admin_prompt()
        self.assertIn("입력에 해당하는 명령어가 없습니다.", mock_stdout.getvalue())
        self.assertEqual(result.name, "ADMIN_BOOK_ADD")

    @patch("builtins.input", side_effect=["11", "1"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_admin_prompt_c2(self, mock_stdout, mock_input):
        result = admin_prompt()
        self.assertIn("입력에 해당하는 명령어가 없습니다.", mock_stdout.getvalue())
        self.assertEqual(result.name, "ADMIN_BOOK_ADD")

    @patch("builtins.input", side_effect=["!", "1"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_admin_prompt_c3(self, mock_stdout, mock_input):
        result = admin_prompt()
        self.assertIn("입력에 해당하는 명령어가 없습니다.", mock_stdout.getvalue())
        self.assertEqual(result.name, "ADMIN_BOOK_ADD")

    @patch("builtins.input", side_effect=["1.0", "1"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_admin_prompt_c4(self, mock_stdout, mock_input):
        result = admin_prompt()
        self.assertIn("입력에 해당하는 명령어가 없습니다.", mock_stdout.getvalue())
        self.assertEqual(result.name, "ADMIN_BOOK_ADD")

    @patch("builtins.input", side_effect=[" ", "1"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_admin_prompt_c5(self, mock_stdout, mock_input):
        result = admin_prompt()
        self.assertIn("입력에 해당하는 명령어가 없습니다.", mock_stdout.getvalue())
        self.assertEqual(result.name, "ADMIN_BOOK_ADD")

    @patch("builtins.input", side_effect=["exit", "1"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_admin_prompt_c6(self, mock_stdout, mock_input):
        result = admin_prompt()
        self.assertIn("입력에 해당하는 명령어가 없습니다.", mock_stdout.getvalue())
        self.assertEqual(result.name, "ADMIN_BOOK_ADD")
