import os
import tempfile
import unittest

from src.repository.manager import BooksRepository, ISBNRepository, CategoryRepository, BorrowRepository
from src.service.book_service import BookService

"""
개발의 편리성과 테스트의 용이함을 위해 service는 repository 합쳐서 통합 테스트만 진행합니다.
"""

class TestBookServiceIntegration(unittest.TestCase):

    def setUp(self):
        # 임시 파일 생성
        self.books = tempfile.NamedTemporaryFile(delete=False, mode="w+")
        self.path1 = self.books.name
        self.isbn = tempfile.NamedTemporaryFile(delete=False, mode="w+")
        self.path2 = self.isbn.name
        self.categories = tempfile.NamedTemporaryFile(delete=False, mode="w+")
        self.path3 = self.categories.name
        self.borrows = tempfile.NamedTemporaryFile(delete=False, mode="w+")
        self.path4 = self.borrows.name

        # 테스트용 초기 데이터 작성
        self.books.write("007|ISBN07\n")
        self.books.close()
        self.isbn.write("ISBN07|Computer Science|Elon musk|CAT01\n")
        self.isbn.close()
        self.categories.write("CAT01|computer\n")
        self.categories.close()

        # 통합 테스트: 실제 Repository + 실제 Service
        self.book_repo = BooksRepository(self.path1)
        self.isbn_repo = ISBNRepository(self.path2)
        self.cat_repo = CategoryRepository(self.path3)
        self.borrow_repo = BorrowRepository(self.path4)

        self.service = BookService(self.book_repo, self.isbn_repo, self.cat_repo, self.borrow_repo)


    def tearDown(self):
        # 테스트 파일 삭제
        os.unlink(self.path1)
        os.unlink(self.path2)
        os.unlink(self.path3)

    def test_search_book_by_title_exact_match(self):
        """
        정상 케이스: 정확한 도서명 검색
        Document Case:
        - 입력: "Computer Science"
        - 결과: 책 상태, book_id, title, author, category 매칭
        """
        # when
        result = self.service.search_book_by_title("Computer Science")

        # then
        self.assertEqual(len(result), 1)
        book = result[0]
        self.assertEqual(book.book_id, "007")
        self.assertEqual(book.isbn, "ISBN07")

        # ISBN 매핑도 검증
        isbn = self.isbn_repo.find_by_isbn("ISBN07")
        self.assertEqual(isbn.title, "Computer Science")
        self.assertEqual(isbn.author, "Elon musk")
        self.assertEqual(isbn.cat_id, "CAT01")

    def test_search_book_by_title_case_insensitive_match(self):
        """
        대소문자 무시 검색
        Document Case:
        - 입력: "computer science", "COMPUTER SCIENCE"
        """
        result1 = self.service.search_book_by_title("computer science")
        result2 = self.service.search_book_by_title("COMPUTER SCIENCE")

        self.assertEqual(len(result1), 1)
        self.assertEqual(len(result2), 1)

        self.assertEqual(result1[0].book_id, "007")
        self.assertEqual(result2[0].book_id, "007")

    def test_search_book_by_title_partial_match(self):
        """
        부분 일치 검색
        Document Case:
        - 입력: "Science", "com", "computer"
        """
        # when
        result1 = self.service.search_book_by_title("Science")
        result2 = self.service.search_book_by_title("com")
        result3 = self.service.search_book_by_title("computer")

        # then
        self.assertEqual(len(result1), 1)
        self.assertEqual(result1[0].book_id, "007")

        self.assertEqual(len(result2), 1)
        self.assertEqual(result2[0].book_id, "007")

        self.assertEqual(len(result3), 1)
        self.assertEqual(result3[0].book_id, "007")

    def test_search_book_by_title_not_found(self):
        """
        존재하지 않는 도서 검색
        Document Case:
        - 입력: "Computer Graphics"
        - 출력: []
        """
        result = self.service.search_book_by_title("Computer Graphics")
        self.assertEqual(result, [])

    def test_search_book_by_title_not_exist_cases(self):
        """
        존재하지 않는 도서 입력 → 결과 없음([])
        케이스:
            - "Computer Graphics"
            - "1"
            - "0"
            - "Computer Science2"
        """

        inputs = [
            "Computer Graphics",
            "1",
            "0",
            "Computer Science2",
        ]

        for keyword in inputs:
            with self.subTest(keyword=keyword):
                result = self.service.search_book_by_title(keyword)
                self.assertEqual(result, [], f"입력값 '{keyword}' 에 대해 결과가 [] 이어야 함")


    def test_add_book_isbn_not_exists_new_registration(self):
        """
        ISBN 없음 → 신규 등록
        초기 상태:
            ISBN07 하나만 존재
        입력:
            title="New Title", author="New Author"
        검증:
            - ISBNRepository에 새 ISBN 생성됨
            - books.txt에 새로운 book_id 추가됨
        """
        # when
        self.service.add_book("New Title", "New Author")

        # then
        # 새 ISBN이 생성되었는지 확인
        all_isbns = self.isbn_repo.data
        self.assertEqual(len(all_isbns), 2)

        new_isbn = [i for i in all_isbns if i.title == "New Title"][0]
        self.assertEqual(new_isbn.author, "New Author")
        self.assertEqual(new_isbn.cat_id, "CAT00")  # 기본 카테고리 등록 확인

        # books.txt도 1건 증가
        all_books = self.book_repo.data
        self.assertEqual(len(all_books), 2)
        self.assertEqual(all_books[-1].isbn, new_isbn.isbn)

    def test_add_book_title_match_only_register_new(self):
        """
        제목만 일치 → 신규 등록
        조건:
            기존 ISBN07: title="Computer Science", author="Elon musk"
        입력:
            title="Computer Science", author="Different Author"

        Document Case:
            - 제목만 일치하는 ISBN은 사용하면 안 됨
            - 저자가 다르면 새 ISBN 생성해야함
        """
        # when
        self.service.add_book("Computer Science", "Different Author")

        # then
        all_isbns = self.isbn_repo.data
        self.assertEqual(len(all_isbns), 2)

        # 제목은 같지만 다른 저자로 신규 생성 여부
        new_isbn = [i for i in all_isbns if i.author == "Different Author"][0]
        self.assertEqual(new_isbn.title, "Computer Science")

        # books.txt 증가 확인
        all_books = self.book_repo.data
        self.assertEqual(len(all_books), 2)
        self.assertEqual(all_books[-1].isbn, new_isbn.isbn)

    def test_add_book_author_match_only_register_new(self):
        """
        저자만 일치 → 신규 등록
        조건:
            기존 ISBN07: title="Computer Science", author="Elon musk"
        입력:
            title="Different Title", author="Elon musk"

        기대:
            - 제목이 다르므로 새 ISBN 생성
        """
        # when
        self.service.add_book("Different Title", "Elon musk")

        # then
        all_isbns = self.isbn_repo.data
        self.assertEqual(len(all_isbns), 2)

        new_isbn = [i for i in all_isbns if i.title == "Different Title"][0]
        self.assertEqual(new_isbn.author, "Elon musk")

        # books.txt 증가 확인
        all_books = self.book_repo.data
        self.assertEqual(len(all_books), 2)
        self.assertEqual(all_books[-1].isbn, new_isbn.isbn)

    def test_add_book_isbn_exists_only_books_added(self):
        """
        ISBN 존재 → books.txt만 추가
        조건:
            기존 ISBN07(title, author 일치)
        입력:
            title="Computer Science", author="Elon musk"
        기대:
            - ISBNRepository는 변경 없음
            - books.txt만 추가됨
        """
        # when
        self.service.add_book("Computer Science", "Elon musk")

        # then
        # ISBN 수 변함 없음
        all_isbns = self.isbn_repo.data
        self.assertEqual(len(all_isbns), 1)

        # books.txt 수 증가
        all_books = self.book_repo.data
        self.assertEqual(len(all_books), 2)

        # 마지막 book의 isbn은 기존 ISBN07이어야 함
        self.assertEqual(all_books[-1].isbn, "ISBN07")