import io
import os
import tempfile
import unittest
from unittest.mock import patch

from src.context import AppContext
from src.prompt.search import search_by_category_prompt
from src.repository.manager import BooksRepository, ISBNRepository, CategoryRepository, BorrowRepository
from src.service.book_service import BookService
from src.service.cat_service import CategoryService


class FakeAppContext(AppContext):
    """
    실제 파일 경로를 모두 temp 파일로 대체하는 Fake Context
    """
    def __init__(self, books_path, isbn_path, cat_path, borrow_path):
        self.current_date = None
        self.current_user = None

        # Fake repositories
        self.users_repo = None
        self.books_repo = BooksRepository(books_path)
        self.borrow_repo = BorrowRepository(borrow_path)
        self.borrow_history_repo = None
        self.isbn_repo = ISBNRepository(isbn_path)
        self.cat_repo = CategoryRepository(cat_path)


class TestSearchByCategoryPrompt(unittest.TestCase):

    def setUp(self):
        # temp 파일 생성
        self.fp_books = tempfile.NamedTemporaryFile(delete=False, mode='w+', encoding='utf-8')
        self.fp_isbn = tempfile.NamedTemporaryFile(delete=False, mode='w+', encoding='utf-8')
        self.fp_cat = tempfile.NamedTemporaryFile(delete=False, mode='w+', encoding='utf-8')
        self.fp_borrow = tempfile.NamedTemporaryFile(delete=False, mode='w+', encoding='utf-8')

        # 카테고리
        # CAT01 | science
        # CAT02 | space
        # CAT03 | chemistry
        self.fp_cat.write("CAT01|science\n")
        self.fp_cat.write("CAT02|space\n")
        self.fp_cat.write("CAT03|chemistry\n")
        self.fp_cat.close()

        # ISBN
        # science + space
        # ISBN01 | Bigbang1 | Jensen | CAT01;CAT02
        # chemistry만
        # ISBN10 | Chem Book | Author | CAT03
        self.fp_isbn.write("ISBN01|Bigbang1|Jensen|CAT01;CAT02\n")
        self.fp_isbn.write("ISBN10|Chem Book|Author|CAT03\n")
        self.fp_isbn.close()

        # Books (ISBN01만 실제로 존재)
        self.fp_books.write("003|ISBN01\n")
        self.fp_books.close()

        # borrow 비어있음
        self.fp_borrow.close()

        # context 생성
        self.app = FakeAppContext(
            books_path=self.fp_books.name,
            isbn_path=self.fp_isbn.name,
            cat_path=self.fp_cat.name,
            borrow_path=self.fp_borrow.name
        )

        # 서비스 생성
        self.book_service = BookService(self.app)
        self.cat_service = CategoryService(self.app)

    def tearDown(self):
        os.unlink(self.fp_books.name)
        os.unlink(self.fp_isbn.name)
        os.unlink(self.fp_cat.name)
        os.unlink(self.fp_borrow.name)

    # ------------------------------------------------------
    # 1) 정상 검색: science & space
    # ------------------------------------------------------
    @patch("builtins.input", side_effect=["science&space"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_category_prompt_normal(self, mock_stdout, mock_input):
        search_by_category_prompt(
            book_service=self.book_service,
            cat_service=self.cat_service
        )
        # Bigbang1 책이 출력되었는지 확인
        self.assertIn("대여가능 | 003 | Bigbang1 | Jensen | science;space", mock_stdout.getvalue())

    # ------------------------------------------------------
    # 2) 문법 오류: science && space → 재입력 발생
    # ------------------------------------------------------
    @patch("builtins.input", side_effect=["science&&space", "science&space"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_category_prompt_operator_error(self, mock_stdout, mock_input):
        search_by_category_prompt(
            book_service=self.book_service,
            cat_service=self.cat_service
        )
        out = mock_stdout.getvalue()

        # 연속 연산자 오류 출력됐는지
        self.assertIn("연산자는 연속으로 사용할 수 없습니다", out)
        # 정상검색까지 이어졌는지
        self.assertIn("대여가능 | 003 | Bigbang1", out)

    # ------------------------------------------------------
    # 3) 존재하지 않는 카테고리: math
    # ------------------------------------------------------
    @patch("builtins.input", side_effect=["math"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_category_prompt_not_exist_category(self, mock_stdout, mock_input):
        search_by_category_prompt(
            book_service=self.book_service,
            cat_service=self.cat_service
        )
        out = mock_stdout.getvalue()

        self.assertIn("카테고리에 해당하는 도서가 존재하지 않습니다.", out)
    # ------------------------------------------------------
    # 4) ISBN 존재하지만 Books 없음 케이스: chemistry
    # ------------------------------------------------------
    @patch("builtins.input", side_effect=["chemistry"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_category_prompt_no_physical_book(self, mock_stdout, mock_input):
        search_by_category_prompt(
            book_service=self.book_service,
            cat_service=self.cat_service
        )
        out = mock_stdout.getvalue()

        self.assertIn("카테고리에 해당하는 도서가 존재하지 않습니다.", out)
    # ---------------------------------------------------------
    # [6.2.1.2-2] 비정상 결과 1: 문법 위배 (로마자/공백 오류)
    # ---------------------------------------------------------

    @patch("builtins.input", side_effect=["Computer", "science&space"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_category_prompt_invalid_case_uppercase(self, mock_stdout, mock_input):
        """
        입력: Computer → 로마자 소문자 위배
        """
        search_by_category_prompt(self.book_service, self.cat_service)
        out = mock_stdout.getvalue()
        self.assertIn("카테고리명은 로마자 소문자만 입력받을 수 있습니다", out)

    @patch("builtins.input", side_effect=["computer3", "science&space"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_category_prompt_invalid_case_number(self, mock_stdout, mock_input):
        """
        입력: computer3 → 숫자 포함
        """
        search_by_category_prompt(self.book_service, self.cat_service)
        out = mock_stdout.getvalue()
        self.assertIn("카테고리명은 로마자 소문자만 입력받을 수 있습니다", out)

    @patch("builtins.input", side_effect=[" computer", "science&space"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_category_prompt_invalid_case_space_before(self, mock_stdout, mock_input):
        """
        입력: ' computer' → 공백 포함
        """
        search_by_category_prompt(self.book_service, self.cat_service)
        out = mock_stdout.getvalue()
        self.assertIn("카테고리명은 공백을 포함하지않습니다", out)

    @patch("builtins.input", side_effect=[" ", "science&space"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_category_prompt_invalid_case_only_space(self, mock_stdout, mock_input):
        """
        입력: ' ' (공백만)
        """
        search_by_category_prompt(self.book_service, self.cat_service)
        out = mock_stdout.getvalue()
        self.assertIn("카테고리명은 공백을 포함하지않습니다", out)


    # ---------------------------------------------------------
    # [6.2.1.2-3] 비정상 결과 2: 검색 조건 위배
    # ---------------------------------------------------------

    @patch("builtins.input", side_effect=["(science)&(space)", "science&space"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_category_prompt_invalid_case_parenthesis(self, mock_stdout, mock_input):
        """
        입력: (science)&(space) → 괄호 금지
        """
        search_by_category_prompt(self.book_service, self.cat_service)
        out = mock_stdout.getvalue()
        self.assertIn("괄호는 사용할 수 없습니다", out)

    @patch("builtins.input", side_effect=["computer!", "science&space"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_category_prompt_invalid_case_not_wrong(self, mock_stdout, mock_input):
        """
        입력: computer! → NOT 앞에 피연산자 없음
        """
        search_by_category_prompt(self.book_service, self.cat_service)
        out = mock_stdout.getvalue()
        self.assertIn("NOT앞에는 피연산자가 올 수 없습니다", out)

    @patch("builtins.input", side_effect=["science| ", "science&space"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_category_prompt_invalid_case_or_missing_operand(self, mock_stdout, mock_input):
        """
        입력: science |  → OR 좌우 operand 없음
        """
        search_by_category_prompt(self.book_service, self.cat_service)
        out = mock_stdout.getvalue()
        self.assertIn("AND, OR은 좌우에 각각 하나의 피연산자가 존재해야 합니다", out)

"""
검사 코드의 우선 순위에 따라서 다르게 동작됨
"""
    # @patch("builtins.input", side_effect=["science& ", "science&space"])
    # @patch("sys.stdout", new_callable=io.StringIO)
    # def test_category_prompt_invalid_case_and_missing_operand(self, mock_stdout, mock_input):
    #     """
    #     입력: science &  → AND 좌우 operand 없음
    #     """
    #     search_by_category_prompt(self.book_service, self.cat_service)
    #     out = mock_stdout.getvalue()
    #     self.assertIn("AND, OR은 좌우에 각각 하나의 피연산자가 존재해야 합니다", out)
    #
    # @patch("builtins.input", side_effect=["science&&space", "science&space"])
    # @patch("sys.stdout", new_callable=io.StringIO)
    # def test_category_prompt_invalid_case_operator_chain(self, mock_stdout, mock_input):
    #     """
    #     입력: science&&space → 연산자 연속
    #     """
    #     search_by_category_prompt(self.book_service, self.cat_service)
    #     out = mock_stdout.getvalue()
    #     self.assertIn("연산자는 연속으로 사용할 수 없습니다", out)
    #
    # @patch("builtins.input", side_effect=["science+space", "science&space"])
    # @patch("sys.stdout", new_callable=io.StringIO)
    # def test_category_prompt_invalid_case_unsupported_operator(self, mock_stdout, mock_input):
    #     """
    #     입력: science+space → 허용되지 않는 연산자
    #     """
    #     search_by_category_prompt(self.book_service, self.cat_service)
    #     out = mock_stdout.getvalue()
    #     self.assertIn("허용 가능한 연산자는 !,&,|입니다", out)
    #
    #
    # # ---------------------------------------------------------
    # # [6.2.1.2-4] 비정상 결과 3: 존재하지 않는 카테고리
    # # ---------------------------------------------------------
    # @patch("builtins.input", side_effect=["math"])
    # @patch("sys.stdout", new_callable=io.StringIO)
    # def test_category_prompt_category_not_exists(self, mock_stdout, mock_input):
    #     """
    #     입력: math → 카테고리 없음
    #     """
    #     search_by_category_prompt(self.book_service, self.cat_service)
    #     out = mock_stdout.getvalue()
    #
    #     # 문서 요구 메시지
    #     self.assertIn("존재하지 않는 카테고리명입니다", out)
    #
    #
    # # ---------------------------------------------------------
    # # [6.2.1.2-5] 비정상 결과 4: ISBN 없음
    # # ---------------------------------------------------------
    # @patch("builtins.input", side_effect=["english"])
    # @patch("sys.stdout", new_callable=io.StringIO)
    # def test_category_prompt_no_isbn_for_category(self, mock_stdout, mock_input):
    #     """
    #     english 카테고리는 존재하지만 ISBN 없음
    #     """
    #     search_by_category_prompt(self.book_service, self.cat_service)
    #     out = mock_stdout.getvalue()
    #
    #     self.assertIn("카테고리에 해당하는 도서가 존재하지 않습니다", out)