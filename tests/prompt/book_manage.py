import io
import os
import tempfile
import unittest
from unittest.mock import patch

from src.context import AppContext
from src.prompt.admin import delete_book_prompt, modify_book_prompt
from src.repository.entity import Borrow
from src.repository.manager import (
    BooksRepository, ISBNRepository, CategoryRepository, BorrowRepository
)
from src.service.book_service import BookService
from src.service.borrow_service import BorrowService


class FakeAppContext(AppContext):
    """
    실제 AppContext 는 데이터 파일 경로 고정이지만,
    테스트에서는 temp 파일을 사용해야 하므로 override 한다.
    """
    def __init__(self, books_path, isbn_path, cat_path, borrow_path):
        self.current_user = None
        self.current_date = None

        self.users_repo = None  # 사용 안함
        self.books_repo = BooksRepository(books_path)
        self.isbn_repo = ISBNRepository(isbn_path)
        self.cat_repo = CategoryRepository(cat_path)
        self.borrow_repo = BorrowRepository(borrow_path)
        self.borrow_history_repo = None  # 사용 안함


class TestDeleteBookPrompt(unittest.TestCase):

    def setUp(self):
        # temp 파일 생성
        self.books = tempfile.NamedTemporaryFile(delete=False, mode="w+", encoding="utf-8")
        self.isbn = tempfile.NamedTemporaryFile(delete=False, mode="w+", encoding="utf-8")
        self.cat = tempfile.NamedTemporaryFile(delete=False, mode="w+", encoding="utf-8")
        self.borrow = tempfile.NamedTemporaryFile(delete=False, mode="w+", encoding="utf-8")

        self.books_path = self.books.name
        self.isbn_path = self.isbn.name
        self.cat_path = self.cat.name
        self.borrow_path = self.borrow.name

        # 기본 데이터 구성
        self.books.write("001|ISBN07\n")
        self.books.write("002|ISBN07\n")
        self.books.write("007|ISBN07\n")
        self.books.close()

        self.isbn.write("ISBN07|Basic Java|Tae woon|CAT01\n")
        self.isbn.close()

        self.cat.write("CAT01|computer\n")
        self.cat.close()

        # borrow.txt 는 각 테스트에서 상황에 따라 작성하므로 초기화만
        self.borrow.close()

        # Fake AppContext 구성
        self.app = FakeAppContext(
            books_path=self.books_path,
            isbn_path=self.isbn_path,
            cat_path=self.cat_path,
            borrow_path=self.borrow_path,
        )

        self.book_service = BookService(self.app)
        self.borrow_service = BorrowService(self.app)

    def tearDown(self):
        os.unlink(self.books_path)
        os.unlink(self.isbn_path)
        os.unlink(self.cat_path)
        os.unlink(self.borrow_path)

    # ---------------------------------------------------
    # 6.3.2-a1 / a2 : 정상 삭제(대출 기록 없음)
    # ---------------------------------------------------
    @patch("builtins.input", side_effect=["001", "Y"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_delete_book_normal_no_borrow(self, mock_stdout, mock_input):
        """
        001 입력, borrow 없음 → 정상 삭제 가능
        """
        delete_book_prompt(self.book_service, self.borrow_service)
        out = mock_stdout.getvalue()

        self.assertIn("도서명: Basic Java", out)
        self.assertIn("해당 도서를 삭제했습니다.", out)

        # books.txt 에서 001 삭제되었는지 확인
        with open(self.books_path, "r", encoding="utf-8") as f:
            data = f.read()
            self.assertNotIn("001|", data)

    # ---------------------------------------------------
    # 6.3.2-a3 : 대출중이면 삭제 불가
    # ---------------------------------------------------
    @patch("builtins.input", side_effect=["001", "Y"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_delete_book_denied_if_borrowed(self, mock_stdout, mock_input):
        """
        001 이 대출중이면 삭제 불가
        """

        # borrow.txt 에 001 대출 추가 (반드시 Repository API 로!)
        self.app.borrow_repo.insert(
            Borrow(
                book_id="001",
                user_id="kim123",
                borrow_date="2025-01-08",
                due_date="2025-01-15",
            )
        )

        delete_book_prompt(self.book_service, self.borrow_service)
        out = mock_stdout.getvalue()

        self.assertIn("대출중이므로 삭제할 수 없습니다", out)

    # ---------------------------------------------------
    # 6.3.2-c1 : Y → 같은 ISBN 도서가 남아있을 때 (ISBN 삭제 X)
    # ---------------------------------------------------
    @patch("builtins.input", side_effect=["001", "Y"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_delete_book_confirm_yes_remaining_isbn(self, mock_stdout, mock_input):
        """
        books.txt: 001, 002, 007 모두 ISBN07
        → 001 삭제 후에도 ISBN07 남음 → ISBN 삭제하면 안됨
        """

        # borrow.txt 비움 (대출중 아님)
        self.app.borrow_repo.data = []

        delete_book_prompt(self.book_service, self.borrow_service)
        out = mock_stdout.getvalue()

        self.assertIn("해당 도서를 삭제했습니다.", out)

        # 001 삭제 후에도 ISBN07 은 남아 있어야 함
        with open(self.isbn_path, "r", encoding="utf-8") as f:
            data = f.read()
        self.assertIn("ISBN07", data)

    # c2: 소문자 y
    @patch("builtins.input", side_effect=["001", "y"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_delete_book_confirm_yes_lowercase_remaining_isbn(self, mock_stdout, mock_input):

        self.app.borrow_repo.data = []

        delete_book_prompt(self.book_service, self.borrow_service)
        out = mock_stdout.getvalue()

        self.assertIn("해당 도서를 삭제했습니다.", out)

        with open(self.isbn_path, "r", encoding="utf-8") as f:
            data = f.read()
        self.assertIn("ISBN07", data)


    # ---------------------------------------------------
    # 6.3.2-c3 : Y → 같은 ISBN 이 001 하나만 남았을 때 (ISBN 삭제 O)
    # ---------------------------------------------------
    @patch("builtins.input", side_effect=["001", "Y"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_delete_book_confirm_yes_last_isbn(self, mock_stdout, mock_input):
        """
        books.txt: 001 하나만 남기도록 Repository 에서 직접 삭제
        → 001 삭제 후 ISBN07 도 삭제되어야 함
        """

        # 002, 007 삭제하여 001 만 남게 함
        self.app.books_repo.delete("002")
        self.app.books_repo.delete("007")

        delete_book_prompt(self.book_service, self.borrow_service)
        out = mock_stdout.getvalue()
        self.assertIn("해당 도서를 삭제했습니다.", out)

        # ISBN07 삭제되었는지 확인
        with open(self.isbn_path, "r", encoding="utf-8") as f:
            data = f.read()
            self.assertNotIn("ISBN07", data)


    # c4: 소문자 y 이지만 동일 로직
    @patch("builtins.input", side_effect=["001", "y"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_delete_book_confirm_yes_lowercase_last_isbn(self, mock_stdout, mock_input):

        self.app.books_repo.delete("002")
        self.app.books_repo.delete("007")

        delete_book_prompt(self.book_service, self.borrow_service)
        out = mock_stdout.getvalue()

        self.assertIn("해당 도서를 삭제했습니다.", out)

        with open(self.isbn_path, "r", encoding="utf-8") as f:
            data = f.read()
        self.assertNotIn("ISBN07", data)


    # ---------------------------------------------------
    # 6.3.2-c5 : N → 삭제하지 않음
    # ---------------------------------------------------
    @patch("builtins.input", side_effect=["001", "N"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_delete_book_confirm_no(self, mock_stdout, mock_input):

        delete_book_prompt(self.book_service, self.borrow_service)
        out = mock_stdout.getvalue()

        self.assertIn("해당 도서를 삭제하지 않았습니다.", out)

        # 001 은 삭제되면 안 됨
        with open(self.books_path, "r", encoding="utf-8") as f:
            data = f.read()
        self.assertIn("001|ISBN07", data)

    # c6: 소문자 n
    @patch("builtins.input", side_effect=["001", "n"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_delete_book_confirm_no_lowercase(self, mock_stdout, mock_input):

        delete_book_prompt(self.book_service, self.borrow_service)
        out = mock_stdout.getvalue()

        self.assertIn("해당 도서를 삭제하지 않았습니다.", out)

        with open(self.books_path, "r", encoding="utf-8") as f:
            data = f.read()
        self.assertIn("001|ISBN07", data)



    #todo 공백은 나중에
    # ---------------------------------------------------
    # 6.3.2-b : 공백 포함 BookID → 오류 메시지
    # ---------------------------------------------------
    # @patch("builtins.input", side_effect=[" 001", "001", "Y"])
    # @patch("sys.stdout", new_callable=io.StringIO)
    # def test_delete_book_id_space_before(self, mock_stdout, mock_input):
    #     delete_book_prompt(self.book_service, self.borrow_service)
    #     out = mock_stdout.getvalue()
    #     self.assertIn("고유번호는 공백을 포함하지 않습니다", out)

    # @patch("builtins.input", side_effect=["001 ", "001", "Y"])
    # @patch("sys.stdout", new_callable=io.StringIO)
    # def test_delete_book_id_space_after(self, mock_stdout, mock_input):
    #     delete_book_prompt(self.book_service, self.borrow_service)
    #     out = mock_stdout.getvalue()
    #     self.assertIn("고유번호는 공백을 포함하지 않습니다", out)

    # @patch("builtins.input", side_effect=[" 001 ", "001", "Y"])
    # @patch("sys.stdout", new_callable=io.StringIO)
    # def test_delete_book_id_space_both(self, mock_stdout, mock_input):
    #     delete_book_prompt(self.book_service, self.borrow_service)
    #     out = mock_stdout.getvalue()
    #     self.assertIn("고유번호는 공백을 포함하지 않습니다", out)

    # ---------------------------------------------------
    # 6.3.2-c : Y/y 입력에 따른 삭제 처리
    # ---------------------------------------------------
    @patch("builtins.input", side_effect=["001", "Y"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_delete_book_confirm_yes_with_remaining_same_isbn(self, mock_stdout, mock_input):
        """
        같은 ISBN 가진 도서가 남아있음 → books만 삭제, ISBN은 삭제 안함
        """
        delete_book_prompt(self.book_service, self.borrow_service)
        out = mock_stdout.getvalue()

        self.assertIn("해당 도서를 삭제했습니다.", out)

        # 002,007이 있으므로 ISBN07 남아야 함
        with open(self.isbn_path, "r", encoding="utf-8") as f:
            data = f.read()
            self.assertIn("ISBN07", data)

    @patch("builtins.input", side_effect=["001", "Y"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_delete_book_confirm_yes_last_isbn(self, mock_stdout, mock_input):
        """
        ISBN07 을 가진 도서가 001만 있는 경우 → books + ISBN 모두 삭제
        """
        # 1) 리포지토리 API로 002, 007을 삭제해서
        #    ISBN07 을 가진 물리 도서가 001 하나만 남도록 만든다.
        self.book_service.books.delete("002")
        self.book_service.books.delete("007")


        remaining = self.book_service.books.find_by_isbn("ISBN07")
        self.assertEqual(len(remaining), 1)
        self.assertEqual(remaining[0].book_id, "001")

        # 2) 실제 프롬프트 실행
        delete_book_prompt(self.book_service, self.borrow_service)
        out = mock_stdout.getvalue()

        self.assertIn("해당 도서를 삭제했습니다.", out)

        # 3) ISBN이 실제로 삭제됐는지 확인
        with open(self.isbn_path, "r", encoding="utf-8") as f:
            data = f.read()
            self.assertNotIn("ISBN07", data)

    @patch("builtins.input", side_effect=["001", "N"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_delete_book_confirm_no(self, mock_stdout, mock_input):
        delete_book_prompt(self.book_service, self.borrow_service)
        out = mock_stdout.getvalue()
        self.assertIn("해당 도서를 삭제하지 않았습니다.", out)

    # ---------------------------------------------------
    # 6.3.2-d : Y/N 앞뒤 공백 처리
    # ---------------------------------------------------
    @patch("builtins.input", side_effect=["001", " y "])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_delete_book_confirm_space_yes(self, mock_stdout, mock_input):
        delete_book_prompt(self.book_service, self.borrow_service)
        out = mock_stdout.getvalue()
        self.assertIn("해당 도서를 삭제했습니다.", out)

    @patch("builtins.input", side_effect=["001", " n "])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_delete_book_confirm_space_no(self, mock_stdout, mock_input):
        delete_book_prompt(self.book_service, self.borrow_service)
        out = mock_stdout.getvalue()
        self.assertIn("해당 도서를 삭제하지 않았습니다.", out)

class TestModifyBookPrompt(unittest.TestCase):

    def setUp(self):
        # temp files
        self.books = tempfile.NamedTemporaryFile(delete=False, mode="w+", encoding="utf-8")
        self.isbn = tempfile.NamedTemporaryFile(delete=False, mode="w+", encoding="utf-8")
        self.cat = tempfile.NamedTemporaryFile(delete=False, mode="w+", encoding="utf-8")
        self.borrow = tempfile.NamedTemporaryFile(delete=False, mode="w+", encoding="utf-8")

        self.books_path = self.books.name
        self.isbn_path = self.isbn.name
        self.cat_path = self.cat.name
        self.borrow_path = self.borrow.name

        # -------------------------
        # 기본 테스트 데이터 구성
        # -------------------------
        # books.txt
        self.books.write("001|ISBN01\n")
        self.books.write("002|ISBN01\n")
        self.books.write("007|ISBN02\n")
        self.books.close()

        # ISBN.txt
        self.isbn.write("ISBN01|Basic Python|Ji Min|CAT01\n")
        self.isbn.write("ISBN02|Nintendo|Gun woo|CAT01\n")
        self.isbn.close()

        # categories.txt
        self.cat.write("CAT01|computer\n")
        self.cat.close()

        # borrow.txt (기본은 빈 파일)
        self.borrow.write("")
        self.borrow.close()

        # Fake AppContext
        self.app = FakeAppContext(
            books_path=self.books_path,
            isbn_path=self.isbn_path,
            cat_path=self.cat_path,
            borrow_path=self.borrow_path
        )

        # Services
        self.book_service = BookService(self.app)
        self.borrow_service = BorrowService(self.app)

    def tearDown(self):
        os.unlink(self.books_path)
        os.unlink(self.isbn_path)
        os.unlink(self.cat_path)
        os.unlink(self.borrow_path)

    # ------------------------------------------------------
    # 6.3.3-a : 정상 → ISBN01, ISBN02 입력 시 도서정보 출력
    # ------------------------------------------------------
    @patch("builtins.input", side_effect=["ISBN01", "NewTitle|NewAuthor"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_modify_book_prompt_a1(self, mock_stdout, mock_input):
        modify_book_prompt(self.book_service)
        out = mock_stdout.getvalue()
        self.assertIn("[수정할 도서 정보]", out)
        self.assertIn("Basic Python", out)
        self.assertIn("Ji Min", out)

    @patch("builtins.input", side_effect=["ISBN02", "NewTitle|NewAuthor"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_modify_book_prompt_a2(self, mock_stdout, mock_input):
        modify_book_prompt(self.book_service)
        out = mock_stdout.getvalue()
        self.assertIn("[수정할 도서 정보]", out)
        self.assertIn("Nintendo", out)
        self.assertIn("Gun woo", out)

    # ------------------------------------------------------
    # 6.3.3-b : ISBN 문법 오류 / 공백 오류
    # ------------------------------------------------------
    @patch("builtins.input", side_effect=["ISBN1", "ISBN01", "New|A"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_modify_book_prompt_b1(self, mock_stdout, mock_input):
        modify_book_prompt(self.book_service)
        self.assertIn("ISBN의 형식은 ISBN+숫자2개입니다", mock_stdout.getvalue())

    @patch("builtins.input", side_effect=["ISBN123", "ISBN01", "New|A"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_modify_book_prompt_b2(self, mock_stdout, mock_input):
        modify_book_prompt(self.book_service)
        self.assertIn("ISBN의 형식은 ISBN+숫자2개입니다", mock_stdout.getvalue())

    @patch("builtins.input", side_effect=["isbn01", "ISBN01", "New|A"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_modify_book_prompt_b3(self, mock_stdout, mock_input):
        modify_book_prompt(self.book_service)
        self.assertIn("ISBN의 형식은 ISBN+숫자2개입니다", mock_stdout.getvalue())

    #todo 공백 테스트는 나중에
    # @patch("builtins.input", side_effect=[" ISBN01", "ISBN01", "New|A"])
    # @patch("sys.stdout", new_callable=io.StringIO)
    # def test_modify_book_prompt_b6(self, mock_stdout, mock_input):
    #     modify_book_prompt(self.book_service)
    #     self.assertIn("입력에 공백을 포함할 수 없습니다", mock_stdout.getvalue())

    # ------------------------------------------------------
    # 6.3.3-c : 존재하지 않는 ISBN 입력
    # ------------------------------------------------------
    @patch("builtins.input", side_effect=["ISBN05", "ISBN01", "New|A"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_modify_book_prompt_c1(self, mock_stdout, mock_input):
        modify_book_prompt(self.book_service)
        self.assertIn("존재하지 않는 ISBN입니다.", mock_stdout.getvalue())

    # ------------------------------------------------------
    # 6.3.3-d : 정상 입력 new_title|new_author
    # ------------------------------------------------------
    @patch("builtins.input", side_effect=["ISBN01", "Python|taewoon"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_modify_book_prompt_d1(self, mock_stdout, mock_input):
        modify_book_prompt(self.book_service)
        out = mock_stdout.getvalue()
        self.assertIn("수정했습니다.", out)

        # 실제 파일 반영 검사
        with open(self.isbn_path, "r", encoding="utf-8") as f:
            data = f.read()
        self.assertIn("Python", data)
        self.assertIn("taewoon", data)

    # ------------------------------------------------------
    # 6.3.3-e/g : 도서명/저자 형식 오류 테스트 일부
    # ------------------------------------------------------
    @patch("builtins.input", side_effect=["ISBN01", "Basic  python|taetae", "Python|tae"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_modify_book_prompt_g1(self, mock_stdout, mock_input):
        modify_book_prompt(self.book_service)
        self.assertIn("잘못된 입력입니다!! 올바른 제목을 입력하세요", mock_stdout.getvalue())

    @patch("builtins.input", side_effect=["ISBN01", "Python||tae", "Python|tae"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_modify_book_prompt_g19(self, mock_stdout, mock_input):
        modify_book_prompt(self.book_service)
        self.assertIn("[도서명 | 저자] 형식으로 입력해주세요.", mock_stdout.getvalue())

    # asd → 오류
    @patch("builtins.input", side_effect=["asd", "ISBN01", "New|A"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_isbn_invalid_asd(self, mock_stdout, mock_input):
        modify_book_prompt(self.book_service)
        self.assertIn("ISBN의 형식은 ISBN+숫자2개입니다", mock_stdout.getvalue())

    # 123 → 오류
    @patch("builtins.input", side_effect=["123", "ISBN01", "New|A"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_isbn_invalid_123(self, mock_stdout, mock_input):
        modify_book_prompt(self.book_service)
        self.assertIn("ISBN의 형식은 ISBN+숫자2개입니다", mock_stdout.getvalue())
    #
    # # ISBN␣01 → 공백 오류
    # @patch("builtins.input", side_effect=["ISBN 01", "ISBN01", "New|A"])
    # @patch("sys.stdout", new_callable=io.StringIO)
    # def test_isbn_invalid_space_middle(self, mock_stdout, mock_input):
    #     modify_book_prompt(self.book_service)
    #     self.assertIn("입력에 공백을 포함할 수 없습니다", mock_stdout.getvalue())

    # # ISBN01␣ → 공백 오류
    # @patch("builtins.input", side_effect=["ISBN01 ", "ISBN01", "New|A"])
    # @patch("sys.stdout", new_callable=io.StringIO)
    # def test_isbn_invalid_space_end(self, mock_stdout, mock_input):
    #     modify_book_prompt(self.book_service)
    #     self.assertIn("입력에 공백을 포함할 수 없습니다", mock_stdout.getvalue())

    # 빈 문자열 → 오류
    @patch("builtins.input", side_effect=["", "ISBN01", "New|A"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_isbn_invalid_empty(self, mock_stdout, mock_input):
        modify_book_prompt(self.book_service)
        self.assertIn("ISBN의 형식은 ISBN+숫자2개입니다", mock_stdout.getvalue())

    # 공백(" ") → 오류
    @patch("builtins.input", side_effect=[" ", "ISBN01", "New|A"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_isbn_invalid_one_space(self, mock_stdout, mock_input):
        modify_book_prompt(self.book_service)
        self.assertIn("ISBN의 형식은 ISBN+숫자2개입니다", mock_stdout.getvalue())

    # ISBN10 없음 → 오류
    @patch("builtins.input", side_effect=["ISBN10", "ISBN01", "New|A"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_isbn_not_found(self, mock_stdout, mock_input):
        modify_book_prompt(self.book_service)
        self.assertIn("존재하지 않는 ISBN입니다.", mock_stdout.getvalue())

    # Python|tae woon → 성공
    @patch("builtins.input", side_effect=["ISBN01", "Python|tae woon"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_modify_success_author_with_space(self, mock_stdout, mock_input):
        modify_book_prompt(self.book_service)
        self.assertIn("수정했습니다.", mock_stdout.getvalue())

    # Basic python|ji min → 성공
    @patch("builtins.input", side_effect=["ISBN01", "Basic python|ji min"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_modify_success_both_have_space(self, mock_stdout, mock_input):
        modify_book_prompt(self.book_service)
        self.assertIn("수정했습니다.", mock_stdout.getvalue())


    # Basic python ␣|taetae → 오류
    @patch("builtins.input", side_effect=["ISBN01", "Basic python |taetae", "Python|ok"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_modify_invalid_title_trailing_space(self, mock_stdout, mock_input):
        modify_book_prompt(self.book_service)
        self.assertIn("잘못된 입력입니다!! 올바른 제목을 입력하세요.", mock_stdout.getvalue())

    # Basic python|␣taetae → 오류
    @patch("builtins.input", side_effect=["ISBN01", "Basic python| taetae", "Python|ok"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_modify_invalid_author_leading_space(self, mock_stdout, mock_input):
        modify_book_prompt(self.book_service)
        self.assertIn("잘못된 입력입니다!! 올바른 저자를 입력하세요.", mock_stdout.getvalue())

    # Basic python␣|␣taetae → 오류
    @patch("builtins.input", side_effect=["ISBN01", "Basic python | taetae", "Python|ok"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_modify_invalid_both_side_spaces(self, mock_stdout, mock_input):
        modify_book_prompt(self.book_service)
        self.assertIn("잘못된 입력입니다!! 올바른 제목을 입력하세요.", mock_stdout.getvalue())

    # Basic python|tae␣␣tae → 오류
    @patch("builtins.input", side_effect=["ISBN01", "Basic python|tae  tae", "Python|ok"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_modify_invalid_author_double_space_middle(self, mock_stdout, mock_input):
        modify_book_prompt(self.book_service)
        self.assertIn("잘못된 입력입니다!! 올바른 저자를 입력하세요.", mock_stdout.getvalue())


    # !Basic python|taetae → 오류
    @patch("builtins.input", side_effect=["ISBN01", "!Basic python|taetae", "Python|ok"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_modify_invalid_title_symbol(self, mock_stdout, mock_input):
        modify_book_prompt(self.book_service)
        self.assertIn("잘못된 입력입니다!! 올바른 제목을 입력하세요.", mock_stdout.getvalue())

    # Basic python|!taetae → 오류
    @patch("builtins.input", side_effect=["ISBN01", "Basic python|!taetae", "Python|ok"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_modify_invalid_author_symbol(self, mock_stdout, mock_input):
        modify_book_prompt(self.book_service)
        self.assertIn("잘못된 입력입니다!! 올바른 저자를 입력하세요.", mock_stdout.getvalue())

    # Basic python|(빈문자열) → 오류
    @patch("builtins.input", side_effect=["ISBN01", "Basic python|", "Python|ok"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_modify_invalid_empty_author(self, mock_stdout, mock_input):
        modify_book_prompt(self.book_service)
        self.assertIn("도서명과 저자는 각각 1자 이상이어야 합니다", mock_stdout.getvalue())

    # Basic python|␣ → 오류
    @patch("builtins.input", side_effect=["ISBN01", "Basic python| ", "Python|ok"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_modify_invalid_author_blank_space(self, mock_stdout, mock_input):
        modify_book_prompt(self.book_service)
        self.assertIn("도서명과 저자는 각각 1자 이상이어야 합니다", mock_stdout.getvalue())

    # (빈문자열)|taetae → 오류
    @patch("builtins.input", side_effect=["ISBN01", "|taetae", "Python|ok"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_modify_invalid_empty_title(self, mock_stdout, mock_input):
        modify_book_prompt(self.book_service)
        self.assertIn("도서명과 저자는 각각 1자 이상이어야 합니다", mock_stdout.getvalue())

    # ␣|taetae → 오류
    @patch("builtins.input", side_effect=["ISBN01", " |taetae", "Python|ok"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_modify_invalid_title_blank_space(self, mock_stdout, mock_input):
        modify_book_prompt(self.book_service)
        self.assertIn("도서명과 저자는 각각 1자 이상이어야 합니다", mock_stdout.getvalue())
    #
    # # ␣Python|taewoon → 오류
    # @patch("builtins.input", side_effect=["ISBN01", " Python|taewoon", "Python|ok"])
    # @patch("sys.stdout", new_callable=io.StringIO)
    # def test_modify_invalid_title_leading_space(self, mock_stdout, mock_input):
    #     modify_book_prompt(self.book_service)
    #     self.assertIn("잘못된 입력입니다!! 올바른 제목을 입력하세요.", mock_stdout.getvalue())


    # # Python|taewoon␣ → 오류
    # @patch("builtins.input", side_effect=["ISBN01", "Python|taewoon ", "Python|ok"])
    # @patch("sys.stdout", new_callable=io.StringIO)
    # def test_modify_invalid_author_trailing_space(self, mock_stdout, mock_input):
    #     modify_book_prompt(self.book_service)
    #     self.assertIn("잘못된 입력입니다!! 올바른 저자를 입력하세요.", mock_stdout.getvalue())

    # # ␣Python|taewoon␣ → 오류
    # @patch("builtins.input", side_effect=["ISBN01", " Python|taewoon ", "Python|ok"])
    # @patch("sys.stdout", new_callable=io.StringIO)
    # def test_modify_invalid_both_sides_space(self, mock_stdout, mock_input):
    #     modify_book_prompt(self.book_service)
    #     self.assertIn("잘못된 입력입니다!! 올바른 제목을 입력하세요.", mock_stdout.getvalue())

    # Python taewoon → 형식 오류
    @patch("builtins.input", side_effect=["ISBN01", "Python taewoon", "Python|ok"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_modify_invalid_format_missing_bar(self, mock_stdout, mock_input):
        modify_book_prompt(self.book_service)
        self.assertIn("[도서명 | 저자] 형식으로 입력해주세요.", mock_stdout.getvalue())

    # Python| taewoon |too → 형식 오류
    @patch("builtins.input", side_effect=["ISBN01", "Python| taewoon |too", "Python|ok"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_modify_invalid_format_multiple_bar(self, mock_stdout, mock_input):
        modify_book_prompt(self.book_service)
        self.assertIn("[도서명 | 저자] 형식으로 입력해주세요.", mock_stdout.getvalue())

