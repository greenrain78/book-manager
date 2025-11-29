from src.core.valid import input_with_validation
from src.prompt.common import yes_no_prompt
from src.service.book_service import BookService
from src.service.borrow_service import BorrowService
from src.vaild.user import is_vaild_book_id


# 대출
def borrow_prompt(book_service: BookService, borrow_service: BorrowService) -> None:
    while True:
        book_id = input_with_validation(
            "대출할 책의 고유번호를 입력하세요 :",
            [
                (lambda v: ' ' not in v, "고유번호는 공백을 포함하지 않습니다"),
                (is_vaild_book_id, "존재하지 않는 고유번호입니다!! 올바른 번호를 입력하세요."),
            ]
        )
        if book_id:
            break

    if not book_service.search_book_by_id(book_id):
        print("존재하지 않는 고유번호입니다!! 올바른 번호를 입력하세요.")
        return None

    if borrow_service.is_book_borrowed(book_id):
        print("이미 대출중인 도서입니다!! 다른 책을 입력하세요.")
        return None

    #todo 연체중인 경우
    #todo 제제중인 경우
    #todo 3회 이상 대출한 경우

    # 도서 목록에서 해당 ID의 도서 찾기
    book = book_service.search_book_by_id(book_id)
    due_date = borrow_service.borrow_book(book_id)
    # 대출 처리
    print(f"“{book.title}” 이 대출되었습니다. 반납기한은 {due_date}입니다.")

    return None


def return_prompt(book_service: BookService, borrow_service: BorrowService) -> None:
    # 대출중인 내역 조회
    borrowed_books = borrow_service.has_unreturned_books()
    if not borrowed_books:
        print(f"현재 대출한 도서가 없습니다.")
        return None
    print("[대출 중인 도서 정보] ")
    for borrow in borrowed_books:
        book = book_service.search_book_by_id(book_id=borrow.book_id)
        print(f"제목: {book.title}")
        print(f"저자: {book.author}")

    while True:
        book_id = input_with_validation(
            "반납할 책의 고유번호를 입력해주세요:",
            [
                (lambda v: ' ' not in v, "고유번호는 공백을 포함하지 않습니다"),
                (is_vaild_book_id, "존재하지 않는 고유번호입니다!! 올바른 번호를 입력하세요."),
            ]
        )
        if book_id:
            break

    # borrowed_books
    borrow = next((b for b in borrowed_books if b.book_id == book_id), None)
    if not borrow:
        print("잘못된 값을 입력했습니다.") # 어색하지만 기획서 대로 진행
        return None

    confirm = yes_no_prompt(f"정말 반납하시겠습니까? (Y/N):")
    if confirm:
        borrow_service.return_book(borrow=borrow)
        print(f"정상적으로 반납이 완료되었습니다.")
    else:
        print(f"사용자가 반납을 취소했습니다.")
    return None

# 대출
# def borrow_prompt1(app: AppContext) -> None:
#     while True:
#         book_id = input_with_validation(
#             "대출할 책의 고유번호를 입력하세요 :",
#             [
#                 (lambda v: ' ' not in v, "고유번호는 공백을 포함하지 않습니다"),
#                 (is_vaild_book_id, "존재하지 않는 고유번호입니다!! 올바른 번호를 입력하세요."),
#             ]
#         )
#         if book_id:
#             break
#
#     if not exist_book_id(app=app, book_id=book_id):
#         print("존재하지 않는 고유번호입니다!! 올바른 번호를 입력하세요.")
#         return None
#
#     if is_book_borrowed(app=app, book_id=book_id):
#         print("이미 대출중인 도서입니다!! 다른 책을 입력하세요.")
#         return None
#
#     # 반납하지 않은 책이 있는지 검사
#     if any(borrow.user_id == app.current_user.user_id for borrow in app.borrow.data):
#         print("반납하지 않은 책이 존재합니다!! 반납 후 대출 가능합니다.")
#         return None
#
#     # 도서 목록에서 해당 ID의 도서 찾기
#     book = next((b for b in app.books.data if str(b.book_id) == book_id), None)
#
#     due_date = (app.current_date + app.borrow_period).strftime("%Y-%m-%d")
#     app.borrow.insert(Borrow(
#         book_id=book.book_id,
#         user_id=app.current_user.user_id,
#         borrow_date=app.current_date.strftime("%Y-%m-%d"),
#         due_date=due_date
#     ))
#     # 대출 처리
#     print(f"“{book.title}” 이 대출되었습니다. 반납기한은 {due_date}입니다.")
#
#     return None
# def return_prompt(app: AppContext) -> None:
#     # 대출중인 내역 조회
#     borrowed_books = [borrow for borrow in app.borrow.data if borrow.user_id == app.current_user.user_id]
#     if not borrowed_books:
#         print(f"현재 대출한 도서가 없습니다.")
#         return None
#     print("[대출 중인 도서 정보] ")
#     for borrow in borrowed_books:
#         book = next((b for b in app.books.data if b.book_id == borrow.book_id), None)
#         print(f"제목: {book.title}")
#         print(f"저자: {book.author}")
#         confirm = yes_no_prompt(f"정말 반납하시겠습니까? (Y/N):")
#         if confirm:
#             app.borrow.delete(book_id=book.book_id)
#             app.borrow_history.insert(BorrowHistory(
#                 book_id=book.book_id,
#                 user_id=app.current_user.user_id,
#                 borrow_date=borrow.borrow_date,
#                 due_date=borrow.due_date,
#                 return_date=app.current_date.strftime("%Y-%m-%d")
#             ))
#             print(f"정상적으로 반납이 완료되었습니다.")
#         else:
#             print(f"사용자가 반납을 취소했습니다.")
#     return None
#



#
# def user_prompt_old(app: AppContext) -> None:
#     while True:
#         print(f"UserPrompt")
#         print(f"1. 검색")
#         print(f"2. 대출")
#         print(f"3. 반납")
#         print(f"4. 로그아웃")
#         choice = input("명령어를 입력하세요: ").strip()
#         if choice == '1':
#             search_prompt(app=app)
#         elif choice == '2':
#             borrow_prompt(app=app)
#         elif choice == '3':
#             return_prompt(app=app)
#         elif choice == '4':
#             confirm = yes_no_prompt(f"정말 로그아웃하시겠습니까? (Y/N):")
#             if confirm:
#                 break
#         else:
#             print("잘못된 입력입니다!! 1,2,3,4 중 하나를 입력하세요.")
#
#     # 로그아웃 처리 - main prompt로 복귀
#     return None



# def search_prompt(app: AppContext) -> None:
#
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