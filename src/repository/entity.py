from dataclasses import asdict, dataclass
from typing import List, Dict, Any


@dataclass
class User:
    user_id: str
    pw: str
    email: str

    @staticmethod
    def from_fields(fields: List[str]) -> "User":
        return User(user_id=fields[0], pw=fields[1], email=fields[2])

    def to_fields(self) -> List[str]:
        return [self.user_id, self.pw, self.email]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class Book:
    book_id: str
    title: str
    author: str

    @staticmethod
    def from_fields(fields: List[str]) -> "Book":
        return Book(book_id=fields[0], title=fields[1], author=fields[2])

    def to_fields(self) -> List[str]:
        return [self.book_id, self.title, self.author]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
@dataclass
class Borrow:
    book_id: str
    user_id: str
    borrow_date: str
    due_date: str

    @staticmethod
    def from_fields(fields: List[str]) -> "Borrow":
        return Borrow(book_id=fields[0], user_id=fields[1], borrow_date=fields[2], due_date=fields[3])

    def to_fields(self) -> List[str]:
        return [self.book_id, self.user_id, self.borrow_date, self.due_date]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class BorrowHistory:
    book_id: str
    user_id: str
    borrow_date: str
    due_date: str
    return_date: str

    @staticmethod
    def from_fields(fields: List[str]) -> "BorrowHistory":
        return BorrowHistory(
            book_id=fields[0], user_id=fields[1], borrow_date=fields[2], due_date=fields[3], return_date=fields[4]
        )

    def to_fields(self) -> List[str]:
        return [self.book_id, self.user_id, self.borrow_date, self.due_date, self.return_date]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
