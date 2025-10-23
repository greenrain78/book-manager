from src.context import AppContext
from src.core.valid import input_with_validation


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
            print("대출 선택")
            #todo 대출 프롬프트 구현
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
        print(f"대여가능 | {book.book_id}")

    return None
