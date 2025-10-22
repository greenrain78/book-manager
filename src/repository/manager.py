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
        self.data: List[Dict[str, str]] = []

        # 데이터 로드
        self.load_all()

    # ---- 공통 검증 ----
    def _validate_line_common(self, raw: str) -> None:
        # 라인이 비었거나(None, 공백, 빈 문자열 등) 아무 문자도 없으면 에러 발생
        if raw is None or raw.strip() == "":
            raise ValueError(f"[{self.path}] empty line is not allowed")
        # 필드 구분자(|) 개수 검사 - 파이프(|) 개수가 기대한 필드 수 -1과 일치하지 않으면 에러 발생
        if raw.count("|") != self.expected_fields - 1:
            raise ValueError(f"[{self.path}] invalid field delimiter count: {raw}")

    # ---- IO ----
    def load_all(self) -> None:
        # 초기화
        self.data = []
        with open(self.path, "r", encoding="utf-8", newline="") as fp:
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

class BooksRepository(BaseRepository):
    def __init__(self, path: str):
        super().__init__(path, expected_fields=3, factory_from_fields=Book.from_fields)

class BorrowRepository(BaseRepository):
    def __init__(self, path: str):
        super().__init__(path, expected_fields=4, factory_from_fields=Borrow.from_fields)

class BorrowHistoryRepository(BaseRepository):
    def __init__(self, path: str):
        super().__init__(path, expected_fields=5, factory_from_fields=BorrowHistory.from_fields)
