
import unittest
from io import StringIO
from unittest.mock import patch

from src.prompt.menu import admin_prompt
from src.prompt.user import user_prompt, search_prompt


class TestUserPrompt(unittest.TestCase):
    @patch("builtins.input", return_value="1") # 정상 입력 - 기본 케이스
    @patch("sys.stdout", new_callable=StringIO)
    def test_book_search_prompt_a1(self, mock_stdout, mock_input):
        # 가장 기본적인 테스트 케이스
        result = user_prompt()
        self.assertIn("UserPrompt", mock_stdout.getvalue())
        self.assertIn("1. 검색", mock_stdout.getvalue())
        self.assertIn("2. 대출", mock_stdout.getvalue())
        self.assertIn("3. 반납", mock_stdout.getvalue())
        self.assertIn("4. 로그아웃", mock_stdout.getvalue())

        # result 값이 PromptType.SEARCH_MENU 인지 확인
        self.assertEqual(result.name, "SEARCH_MENU")


    @patch("builtins.input", return_value="2")
    @patch("sys.stdout", new_callable=StringIO)
    def test_book_borrow_prompt_2(self, mock_stdout, mock_input):
        result = user_prompt()
        self.assertEqual(result.name, "BOOK_BORROW")

    @patch("builtins.input", return_value="3")
    @patch("sys.stdout", new_callable=StringIO)
    def test_book_borrow_prompt_3(self, mock_stdout, mock_input):
        result = user_prompt()
        self.assertEqual(result.name, "BOOK_RETURN")

    @patch("builtins.input", side_effect=["4", "Y"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_user_logout_prompt_4(self, mock_stdout, mock_input):
        result = user_prompt()
        self.assertEqual(result.name, "LOGOUT")

# ====================================================================
    @patch("builtins.input", return_value=" 1") # 앞에 공백 포함 - 정상 입력
    @patch("sys.stdout", new_callable=StringIO)
    def test_book_search_prompt_b1(self, mock_stdout, mock_input):
        result = user_prompt()
        self.assertIn("UserPrompt", mock_stdout.getvalue()) # 정상 출력 확인
        self.assertEqual(result.name, "SEARCH_MENU")  # 기능 호출 확인

    @patch("builtins.input", return_value="1 ")  # 뒤에 공백 포함 - 정상 입력
    @patch("sys.stdout", new_callable=StringIO)
    def test_book_search_prompt_b2(self, mock_stdout, mock_input):
        result = user_prompt()
        self.assertIn("UserPrompt", mock_stdout.getvalue())  # 정상 출력 확인
        self.assertEqual(result.name, "SEARCH_MENU")  # 기능 호출 확인

    @patch("builtins.input", return_value=" 1 ")  # 앞뒤에 공백 포함 - 정상 입력
    @patch("sys.stdout", new_callable=StringIO)
    def test_book_search_prompt_b3(self, mock_stdout, mock_input):
        result = user_prompt()
        self.assertIn("UserPrompt", mock_stdout.getvalue())  # 정상 출력 확인
        self.assertEqual(result.name, "SEARCH_MENU")  # 기능 호출 확인

# ====================================================================

    @patch("builtins.input", side_effect=["11", "1"]) # 잘못된 입력(11) 후 올바른 입력
    @patch("sys.stdout", new_callable=StringIO)
    def test_book_search_prompt_c1(self, mock_stdout, mock_input):
        result = user_prompt()
        self.assertIn("UserPrompt", mock_stdout.getvalue())  # 정상 출력 확인
        self.assertIn("잘못된 입력입니다!! 1,2,3,4 중 하나를 입력하세요.", mock_stdout.getvalue())  # 오류 메시지 확인
        self.assertEqual(result.name, "SEARCH_MENU")  # 기능 호출 확인

    @patch("builtins.input", side_effect=["01", "1"]) # 잘못된 입력(01) 후 올바른 입력
    @patch("sys.stdout", new_callable=StringIO)
    def test_book_search_prompt_c2(self, mock_stdout, mock_input):
        result = user_prompt()
        self.assertIn("UserPrompt", mock_stdout.getvalue())  # 정상 출력 확인
        self.assertIn("잘못된 입력입니다!! 1,2,3,4 중 하나를 입력하세요.", mock_stdout.getvalue())  # 오류 메시지 확인
        self.assertEqual(result.name, "SEARCH_MENU")  # 기능 호출 확인


    @patch("builtins.input", side_effect=["0", "1"]) # 잘못된 입력(0) 후 올바른 입력
    @patch("sys.stdout", new_callable=StringIO)
    def test_book_search_prompt_c3(self, mock_stdout, mock_input):
        result = user_prompt()
        self.assertIn("UserPrompt", mock_stdout.getvalue())  # 정상 출력 확인
        self.assertIn("잘못된 입력입니다!! 1,2,3,4 중 하나를 입력하세요.", mock_stdout.getvalue())  # 오류 메시지 확인
        self.assertEqual(result.name, "SEARCH_MENU")  # 기능 호출 확인

    @patch("builtins.input", side_effect=["5", "1"])  # 잘못된 입력(5) 후 올바른 입력
    @patch("sys.stdout", new_callable=StringIO)
    def test_book_search_prompt_c4(self, mock_stdout, mock_input):
        result = user_prompt()
        self.assertIn("UserPrompt", mock_stdout.getvalue())  # 정상 출력 확인
        self.assertIn("잘못된 입력입니다!! 1,2,3,4 중 하나를 입력하세요.", mock_stdout.getvalue())  # 오류 메시지 확인
        self.assertEqual(result.name, "SEARCH_MENU")  # 기능 호출 확인
        
    @patch("builtins.input", side_effect=["-1", "1"])  # 잘못된 입력(-1) 후 올바른 입력
    @patch("sys.stdout", new_callable=StringIO)
    def test_book_search_prompt_c5(self, mock_stdout, mock_input):
        result = user_prompt()
        self.assertIn("UserPrompt", mock_stdout.getvalue())  # 정상 출력 확인
        self.assertIn("잘못된 입력입니다!! 1,2,3,4 중 하나를 입력하세요.", mock_stdout.getvalue())  # 오류 메시지 확인
        self.assertEqual(result.name, "SEARCH_MENU")  # 기능 호출 확인

    @patch("builtins.input", side_effect=["!", "1"])  # 잘못된 입력(!) 후 올바른 입력
    @patch("sys.stdout", new_callable=StringIO)
    def test_book_search_prompt_c6(self, mock_stdout, mock_input):
        result = user_prompt()
        self.assertIn("UserPrompt", mock_stdout.getvalue())  # 정상 출력 확인
        self.assertIn("잘못된 입력입니다!! 1,2,3,4 중 하나를 입력하세요.", mock_stdout.getvalue())  # 오류 메시지 확인
        self.assertEqual(result.name, "SEARCH_MENU")  # 기능 호출 확인

    @patch("builtins.input", side_effect=["1.0", "1"])  # 잘못된 입력(1.0) 입력후 올바른 입력
    @patch("sys.stdout", new_callable=StringIO)
    def test_book_search_prompt_c6_1(self, mock_stdout, mock_input):
        result = user_prompt()
        self.assertIn("UserPrompt", mock_stdout.getvalue())  # 정상 출력 확인
        self.assertIn("잘못된 입력입니다!! 1,2,3,4 중 하나를 입력하세요.", mock_stdout.getvalue())  # 오류 메시지 확인
        self.assertEqual(result.name, "SEARCH_MENU")  # 기능 호출 확인

    @patch("builtins.input", side_effect=["exit", "1"])  # 잘못된 입력(exit) 후 올바른 입력
    @patch("sys.stdout", new_callable=StringIO)
    def test_book_search_prompt_c6_2(self, mock_stdout, mock_input):
        result = user_prompt()
        self.assertIn("UserPrompt", mock_stdout.getvalue())  # 정상 출력 확인
        self.assertIn("잘못된 입력입니다!! 1,2,3,4 중 하나를 입력하세요.", mock_stdout.getvalue())  # 오류 메시지 확인
        self.assertEqual(result.name, "SEARCH_MENU")  # 기능 호출 확인

    @patch("builtins.input", side_effect=[" ", "1"])  # 잘못된 입력=(빈 문자열) 입력후 올바른 입력
    @patch("sys.stdout", new_callable=StringIO)
    def test_book_search_prompt_c6_3(self, mock_stdout, mock_input):
        result = user_prompt()
        self.assertIn("UserPrompt", mock_stdout.getvalue())  # 정상 출력 확인
        self.assertIn("잘못된 입력입니다!! 1,2,3,4 중 하나를 입력하세요.", mock_stdout.getvalue())  # 오류 메시지 확인
        self.assertEqual(result.name, "SEARCH_MENU")  # 기능 호출 확인



class TestSearchPrompt(unittest.TestCase):
    @patch("builtins.input", return_value="1") # 정상 입력 - 기본 케이스
    @patch("sys.stdout", new_callable=StringIO)
    def test_search_prompt_a1(self, mock_stdout, mock_input):
        # 가장 기본적인 테스트 케이스
        result = search_prompt()
        self.assertIn("검색하고 싶은 종류를 골라주세요.", mock_stdout.getvalue())
        self.assertIn("1. 도서 검색", mock_stdout.getvalue())
        self.assertIn("2. 카테고리 검색", mock_stdout.getvalue())

        self.assertEqual(result.name, "SEARCH_BOOK")

    @patch("builtins.input", return_value="2")
    @patch("sys.stdout", new_callable=StringIO)
    def test_search_prompt_a2(self, mock_stdout, mock_input):
        result = search_prompt()
        self.assertEqual(result.name, "SEARCH_CATEGORY")

    @patch("builtins.input", return_value=" 1") # 앞에 공백 포함 - 정상 입력
    @patch("sys.stdout", new_callable=StringIO)
    def test_search_prompt_b1(self, mock_stdout, mock_input):
        result = search_prompt()
        self.assertIn("검색하고 싶은 종류를 골라주세요.", mock_stdout.getvalue()) # 정상 출력 확인
        self.assertEqual(result.name, "SEARCH_BOOK")  # 기능 호출 확인

    @patch("builtins.input", return_value="1 ")  # 뒤에 공백 포함 - 정상 입력
    @patch("sys.stdout", new_callable=StringIO)
    def test_search_prompt_b2(self, mock_stdout, mock_input):
        result = search_prompt()
        self.assertIn("검색하고 싶은 종류를 골라주세요.", mock_stdout.getvalue())  # 정상 출력 확인
        self.assertEqual(result.name, "SEARCH_BOOK")  # 기능 호출 확인

    @patch("builtins.input", return_value=" 1 ")  # 앞뒤에 공백 포함 - 정상 입력
    @patch("sys.stdout", new_callable=StringIO)
    def test_search_prompt_b3(self, mock_stdout, mock_input):
        result = search_prompt()
        self.assertIn("검색하고 싶은 종류를 골라주세요.", mock_stdout.getvalue())  # 정상 출력 확인
        self.assertEqual(result.name, "SEARCH_BOOK")  # 기능 호출 확인

    @patch("builtins.input", side_effect=["3", "1"]) # 잘못된 입력(3) 후 올바른 입력
    @patch("sys.stdout", new_callable=StringIO)
    def test_search_prompt_c1(self, mock_stdout, mock_input):
        result = search_prompt()
        self.assertIn("검색하고 싶은 종류를 골라주세요.", mock_stdout.getvalue())
        self.assertIn("잘못된 입력입니다!! 1,2 중 하나를 입력하세요.", mock_stdout.getvalue())
        self.assertEqual(result.name, "SEARCH_BOOK")  # 기능 호출 확인

    @patch("builtins.input", side_effect=["0", "1"]) # 잘못된 입력(0) 후 올바른 입력
    @patch("sys.stdout", new_callable=StringIO)
    def test_search_prompt_c2(self, mock_stdout, mock_input):
        result = search_prompt()
        self.assertIn("검색하고 싶은 종류를 골라주세요.", mock_stdout.getvalue())
        self.assertIn("잘못된 입력입니다!! 1,2 중 하나를 입력하세요.", mock_stdout.getvalue())
        self.assertEqual(result.name, "SEARCH_BOOK")  # 기능 호출 확인

    @patch("builtins.input", side_effect=["-1", "1"])  # 잘못된 입력(-1) 후 올바른 입력
    @patch("sys.stdout", new_callable=StringIO)
    def test_search_prompt_c3(self, mock_stdout, mock_input):
        result = search_prompt()
        self.assertIn("검색하고 싶은 종류를 골라주세요.", mock_stdout.getvalue())
        self.assertIn("잘못된 입력입니다!! 1,2 중 하나를 입력하세요.", mock_stdout.getvalue())
        self.assertEqual(result.name, "SEARCH_BOOK")  # 기능 호출 확인

    @patch("builtins.input", side_effect=["!", "1"])  # 잘못된 입력(!) 후 올바른 입력
    @patch("sys.stdout", new_callable=StringIO)
    def test_search_prompt_c4(self, mock_stdout, mock_input):
        result = search_prompt()
        self.assertIn("검색하고 싶은 종류를 골라주세요.", mock_stdout.getvalue())
        self.assertIn("잘못된 입력입니다!! 1,2 중 하나를 입력하세요.", mock_stdout.getvalue())
        self.assertEqual(result.name, "SEARCH_BOOK")  # 기능 호출 확인

    @patch("builtins.input", side_effect=["1.0", "1"])  # 잘못된 입력(1.0) 입력후 올바른 입력
    @patch("sys.stdout", new_callable=StringIO)
    def test_search_prompt_c5(self, mock_stdout, mock_input):
        result = search_prompt()
        self.assertIn("검색하고 싶은 종류를 골라주세요.", mock_stdout.getvalue())
        self.assertIn("잘못된 입력입니다!! 1,2 중 하나를 입력하세요.", mock_stdout.getvalue())
        self.assertEqual(result.name, "SEARCH_BOOK")  # 기능 호출 확인

    @patch("builtins.input", side_effect=["exit", "1"])  # 잘못된 입력(exit) 후 올바른 입력
    @patch("sys.stdout", new_callable=StringIO)
    def test_search_prompt_c6(self, mock_stdout, mock_input):
        result = search_prompt()
        self.assertIn("검색하고 싶은 종류를 골라주세요.", mock_stdout.getvalue())
        self.assertIn("잘못된 입력입니다!! 1,2 중 하나를 입력하세요.", mock_stdout.getvalue())
        self.assertEqual(result.name, "SEARCH_BOOK")  # 기능 호출 확인

    @patch("builtins.input", side_effect=[" ", "1"])  # 잘못된 입력=(빈 문자열) 입력후 올바른 입력
    @patch("sys.stdout", new_callable=StringIO)
    def test_search_prompt_c7(self, mock_stdout, mock_input):
        result = search_prompt()
        self.assertIn("검색하고 싶은 종류를 골라주세요.", mock_stdout.getvalue())
        self.assertIn("잘못된 입력입니다!! 1,2 중 하나를 입력하세요.", mock_stdout.getvalue())
        self.assertEqual(result.name, "SEARCH_BOOK")  # 기능 호출 확인



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
