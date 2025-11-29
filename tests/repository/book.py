import os
import tempfile
import unittest

from src.repository.manager import BooksRepository


class TestBooksRepository(unittest.TestCase):

    def setUp(self):
        """
        테스트용 임시 파일 생성 (영문 데이터)
        파일 형식: book_id | isbn
        """
        self.tmp = tempfile.NamedTemporaryFile(delete=False, mode="w+")
        self.path = self.tmp.name

        self.tmp.write("001|ISBN01\n")
        self.tmp.write("002|ISBN02\n")
        self.tmp.close()

    def tearDown(self):
        """
        테스트 종료 후 파일 삭제
        """
        os.unlink(self.path)

    def test_load_all(self):
        """
        파일 로드가 정상적으로 이루어지는지 확인
        """
        repo = BooksRepository(self.path)

        self.assertEqual(len(repo.data), 2)
        self.assertEqual(repo.data[0].book_id, "001")
        self.assertEqual(repo.data[0].isbn, "ISBN01")

    def test_insert(self):
        """
        새로운 도서 추가 후 저장 여부 확인
        """
        repo = BooksRepository(self.path)

        repo.insert(isbn="ISBN03")

        self.assertEqual(len(repo.data), 3)
        self.assertEqual(repo.data[-1].isbn, "ISBN03")

        repo2 = BooksRepository(self.path)
        self.assertEqual(len(repo2.data), 3)
        self.assertEqual(repo2.data[-1].book_id, "003")

    def test_delete(self):
        """
        특정 book_id 삭제 후 정상적으로 제거되는지 확인
        """
        repo = BooksRepository(self.path)

        repo.delete("001")

        self.assertEqual(len(repo.data), 1)
        self.assertEqual(repo.data[0].book_id, "002")

        repo2 = BooksRepository(self.path)
        self.assertEqual(len(repo2.data), 1)

    def test_modify(self):
        """
        도서 정보 수정 후 저장 여부 확인 (isbn만 사용)
        isbn 수정은 없음
        """
        pass

    def test_invalid_format_raises(self):
        """
        필드가 2개가 아니면 오류가 발생해야 함
        """
        bad_tmp = tempfile.NamedTemporaryFile(delete=False, mode="w+")
        path = bad_tmp.name

        bad_tmp.write("BROKEN_LINE\n")          # 파이프 없음 → 필드 1개 → 오류 발생해야 함
        bad_tmp.close()

        with self.assertRaises(RuntimeError):
            BooksRepository(path)

        os.unlink(path)

    def test_invalid_format_raises2(self):
        """
        필드가 2개가 아니면 오류가 발생해야 함
        """
        bad_tmp = tempfile.NamedTemporaryFile(delete=False, mode="w+")
        path = bad_tmp.name

        bad_tmp.write("001|ISBN01|EXTRA_FIELD\n")   # 파이프(|) 2개 → 필드 3개 → 오류 발생해야 함
        bad_tmp.close()

        with self.assertRaises(RuntimeError):
            BooksRepository(path)

        os.unlink(path)

    def test_blank_line_raises(self):
        """
        빈 줄은 오류가 발생해야 함
        """
        bad_tmp = tempfile.NamedTemporaryFile(delete=False, mode="w+")
        path = bad_tmp.name

        bad_tmp.write("\n")
        bad_tmp.close()

        with self.assertRaises(RuntimeError):
            BooksRepository(path)

        os.unlink(path)

