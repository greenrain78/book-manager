import unittest
import tempfile
import os

from src.repository.entity import Category
from src.repository.manager import CategoryRepository


class TestCategoryRepository(unittest.TestCase):

    def setUp(self):
        """
        테스트용 임시 파일 생성
        형식: cat_id|cat_name
        """
        self.tmp = tempfile.NamedTemporaryFile(delete=False, mode="w+")
        self.path = self.tmp.name

        self.tmp.write("CAT00|uncategorized\n")
        self.tmp.write("CAT01|os\n")
        self.tmp.write("CAT02|db\n")
        self.tmp.write("CAT11|graphics\n")
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
        repo = CategoryRepository(self.path)

        self.assertEqual(len(repo.data), 4)
        self.assertEqual(repo.data[0].cat_id, "CAT00")
        self.assertEqual(repo.data[0].cat_name, "uncategorized")

    def test_insert(self):
        """
        새 카테고리 추가 후 저장 확인
        """
        repo = CategoryRepository(self.path)

        new_cat = Category(cat_id="CAT50", cat_name="cloud")
        repo.insert(new_cat)

        self.assertEqual(len(repo.data), 5)
        self.assertEqual(repo.data[-1].cat_name, "cloud")

        repo2 = CategoryRepository(self.path)
        self.assertEqual(len(repo2.data), 5)
        self.assertEqual(repo2.data[-1].cat_id, "CAT50")

    def test_delete(self):
        """
        카테고리 삭제 기능 확인
        """
        repo = CategoryRepository(self.path)
        repo.delete("CAT01")

        self.assertEqual(len(repo.data), 3)
        self.assertFalse(any(item.cat_id == "CAT01" for item in repo.data))

        repo2 = CategoryRepository(self.path)
        self.assertEqual(len(repo2.data), 3)

    def test_modify(self):
        """
        카테고리 이름 수정 후 반영 여부 확인
        """
        repo = CategoryRepository(self.path)

        repo.modify("CAT02", new_name="database")

        updated = repo.data[2]
        self.assertEqual(updated.cat_name, "database")

        repo2 = CategoryRepository(self.path)
        self.assertEqual(repo2.data[2].cat_name, "database")

    def test_find(self):
        """
        cat_id로 카테고리 조회
        """
        repo = CategoryRepository(self.path)
        item = repo.find("CAT11")

        self.assertIsNotNone(item)
        self.assertEqual(item.cat_name, "graphics")

    def test_find_by_name(self):
        """
        이름 검색 기능 테스트
        """
        repo = CategoryRepository(self.path)

        results = repo.find_by_name("os")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].cat_id, "CAT01")

    def test_invalid_format_raises(self):
        """
        필드 2개가 아니면 오류 발생해야 함
        """
        tmp = tempfile.NamedTemporaryFile(delete=False, mode="w+")
        path = tmp.name

        # 파이프(|) 개수 부족 → 필드 1개 → 오류
        tmp.write("CAT01\n")
        tmp.close()

        with self.assertRaises(RuntimeError):
            CategoryRepository(path)

        os.unlink(path)

    def test_blank_line_raises(self):
        """
        빈 줄 존재 시 오류 발생해야 함
        """
        tmp = tempfile.NamedTemporaryFile(delete=False, mode="w+")
        path = tmp.name

        tmp.write("\n")
        tmp.close()

        with self.assertRaises(RuntimeError):
            CategoryRepository(path)

        os.unlink(path)


if __name__ == "__main__":
    unittest.main()
