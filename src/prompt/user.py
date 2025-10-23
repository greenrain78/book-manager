from src.context import AppContext
from src.core.valid import input_with_validation
from src.repository.entity import Borrow
from src.vaild.user import is_book_borrowed


def user_prompt(app: AppContext) -> None:
    while True:
        print(f"UserPrompt")
        print(f"1. 검색")
        print(f"2. 대출")
        print(f"3. 반납")
        print(f"4. 로그아웃")
        choice = input("명령어를 입력하세요: ").strip()
        if choice == '1':
            search_prompt(app=app)
        elif choice == '2':
            borrow_prompt(app=app)
        elif choice == '3':
            print("반납 선택")
            #todo 반납 프롬프트 구현
        elif choice == '4':
            confirm = input("정말 로그아웃하시겠습니까? (Y/N): ").strip()
            if confirm == 'y':
                break
        else:
            print("잘못된 입력입니다!! 1,2,3,4 중 하나를 입력하세요.")

    # 로그아웃 처리 - main prompt로 복귀
    return None


def search_prompt(app: AppContext) -> None:

    while True:
        keyword = input_with_validation(
            "검색할 책 제목을 입력하세요 : ",
            [
                # (lambda v: len(v) > 0, "검색어는 비어 있을 수 없습니다."
                # 제목에는 하이픈(-) 및 기타 특수문자는 포함되어서는 안 됩니다!! 올바른 제목을 입력하세요.
                # 공백이 너무 많습니다!! 올바른 제목을 입력하세요.
                # 목록에 존재하지 않는 도서입니다.!! 올바른 제목을 입력하세요.

                #todo 검증 함수 추가
            ]
        )
        if keyword:
            break

    results = [book for book in app.books.data if keyword in book.title]
    for book in results:
        if any(borrow.book_id == book.book_id for borrow in app.borrow.data):
            print(f"대출중 | {book.book_id}")
        else:
            print(f"대여가능 | {book.book_id}")

    return None

# 대출
def borrow_prompt(app: AppContext) -> None:
    while True:
        book_id = input_with_validation(
            "대출할 책의 고유번호를 입력하세요 :",
            [
                # 존재하지 않는 고유번호입니다!! 올바른 번호를 입력하세요.
                (lambda v: not is_book_borrowed(app, v), "해당 도서는 이미 대출중입니다!! 다른 책을 입력하세요."),
                #todo 검증 함수 추가
            ]
        )
        if book_id:
            break
    #todo 현재 사용자가 이미 대출한 책이 있는지 검사
    # 반납하지 않은 책이 존재합니다!! 반납 후 대출 가능합니다.

    # 도서 목록에서 해당 ID의 도서 찾기
    book = next((b for b in app.books.data if str(b.book_id) == book_id), None)

    due_date = (app.current_date + app.borrow_period).strftime("%Y-%m-%d")
    app.borrow.insert(Borrow(
        book_id=book.book_id,
        user_id=app.current_user.user_id,
        borrow_date=app.current_date.strftime("%Y-%m-%d"),
        due_date=due_date
    ))
    # 대출 처리
    print(f"“{book.title}” 이 대출되었습니다. 반납기한은 {due_date}입니다.")

    return None