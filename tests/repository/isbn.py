import os
import tempfile
import unittest

from src.repository.manager import ISBNRepository


class TestISBNRepository(unittest.TestCase):

    def setUp(self):
        """
        테스트용 임시 파일 생성
        형식: isbn|title|author|cat_id
        """
        self.tmp = tempfile.NamedTemporaryFile(delete=False, mode="w+")
        self.path = self.tmp.name

        self.tmp.write("ISBN01|Clean Code|Robert Martin|CAT01\n")
        self.tmp.write("ISBN02|Python Programming|John Doe|CAT02\n")
        self.tmp.close()

    def tearDown(self):
        """
        테스트 종료 후 파일 삭제
        """
        os.unlink(self.path)

    def test_load_all(self):
        """
        파일에서 모든 레코드를 정상적으로 읽어오는지 확인
        """
        repo = ISBNRepository(self.path)

        self.assertEqual(len(repo.data), 2)
        self.assertEqual(repo.data[0].isbn, "ISBN01")
        self.assertEqual(repo.data[0].title, "Clean Code")
        self.assertEqual(repo.data[0].author, "Robert Martin")
        self.assertEqual(repo.data[0].cat_id, "CAT01")

    def test_insert(self):
        """
        새 ISBN 레코드 추가 후 저장/재로드 확인
        """
        repo = ISBNRepository(self.path)

        repo.insert(title="Software Engineering", author="Alice Smith", cat_id="CAT03")

        self.assertEqual(len(repo.data), 3)
        self.assertEqual(repo.data[-1].author, "Alice Smith")

        repo2 = ISBNRepository(self.path)
        self.assertEqual(len(repo2.data), 3)
        self.assertEqual(repo2.data[-1].isbn, "ISBN03")

    def test_delete(self):
        """
        특정 ISBN 레코드 삭제 테스트
        """
        repo = ISBNRepository(self.path)
        repo.delete("ISBN01")

        self.assertEqual(len(repo.data), 1)
        self.assertEqual(repo.data[0].isbn, "ISBN02")

        repo2 = ISBNRepository(self.path)
        self.assertEqual(len(repo2.data), 1)

    def test_modify(self):
        """
        제목/저자/카테고리 수정 후 반영 여부 확인
        """
        repo = ISBNRepository(self.path)

        repo.modify("ISBN02", new_title="Python Guide", new_author="James Bond", new_cat_id="CAT99")

        updated = repo.data[1]
        self.assertEqual(updated.title, "Python Guide")
        self.assertEqual(updated.author, "James Bond")
        self.assertEqual(updated.cat_id, "CAT99")

        repo2 = ISBNRepository(self.path)
        self.assertEqual(repo2.data[1].cat_id, "CAT99")

    def test_find(self):
        """
        ISBN으로 개별 레코드 찾기
        """
        repo = ISBNRepository(self.path)
        item = repo.find("ISBN02")

        self.assertIsNotNone(item)
        self.assertEqual(item.title, "Python Programming")

    def test_find_by_title(self):
        """
        제목 검색 기능 테스트
        """
        repo = ISBNRepository(self.path)
        results = repo.find_by_title("python")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].isbn, "ISBN02")

    def test_find_by_category(self):
        """
        카테고리 기준 검색 테스트
        """
        repo = ISBNRepository(self.path)
        results = repo.find_by_category("CAT02")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].isbn, "ISBN02")

    def test_invalid_format_raises(self):
        """
        필드 4개가 아닌 잘못된 형식은 RuntimeError 발생해야 한다
        """
        tmp = tempfile.NamedTemporaryFile(delete=False, mode="w+")
        path = tmp.name

        tmp.write("ISBN01|MissingFieldsOnlyTwo\n")  # 필드 개수 부족
        tmp.close()

        with self.assertRaises(RuntimeError):
            ISBNRepository(path)

        os.unlink(path)

    def test_blank_line_raises(self):
        """
        빈 줄이 존재하면 오류 발생해야 한다
        """
        tmp = tempfile.NamedTemporaryFile(delete=False, mode="w+")
        path = tmp.name

        tmp.write("\n")
        tmp.close()

        with self.assertRaises(RuntimeError):
            ISBNRepository(path)

        os.unlink(path)

    def test_get_next_id(self):
        """
        ISBN 자동 증가 기능 테스트
        """
        repo = ISBNRepository(self.path)

        next_id = repo.get_next_id()

        # 기존: ISBN01, ISBN02 → 다음은 ISBN003
        self.assertEqual(next_id, "ISBN03")

