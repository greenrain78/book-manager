from src.context import AppContext
from src.core.valid import input_with_validation
from src.prompt.common import yes_no_prompt
from src.repository.entity import Book
from src.vaild.user import is_valid_book_title, is_vaild_author, exist_book_id


def admin_prompt(app: AppContext) -> None:
    """
    :param app:
    :return:
    """
    while True:
        print(f"Admin")
        print(f"1. 도서 추가")
        print(f"2. 도서 삭제")
        print(f"3. 도서 수정")
        print(f"4. 로그아웃")
        choice = input("명령어를 입력하세요: ").strip()
        if choice == '1':
            print("도서 추가 선택")
            add_book_prompt(app=app)
        elif choice == '2':
            print("도서 삭제 선택")
            delete_book_prompt(app=app)
        elif choice == '3':
            print("도서 수정 선택")
            modify_book_prompt(app=app)
        elif choice == '4':
            break
        else:
            print("입력에 해당하는 명령어가 없습니다. 다시 입력해 주세요.")

    # 로그아웃 처리 - main prompt로 복귀
    return None

def add_book_prompt(app: AppContext) -> None:
    """
    도서 추가 프롬프트
    :param app:
    :return:
    """

    while True:
        title = input_with_validation(
            "도서명을 입력해주세요: ",
            [
                # 도서명은 한글자 이상 입력해야합니다!!
                (lambda v: len(v.strip()) > 0, "도서명은 한글자 이상 입력해야합니다!!"),
                # 도서명은 불필요한 공백이나 특수문자를 포함하지 않아야 합니다.
                (lambda v: all(ch.isalnum() or ch.isspace() for ch in v), "도서명은 불필요한 공백이나 특수문자를 포함하지 않아야 합니다."),
                # 유효한 도서 제목인지 검사
                (is_valid_book_title, "잘못된 입력입니다!! 올바른 제목을 입력하세요."),
            ]
        )
        if title:
            break

    while True:
        author = input_with_validation(
            "저자를 입력해주세요:",
            [
                # 저자는 한글자 이상 입력해야합니다!!
                (lambda v: len(v.strip()) > 0, "저자는 한글자 이상 입력해야합니다!!"),
                # 저자는 불필요한 공백이나 특수문자를 포함하지 않아야 합니다.
                (lambda v: all(ch.isalnum() or ch.isspace() for ch in v), "저자는 불필요한 공백이나 특수문자를 포함하지 않아야 합니다."),
                # 유효한 저자명인지 검사
                (is_vaild_author, "잘못된 입력입니다!! 올바른 저자를 입력하세요."),
            ]
        )
        if author:
            break

    print(f"[추가할 도서 정보]")
    print(f"도서명: {title}")
    print(f"저자: {author}")
    confirm = yes_no_prompt(f"정말 추가 하시겠습니까?(Y,N):")
    if confirm:
        app.books.insert(Book(book_id=app.books.get_next_id(), title=title, author=author))
        print(f"해당 도서를 추가했습니다.")
    else:
        print(f"해당 도서를 추가하지 않았습니다.")
    return None

def delete_book_prompt(app: AppContext) -> None:
    """
    도서 삭제 프롬프트
    :param app:
    :return:
    """
    while True:
        book_id = input_with_validation(
            "삭제할 도서의 고유번호(BookId)를 입력하세요:",
            [
                # 고유번호는 숫자 3자리 입니다. EX:001,011,111
                (lambda v: v.isdigit() and len(v) == 3, "고유번호는 숫자 3자리 입니다. EX:001,011,111"),
                # 고유번호는 공백을 포함하지 않습니다
                (lambda v: ' ' not in v, "고유번호는 공백을 포함하지 않습니다"),
                # 존재하는 도서 ID인지 검사
                (lambda v: exist_book_id(app=app, book_id=v), "목록에 존재하지 않는 도서입니다.!! 올바른 고유번호를 입력하세요."),
            ]
        )
        if book_id:
            break

    book = next((b for b in app.books.data if b.book_id == book_id), None)

    print(f"[삭제할 도서 정보]")
    print(f"도서명: {book.title}")
    print(f"저자: {book.author}")
    confirm = yes_no_prompt(f"정말 삭제 하시겠습니까?(Y,N):")
    if confirm:
        app.books.delete(book_id=book_id)
        print(f"해당 도서를 삭제했습니다.")
    else:
        print(f"해당 도서를 삭제하지 않았습니다.")
    return None

def modify_book_prompt(app: AppContext) -> None:
    """
    도서 수정 프롬프트
    :param app:
    :return:
    """

    while True:
        book_id = input_with_validation(
            "수정할 도서의 고유번호(BookId)를 입력하세요:",
            [
                # 고유번호는 숫자 3자리 입니다. EX:001,011,111
                (lambda v: v.isdigit() and len(v) == 3, "고유번호는 숫자 3자리 입니다. EX:001,011,111"),
                # 고유번호는 공백을 포함하지 않습니다
                (lambda v: ' ' not in v, "고유번호는 공백을 포함하지 않습니다"),
                # 존재하는 도서 ID인지 검사
                (lambda v: exist_book_id(app=app, book_id=v), "목록에 존재하지 않는 도서입니다.!! 올바른 고유번호를 입력하세요."),
            ]
        )
        if book_id:
            break

    book = next((b for b in app.books.data if b.book_id == book_id), None)
    print(f"[수정할 도서 정보]")
    print(f"도서명: {book.title}")
    print(f"저자: {book.author}")

    # 수정된 도서
    while True:
        modified_book = input_with_validation(
            "새로운 도서명과 저자를 [도서명 “|” 저자] 형식으로 입력하세요:",
            [
                # 정확히 ' | ' 구분자 1개만 허용
                (lambda s: s.count("|") == 1, "[도서명 | 저자] 형식으로 입력해주세요."),
                # 제목/저자 모두 비어 있지 않아야 함
                (lambda s: all(p.strip() for p in s.split("|", 1)),
                 "도서명과 저자는 각각 1자 이상이어야 합니다. 다시 입력해주세요."),
                # 도서명 유효성 검사
                (lambda s: is_valid_book_title(s.split("|", 1)[0]),
                 "잘못된 입력입니다!! 올바른 제목을 입력하세요."),
                # 저자명 유효성 검사
                (lambda s: is_vaild_author(s.split("|", 1)[1]),
                 "잘못된 입력입니다!! 올바른 저자를 입력하세요."),
            ]
        )
        if modified_book:
            break

    new_title, new_author = [part.strip() for part in modified_book.split("|", 1)]

    print(f"변경 전: {book.title} {book.author}")
    print(f"변경 후: {new_title} {new_author}")
    confirm = yes_no_prompt(f"정말 수정하시겠습니까?(Y,N):")
    if confirm:
        app.books.modify(book_id=book_id, new_title=new_title, new_author=new_author)
        print(f"해당 도서를 수정했습니다.")
    else:
        print(f"해당 도서를 수정하지 않았습니다.")
    return None