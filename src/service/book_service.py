from src.vaild.user import exist_book_title


class BookService:
    def __init__(self, app):
        self.app = app

    def search_book_by_title(self, title_keyword):
        if not exist_book_title(app=self.app, title=title_keyword):
            print("목록에 존재하지 않는 도서입니다.!! 올바른 제목을 입력하세요.")
            return None

        results = [book for book in self.app.books.data if title_keyword.lower() in book.title.lower()]
        return results

# def search_prompt(app: AppContext) -> None:
#     while True:
#         keyword = input_with_validation(
#             "검색할 책 제목을 입력하세요 : ",
#             [
#                 # 알파벳과 숫자 그리고 공백만
#                 (lambda v: all(ch.isalnum() or ch.isspace() for ch in v), "제목에는 하이픈(-) 및 기타 특수문자는 포함되어서는 안 됩니다!! 올바른 제목을 입력하세요."),
#                 # 공백이 2개 이상 연속으로 포함되어 있는지 검사
#                 (lambda v: '  ' not in v, "공백이 너무 많습니다!! 올바른 제목을 입력하세요."),
#                 # 정규식
#                 (is_valid_book_title, "잘못된 입력입니다!! 올바른 제목을 입력하세요."),
#             ]
#         )
#         if keyword:
#             break
#     if not exist_book_title(app=app, title=keyword):
#         print("목록에 존재하지 않는 도서입니다.!! 올바른 제목을 입력하세요.")
#         return None
#
#     results = [book for book in app.books.data if keyword.lower() in book.title.lower()]
#     for book in results:
#         if any(borrow.book_id == book.book_id for borrow in app.borrow.data):
#             print(f"대출중 | {book.book_id}")
#         else:
#             print(f"대여가능 | {book.book_id}")
#     return None