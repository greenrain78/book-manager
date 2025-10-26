import os
from typing import Callable, List, Any, Iterable, Dict

from src.repository.entity import User, Book, Borrow, BorrowHistory


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
        self.data.append(user)
        self.save_all()

class BooksRepository(BaseRepository):
    def __init__(self, path: str):
        super().__init__(path, expected_fields=3, factory_from_fields=Book.from_fields)

    def insert(self, book: Book) -> None:
        self.data.append(book)
        self.save_all()

    def get_next_id(self):
        if not self.data:
            return "001"
        max_id = max(int(book.book_id) for book in self.data)
        return f"{max_id + 1:03d}"

    def delete(self, book_id: str) -> None:
        self.data = [b for b in self.data if b.book_id != book_id]
        self.save_all()

    def modify(self, book_id: str, new_title: str, new_author: str) -> None:
        for book in self.data:
            if book.book_id == book_id:
                book.title = new_title
                book.author = new_author
                break
        self.save_all()

class BorrowRepository(BaseRepository):
    def __init__(self, path: str):
        super().__init__(path, expected_fields=4, factory_from_fields=Borrow.from_fields)

    def insert(self, borrow: Borrow) -> None:
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

