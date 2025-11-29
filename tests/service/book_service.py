import tempfile
import unittest

from src.repository.manager import BooksRepository

"""
개발의 편리성과 테스트의 용이함을 위해 service는 repository 합쳐서 통합 테스트만 진행합니다.
"""

class TestBookServiceIntegration(unittest.TestCase):

    def setUp(self):
        # 임시 파일 생성
        self.book = tempfile.NamedTemporaryFile(delete=False, mode="w+", encoding="utf-8")
        self.path1 = self.book.name
        self.isbn = tempfile.NamedTemporaryFile(delete=False, mode="w+", encoding="utf-8")
        self.path2 = self.isbn.name
        self.categories = tempfile.NamedTemporaryFile(delete=False, mode="w+", encoding="utf-8")
        self.path2 = self.categories.name

        # 테스트용 초기 데이터 작성
        # expected_fields = 3 → book_id | title | author
        self.books.write("007|ISBN07\n")
        self.temp.write("002|클린코드|로버트마틴\n")
        self.temp.close()

        # 통합 테스트: 실제 Repository + 실제 Service
        self.repo = BooksRepository(path=self.path)
        self.service = BookService(repository=self.repo)

    def tearDown(self):
        # 테스트 파일 삭제
        os.unlink(self.path)