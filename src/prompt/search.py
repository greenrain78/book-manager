from src.core.valid import input_with_validation
from src.service.book_service import BookService
from src.vaild.user import is_valid_book_title, exist_book_title


def search_by_book_prompt(service: BookService):
    while True:
        keyword = input_with_validation(
            "검색할 책 제목을 입력하세요 : ",
            [
                # 알파벳과 숫자 그리고 공백만
                (lambda v: all(ch.isalnum() or ch.isspace() for ch in v), "제목에는 하이픈(-) 및 기타 특수문자는 포함되어서는 안 됩니다!! 올바른 제목을 입력하세요."),
                # 공백이 2개 이상 연속으로 포함되어 있는지 검사
                (lambda v: '  ' not in v, "공백이 너무 많습니다!! 올바른 제목을 입력하세요."),
                # 정규식
                (is_valid_book_title, "잘못된 입력입니다!! 올바른 제목을 입력하세요."),
            ]
        )
        if keyword:
            break
    results = service.search_book_by_title(title_keyword=keyword)
    if results is None:
        print("목록에 존재하지 않는 도서입니다.!! 올바른 제목을 입력하세요.")

    for book in results:
        if any(borrow.book_id == book.book_id for borrow in app.borrow.data):
            print(f"대출중 | {book.book_id}")
        else:
            print(f"대여가능 | {book.book_id}")
    return None

def search_by_category_prompt():
    pass