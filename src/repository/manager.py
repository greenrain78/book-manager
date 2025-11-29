import os
from typing import Callable, List, Any, Iterable, Dict

from src.repository.entity import User, Book, Borrow, BorrowHistory, ISBN, Category


class BaseRepository:
    """
    개별 도메인 규칙(정규식/참조 무결성/날짜 형식)은 수행하지 않음.
    """
    def __init__(self, path: str, expected_fields: int, factory_from_fields: Callable[[List[str]], Any]):
        self.path = path
        self.expected_fields = expected_fields
        self.factory_from_fields = factory_from_fields
        self.data = []

        # 데이터 로드
        self.load_all()

    # ---- 공통 검증 ----
    def _validate_line_common(self, raw: str) -> None:
        # 라인이 비었거나(None, 공백, 빈 문자열 등) 아무 문자도 없으면 에러 발생
        if raw is None or raw.strip() == "":
            raise RuntimeError(f"필수 데이터 파일이 손상되거나 혹은 필드에 오류가있습니다. 확인 후 다시 시작해주세요.")
        # 필드 구분자(|) 개수 검사 - 파이프(|) 개수가 기대한 필드 수 -1과 일치하지 않으면 에러 발생
        if raw.count("|") != self.expected_fields - 1:
            raise RuntimeError(f"필수 데이터 파일이 손상되거나 혹은 필드에 오류가있습니다. 확인 후 다시 시작해주세요.")

    # ---- IO ----
    def load_all(self) -> None:
        if not os.path.exists(self.path):
            # 필수 데이터 파일이 존재하지 않습니다. 데이터 파일 확인 후 다시 시작해주세요..
            raise RuntimeError("필수 데이터 파일이 존재하지 않습니다. 데이터 파일 확인 후 다시 시작해주세요.")
        # 초기화
        self.data = []
        with open(self.path, "r", newline="") as fp:
            for line in fp:
                raw = line.rstrip("\r\n")
                self._validate_line_common(raw)
                fields = raw.split("|")
                self.data.append(self.factory_from_fields(fields))

    def save_all(self) -> None:
        with open(self.path, "w", newline="") as fp:
            for it in self.data:
                fields = getattr(it, "to_fields")()
                raw = "|".join(fields)
                self._validate_line_common(raw)
                fp.write(raw + "\r\n")

class UsersRepository(BaseRepository):
    def __init__(self, path: str):
        super().__init__(path, expected_fields=3, factory_from_fields=User.from_fields)

    def insert(self, user: User) -> None:
        if len(self.data) >= 20:
            raise RuntimeError("레코드 수가 20개를 초과할 수 없습니다.")
        self.data.append(user)
        self.save_all()

    def count_users(self):
        return len(self.data)


class BooksRepository(BaseRepository):
    def __init__(self, path: str):
        super().__init__(path, expected_fields=2, factory_from_fields=Book.from_fields)

    def insert(self, isbn: str) -> Book:
        book = Book(book_id=self.get_next_id(), isbn=isbn)
        if len(self.data) >= 20:
            raise RuntimeError("레코드 수가 20개를 초과할 수 없습니다.")
        self.data.append(book)
        self.save_all()
        return book

    def get_next_id(self):
        if not self.data:
            return "001"
        max_id = max(int(book.book_id) for book in self.data)
        return f"{max_id + 1:03d}"

    def delete(self, book_id: str) -> None:
        self.data = [b for b in self.data if b.book_id != book_id]
        self.save_all()

    def find_by_isbn(self, isbn: str) -> List[Book]:
        return [b for b in self.data if b.isbn == isbn]

    def find_by_id(self, book_id: str) -> Book | None:
        for b in self.data:
            if b.book_id == book_id:
                return b
        return None

class BorrowRepository(BaseRepository):
    def __init__(self, path: str):
        super().__init__(path, expected_fields=4, factory_from_fields=Borrow.from_fields)

    def insert(self, borrow: Borrow) -> None:
        if len(self.data) >= 20:
            raise RuntimeError("레코드 수가 20개를 초과할 수 없습니다.")
        self.data.append(borrow)
        self.save_all()

    def delete(self, book_id: str) -> None:
        self.data = [b for b in self.data if b.book_id != book_id] # 특정 book_id를 가진 대출 기록 삭제
        self.save_all()

