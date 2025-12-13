from src.core.valid import input_with_validation
from src.service.book_service import BookService
from src.service.borrow_service import BorrowService
from src.service.cat_service import CategoryService
from src.vaild.user import is_valid_book_title


def search_by_book_prompt(book_service: BookService, borrow_service: BorrowService) -> None:
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
            ],
            strip=False,
        )
        if keyword:
            break

    isbns = book_service.search_isbn_by_title(keyword=keyword)
    if isbns is None or len(isbns) == 0:
        print("목록에 존재하지 않는 도서입니다.!! 올바른 제목을 입력하세요.")
        return None

    for isbn in isbns:
        books = book_service.read_books_by_isbn(isbn=isbn)
        for book in books:
            print(f"{book['status']} | {book['book_id']} | {book['title']} | {book['author']} | {book['category']}")
    return None

def search_by_category_prompt(book_service: BookService, cat_service: CategoryService) -> None:
    while True:
        keyword = input_with_validation(
            "검색할 카테고리명을 입력하세요(허용 표기는 !, &, | 이며 !=NOT, &=AND, |=OR를 의미함) :",
            [
                # 카테고리명은 공백을 포함하지않습니다.다시 입력해주세요.
                (lambda v: ' ' not in v, "카테고리명은 공백을 포함하지않습니다.다시 입력해주세요."),
                (lambda v: not any((v[i] == '!' and (i != 0)) for i in range(len(v))), # !가 중간이나 끝에 위치해 있으면 오류
                 "NOT앞에는 피연산자가 올 수 없습니다. 다시 입력해주세요."),
                # 괄호는 사용할 수 없습니다. 다시 입력해주세요.
                (lambda v: '(' not in v and ')' not in v, "괄호는 사용할 수 없습니다. 다시 입력해주세요."),

                # 연산자는 연속으로 사용할 수 없습니다. 다시 입력해주세요.
                (lambda v: all(
                    not (v[i] in ['&', '|', '!'] and v[i + 1] in ['&', '|', '!']) for i in range(len(v) - 1)),
                 "연산자는 연속으로 사용할 수 없습니다. 다시 입력해주세요."),

                # AND, OR은 좌우에 각각 하나의 피연산자가 존재해야 합니다. 다시 입력해주세요.
                (lambda v: all(not (v[i] in ['&', '|'] and (i == 0 or i == len(v) - 1 or v[i - 1] in ['&', '|', '!'] or v[i + 1] in ['&', '|', '!'])) for i in range(len(v))),
                 "AND, OR은 좌우에 각각 하나의 피연산자가 존재해야 합니다. 다시 입력해주세요."),

                # 카테고리명은 로마자 소문자만 입력받을 수 있습니다. 다시 입력해주세요.
                (lambda v: all(ch.islower() or ch in ['!', '&', '|'] for ch in v),
                 "카테고리명은 로마자 소문자만 입력받을 수 있습니다. 다시 입력해주세요."),

                # 허용 가능한 연산자는 !,&,|입니다. 다시 입력해주세요.
                (lambda v: all(ch.islower() or ch in ['!', '&', '|'] for ch in v), "허용 가능한 연산자는 !,&,|입니다. 다시 입력해주세요."),
            ],
            strip = False,
        )
        if keyword:
            break
    # # 기획서에 있는 내용을 충족하기 위해 동일한 연산을 2번 수행
    # # cat_service.search_category_by_name으로 조회, 연산자를 기준으로 list로 분리 후 각각 조회
    # # 존재하지 않는 카테고리명입니다
    # for token in keyword.replace('&', ' ').replace('|', ' ').split():
    #     cat = cat_service.search_category_by_name(cat_name=token)
    #     if not cat:
    #         print(f"존재하지 않는 카테고리명입니다.")
    #         return None

    # 검색 수행
    isbns = cat_service.search_by_category(expr=keyword)
    if not isbns:
        print("카테고리에 해당하는 도서가 존재하지 않습니다.")
        return None
    # 모든 books 가져오기
    books = []
    for isbn in isbns:
        books.extend(book_service.read_books_by_isbn(isbn=isbn))
    if not books:
        print("카테고리에 해당하는 도서가 존재하지 않습니다.")
        return None
    for book in books:
        print(f"{book['status']} | {book['book_id']} | {book['title']} | {book['author']} | {book['category']}")
    return None
