
import unittest
from io import StringIO
from unittest.mock import patch

from src.controller import SearchController
from src.prompt.user import search_prompt


class TestSearchPrompt(unittest.TestCase):

    def setUp(self):
        class FakeController(SearchController):
            def __init__(self):
                super().__init__(app=None)
            def search(self):
                print("Search called")
            def search_by_category(self):
                print("Search by category called")
        self.controller = FakeController()

    @patch("builtins.input", return_value="1") # 정상 입력 - 기본 케이스
    @patch("sys.stdout", new_callable=StringIO)
    def test_search_prompt_a1(self, mock_stdout, mock_input):
        # 가장 기본적인 테스트 케이스
        search_prompt(controller=self.controller)
        self.assertIn("검색하고 싶은 종류를 골라주세요.", mock_stdout.getvalue())
        self.assertIn("1. 도서 검색", mock_stdout.getvalue())
        self.assertIn("2. 카테고리 검색", mock_stdout.getvalue())

        self.assertIn("Search called", mock_stdout.getvalue())

    @patch("builtins.input", return_value="2")
    @patch("sys.stdout", new_callable=StringIO)
    def test_search_prompt_a2(self, mock_stdout, mock_input):
        search_prompt(controller=self.controller)
        self.assertIn("Search by category called", mock_stdout.getvalue())

    @patch("builtins.input", return_value=" 1") # 앞에 공백 포함 - 정상 입력
    @patch("sys.stdout", new_callable=StringIO)
    def test_search_prompt_b1(self, mock_stdout, mock_input):
        search_prompt(controller=self.controller)
        self.assertIn("검색하고 싶은 종류를 골라주세요.", mock_stdout.getvalue()) # 정상 출력 확인
        self.assertIn("Search called", mock_stdout.getvalue()) # 기능
        self.assertIn("Search called", mock_stdout.getvalue()) # 기능 호출 확인

    @patch("builtins.input", return_value="1 ")  # 뒤에 공백 포함 - 정상 입력
    @patch("sys.stdout", new_callable=StringIO)
    def test_search_prompt_b2(self, mock_stdout, mock_input):
        search_prompt(controller=self.controller)
        self.assertIn("검색하고 싶은 종류를 골라주세요.", mock_stdout.getvalue())
        self.assertIn("Search called", mock_stdout.getvalue())

    @patch("builtins.input", return_value=" 1 ")  # 앞뒤에 공백 포함 - 정상 입력
    @patch("sys.stdout", new_callable=StringIO)
    def test_search_prompt_b3(self, mock_stdout, mock_input):
        search_prompt(controller=self.controller)
        self.assertIn("검색하고 싶은 종류를 골라주세요.", mock_stdout.getvalue())
        self.assertIn("Search called", mock_stdout.getvalue())

    @patch("builtins.input", side_effect=["3", "1"]) # 잘못된 입력(3) 후 올바른 입력
    @patch("sys.stdout", new_callable=StringIO)
    def test_search_prompt_c1(self, mock_stdout, mock_input):
        search_prompt(controller=self.controller)
        self.assertIn("검색하고 싶은 종류를 골라주세요.", mock_stdout.getvalue())
        self.assertIn("잘못된 입력입니다!! 1,2 중 하나를 입력하세요.", mock_stdout.getvalue())

    @patch("builtins.input", side_effect=["0", "1"]) # 잘못된 입력(0) 후 올바른 입력
    @patch("sys.stdout", new_callable=StringIO)
    def test_search_prompt_c2(self, mock_stdout, mock_input):
        search_prompt(controller=self.controller)
        self.assertIn("검색하고 싶은 종류를 골라주세요.", mock_stdout.getvalue())
        self.assertIn("잘못된 입력입니다!! 1,2 중 하나를 입력하세요.", mock_stdout.getvalue())

    @patch("builtins.input", side_effect=["-1", "1"])  # 잘못된 입력(-1) 후 올바른 입력
    @patch("sys.stdout", new_callable=StringIO)
    def test_search_prompt_c3(self, mock_stdout, mock_input):
        search_prompt(controller=self.controller)
        self.assertIn("검색하고 싶은 종류를 골라주세요.", mock_stdout.getvalue())
        self.assertIn("잘못된 입력입니다!! 1,2 중 하나를 입력하세요.", mock_stdout.getvalue())

    @patch("builtins.input", side_effect=["!", "1"])  # 잘못된 입력(!) 후 올바른 입력
    @patch("sys.stdout", new_callable=StringIO)
    def test_search_prompt_c4(self, mock_stdout, mock_input):
        search_prompt(controller=self.controller)
        self.assertIn("검색하고 싶은 종류를 골라주세요.", mock_stdout.getvalue())
        self.assertIn("잘못된 입력입니다!! 1,2 중 하나를 입력하세요.", mock_stdout.getvalue())

    @patch("builtins.input", side_effect=["1.0", "1"])  # 잘못된 입력(1.0) 입력후 올바른 입력
    @patch("sys.stdout", new_callable=StringIO)
    def test_search_prompt_c5(self, mock_stdout, mock_input):
        search_prompt(controller=self.controller)
        self.assertIn("검색하고 싶은 종류를 골라주세요.", mock_stdout.getvalue())
        self.assertIn("잘못된 입력입니다!! 1,2 중 하나를 입력하세요.", mock_stdout.getvalue())

    @patch("builtins.input", side_effect=["exit", "1"])  # 잘못된 입력(exit) 후 올바른 입력
    @patch("sys.stdout", new_callable=StringIO)
    def test_search_prompt_c6(self, mock_stdout, mock_input):
        search_prompt(controller=self.controller)
        self.assertIn("검색하고 싶은 종류를 골라주세요.", mock_stdout.getvalue())
        self.assertIn("잘못된 입력입니다!! 1,2 중 하나를 입력하세요.", mock_stdout.getvalue())

    @patch("builtins.input", side_effect=[" ", "1"])  # 잘못된 입력=(빈 문자열) 입력후 올바른 입력
    @patch("sys.stdout", new_callable=StringIO)
    def test_search_prompt_c7(self, mock_stdout, mock_input):
        search_prompt(controller=self.controller)
        self.assertIn("검색하고 싶은 종류를 골라주세요.", mock_stdout.getvalue())
        self.assertIn("잘못된 입력입니다!! 1,2 중 하나를 입력하세요.", mock_stdout.getvalue())




