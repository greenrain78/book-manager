from dataclasses import asdict, dataclass
from typing import List, Dict, Any

from src.vaild.entity import validate_isbn, validate_cat_id, validate_book_title, validate_book_author, \
    validate_book_id, validate_cat_name


@dataclass
class User:
    user_id: str
    pw: str
    email: str
    penaltyDate: str

    @staticmethod
    def from_fields(fields: List[str]) -> "User":
        return User(user_id=fields[0], pw=fields[1], email=fields[2], penaltyDate=fields[3])

    def to_fields(self) -> List[str]:
        return [self.user_id, self.pw, self.email, self.penaltyDate]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class Book:
    book_id: str
    isbn: str

    def __post_init__(self):
        validate_book_id(value=self.book_id)
        validate_isbn(value=self.isbn)

    @staticmethod
    def from_fields(fields: List[str]) -> "Book":
        return Book(book_id=fields[0], isbn=fields[1])

    def to_fields(self) -> List[str]:
        return [self.book_id, self.isbn]

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


@dataclass
class ISBN:
    isbn: str
    title: str
    author: str
    cat_id: str

    def __post_init__(self):
        # 각 필드에 대한 유효성 검사 수행
        validate_isbn(value=self.isbn)
        validate_cat_id(value=self.cat_id)
        validate_book_title(value=self.title)
        validate_book_author(value=self.author)

    @staticmethod
    def from_fields(fields: List[str]) -> "ISBN":
        return ISBN(isbn=fields[0], title=fields[1], author=fields[2], cat_id=fields[3])

    def to_fields(self) -> List[str]:
        return [self.isbn, self.title, self.author, self.cat_id]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class Category:
    cat_id: str
    cat_name: str

    def __post_init__(self):
        validate_cat_id(value=self.cat_id)
        validate_cat_name(value=self.cat_name)

    @staticmethod
    def from_fields(fields: List[str]) -> "Category":
        return Category(cat_id=fields[0], cat_name=fields[1])

    def to_fields(self) -> List[str]:
        return [self.cat_id, self.cat_name]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)