class BorrowHistoryRepository(BaseRepository):
    def __init__(self, path: str):
        super().__init__(path, expected_fields=5, factory_from_fields=BorrowHistory.from_fields)

    def insert(self, borrow_history: BorrowHistory) -> None:
        self.data.append(borrow_history)
        self.save_all()



class ISBNRepository(BaseRepository):
    """
    isbn.txt 파일을 관리하는 저장소 클래스
    형식: isbn|title|author|cat_id
    필드수: 4
    """
    def __init__(self, path: str):
        super().__init__(path, expected_fields=4, factory_from_fields=ISBN.from_fields)

    def insert(self, title, author, cat_id) -> ISBN:
        isbn_obj = ISBN(isbn=self.get_next_id(), title=title, author=author, cat_id=cat_id)
        if len(self.data) >= 20:
            raise RuntimeError("레코드 수가 20개를 초과할 수 없습니다.")
        self.data.append(isbn_obj)
        self.save_all()
        return isbn_obj

    def delete(self, isbn: str) -> None:
        self.data = [item for item in self.data if item.isbn != isbn]
        self.save_all()

    def modify(self, isbn: str, new_title: str = None, new_author: str = None, new_cat_id: str = None) -> None:
        for item in self.data:
            if item.isbn == isbn:
                if new_title is not None:
                    item.title = new_title
                if new_author is not None:
                    item.author = new_author
                if new_cat_id is not None:
                    item.cat_id = new_cat_id
                break
        self.save_all()

    def find(self, isbn: str) -> ISBN | None:
        for item in self.data:
            if item.isbn == isbn:
                return item
        return None

    def find_by_title(self, keyword: str) -> List[ISBN]:
        keyword_lower = keyword.lower()
        return [item for item in self.data if keyword_lower in item.title.lower()]

    def find_by_category(self, cat_id: str) -> List[ISBN]:
        """
        카테고리 ID 기준 검색
        """
        return [item for item in self.data if item.cat_id == cat_id]

    def get_next_id(self) -> str:
        """
        ISBN을 'ISBN01' 형태로 자동 증가시키고 싶을 때 사용할 수 있는 메서드.
        """
        if not self.data:
            return "ISBN01"

        # ISBN 접두사 제거 후 숫자만 추출
        numeric_ids = []
        for item in self.data:
            # 예: ISBN01 → 1
            num = ''.join(ch for ch in item.isbn if ch.isdigit())
            if num.isdigit():
                numeric_ids.append(int(num))

        if not numeric_ids:
            return "ISBN01"

        next_num = max(numeric_ids) + 1
        return f"ISBN{next_num:02d}"

    def find_by_isbn(self, isbn: str) -> ISBN | None:
        for item in self.data:
            if item.isbn == isbn:
                return item
        return None

    def find_by_title_and_author(self, title, author):
        for item in self.data:
            if item.title == title and item.author == author:
                return item
        return None


class CategoryRepository(BaseRepository):
    """
    categories.txt 관리용 저장소
    필드수: 2
    형식: cat_id|cat_name
    """

    def __init__(self, path: str):
        super().__init__(path, expected_fields=2, factory_from_fields=Category.from_fields)

    def insert(self, category: Category) -> None:
        if len(self.data) >= 20:
            raise RuntimeError("레코드 수가 20개를 초과할 수 없습니다.")
        self.data.append(category)
        self.save_all()

    def delete(self, cat_id: str) -> None:
        self.data = [item for item in self.data if item.cat_id != cat_id]
        self.save_all()

    def modify(self, cat_id: str, new_name: str) -> None:
        for item in self.data:
            if item.cat_id == cat_id:
                item.cat_name = new_name
                break
        self.save_all()

    def find(self, cat_id: str) -> Category | None:
        for item in self.data:
            if item.cat_id == cat_id:
                return item
        return None

    def find_by_name(self, keyword: str):
        keyword_lower = keyword.lower()
        return [item for item in self.data if keyword_lower in item.cat_name.lower()]