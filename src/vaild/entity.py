"""
Entity 관련 유효성 검사 함수들
"""
import re


def validate_isbn(value: str) -> None:
    # 정규식: ISBN[0-9]{2}
    if not value.startswith("ISBN") or not value[4:].isdigit() or len(value[4:]) != 2:
        raise ValueError(f"Invalid ISBN format: {value!r}")
    # 공백류는 어디에도 포함 불가
    if ' ' in value or '\t' in value or '\n' in value:
        raise ValueError(f"공백류는 어디에도 포함 불가: {value!r}")


def validate_cat_id(value: str) -> None:
    # 접두사 CAT + 숫자(0-9) 2자리 (선행 0 허용)
    if not value.startswith("CAT") or not value[3:].isdigit() or len(value[3:]) != 2:
        raise ValueError(f"Invalid Category ID format: {value!r}")
    # 공백류는 어디에도 포함 불가
    if ' ' in value or '\t' in value or '\n' in value:
        raise ValueError(f"공백류는 어디에도 포함 불가: {value!r}")


def validate_book_title(value: str) -> None:
    pattern = r'^[A-Za-z0-9]+( [A-Za-z0-9]+)*$'
    if not re.match(pattern, value):
        raise ValueError(f"Invalid book title format: {value!r}")


def validate_book_author(value: str) -> None:
    pattern = r'^[A-Za-z]+( [A-Za-z]+)*$'
    if not re.match(pattern, value):
        raise ValueError(f"Invalid book author format: {value!r}")


def validate_book_id(value: str) -> None:
    pattern = r'^[0-9]{3}$'
    if not re.match(pattern, value):
        raise ValueError(f"Invalid book ID format: {value!r}")
