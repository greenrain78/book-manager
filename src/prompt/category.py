from logging import getLogger

from src.core.valid import input_with_validation
from src.service.book_service import BookService
from src.service.cat_service import CategoryService

log = getLogger(__name__)

def add_category_prompt(cat_service: CategoryService) -> None:
    """
    카테고리 추가 프롬프트.
    """
    # 카테고리 20개
    # 카테고리가 너무 많습니다.
    # 도서가 20권인지 확인
    if len(cat_service.cat_repo.data) >= 20:
        print("카테고리가 너무 많습니다.")
        return None

    while True:
        cat_name = input_with_validation(
            "추가할 카테고리명을 입력해주세요: ",
            [
                # uncategorized는 카테고리명으로 추가할 수 없습니다. 다시입력해주세요.
                (lambda x: x != "uncategorized", "uncategorized는 카테고리명으로 추가할 수 없습니다. 다시입력해주세요."),
                # 카테고리명은 공백을 포함하지않습니다. 다시 입력해주세요.
                (lambda x: ' ' not in x, "카테고리명은 공백을 포함하지않습니다. 다시 입력해주세요."),
                # 카테고리명은 로마자 소문자만 입력받을 수 있습니다. 다시 입력해주세요.
                (lambda x: x.islower() and x.isalpha(), "카테고리명은 로마자 소문자만 입력받을 수 있습니다. 다시 입력해주세요."),
                # 이미 존재하는 카테고리명입니다. 다시 입력해주세요.
                (lambda x: not cat_service.category_exists(x), "이미 존재하는 카테고리명입니다. 다시 입력해주세요."),
            ],
            strip=False
        )
        if cat_name:
            break

    # 추가될 카테고리ID와 이름
    # CAT02␣computer

    cat = cat_service.add_category(cat_name)

    print(f"추가될 카테고리ID와 이름")
    print(f"{cat.cat_id} {cat.cat_name}")
    print(f"성공적으로 추가했습니다.")


def delete_category_prompt(cat_service: CategoryService) -> None:
    """
    카테고리 삭제 프롬프트.
    """
    while True:
        cat_name = input_with_validation(
            "삭제할 카테고리명을 입력해주세요: ",
            [
                # 카테고리명은 공백을 포함하지않습니다. 다시 입력해주세요.
                (lambda x: ' ' not in x, "카테고리명은 공백을 포함하지않습니다. 다시 입력해주세요."),
                # 카테고리명은 로마자 소문자만 입력받을 수 있습니다. 다시 입력해주세요.
                (lambda x: x.islower() and x.isalpha(), "카테고리명은 로마자 소문자만 입력받을 수 있습니다. 다시 입력해주세요."),
            ],
            strip=False
        )
        if cat_name:
            break
    if cat_name == "uncategorized":
        print("uncategorized는삭제할 수 없습니다.")
        return

    cat = cat_service.search_category_by_name(cat_name)
    if not cat:
        print("존재하지 않는 카테고리입니다.")
        return

    for isbn in cat_service.isbn_repo.data:
        # 현재 카테고리ID 목록에서 삭제할 카테고리ID 제거
        current_cat_ids = isbn.cat_id.split(';')
        if not cat.cat_id in current_cat_ids:
            continue # 없으면 패스
        if cat.cat_id in current_cat_ids:
            current_cat_ids.remove(cat.cat_id)
        # 카테고리가 하나도 없으면 uncategorized 부여
        if not current_cat_ids:
            current_cat_ids.append("CAT00")
        isbn.cat_id = ';'.join(current_cat_ids)
    cat_service.isbn_repo.save_all()

    cat_service.cat_repo.delete(cat.cat_id)

    print(f"삭제대상 카테고리")
    print(f"{cat.cat_id} {cat.cat_name}")
    print(f"해당 카테고리를 삭제했습니다.")

def merge_category_prompt(cat_service: CategoryService) -> None:
    """
    카테고리 병합 프롬프트.
    """
    # 병합할 카테고리명을 입력해주세요
    # 카테고리1:
    # 카테고리2:

    while True:
        cat_name1 = input_with_validation(
            "병합할 카테고리명을 입력해주세요\n카테고리1: ",
            [
                # 카테고리명은 공백을 포함하지않습니다. 다시 입력해주세요.
                (lambda x: ' ' not in x, "카테고리명은 공백을 포함하지않습니다. 다시 입력해주세요."),
                # 카테고리명은 로마자 소문자만 입력받을 수 있습니다. 다시 입력해주세요.
                (lambda x: x.islower() and x.isalpha(), "카테고리명은 로마자 소문자만 입력받을 수 있습니다. 다시 입력해주세요."),

            ],
            strip=False
        )
        if cat_name1 == "uncategorized":
            print("uncategorized는 병합할 수 없습니다.")
            return

        if not cat_service.category_exists(cat_name1):
            print("존재하지 않는 카테고리명입니다.")
            return

        if cat_name1:
            break


    while True:
        cat_name2 = input_with_validation(
            "카테고리2: ",
            [
                # 카테고리명은 공백을 포함하지않습니다. 다시 입력해주세요.
                (lambda x: ' ' not in x, "카테고리명은 공백을 포함하지않습니다. 다시 입력해주세요."),
                # 카테고리명은 로마자 소문자만 입력받을 수 있습니다. 다시 입력해주세요.
                (lambda x: x.islower() and x.isalpha(), "카테고리명은 로마자 소문자만 입력받을 수 있습니다. 다시 입력해주세요."),
                # 카테고리1과 동일한 카테고리명입니다. 다시 입력해주세요.
                (lambda x: x != cat_name1, "카테고리1과 동일한 카테고리명입니다. 다시 입력해주세요."),
            ],
            strip=False
        )
        if cat_name2 == "uncategorized":
            print("uncategorized는 병합할 수 없습니다.")
            return
        if not cat_service.category_exists(cat_name2):
            print("존재하지 않는 카테고리명입니다.")
            return

        if cat_name2:
            break
    while True:
        new_cat_name = input_with_validation(
            "새로운 카테고리명을 입력해주세요: ",
            [
                # 카테고리명은 공백을 포함하지않습니다. 다시 입력해주세요.
                (lambda x: ' ' not in x, "카테고리명은 공백을 포함하지않습니다. 다시 입력해주세요."),
                # 카테고리명은 로마자 소문자만 입력받을 수 있습니다. 다시 입력해주세요.
                (lambda x: x.islower() and x.isalpha(), "카테고리명은 로마자 소문자만 입력받을 수 있습니다. 다시 입력해주세요."),
                # 이미 존재하는 카테고리명입니다. 다시 입력해주세요.
                (lambda x: not cat_service.category_exists(x), "이미 존재하는 카테고리명입니다. 다시 입력해주세요."),
            ],
            strip=False
        )
        if new_cat_name == "uncategorized":
            print("uncategorized는 카테고리명으로 사용할 수 없습니다.")
            return
        if new_cat_name:
            break

    new_cat = cat_service.merge_category(new_cat_name, cat_name1, cat_name2)
    print(f"통합할 카테고리는 {cat_name1} | {cat_name2}이고")
    print(f"신설된 카테고리는 {new_cat.cat_id} | {new_cat.cat_name}입니다.")
    print(f"성공적으로 병합이 완료되었습니다.")

def modify_category_prompt(cat_service: CategoryService) -> None:
    """
    카테고리 수정 프롬프트.
    """
    while True:
        cat_name = input_with_validation(
            "수정할 카테고리명을 입력해주세요: ",
            [
                # 카테고리명은 공백을 포함하지않습니다. 다시 입력해주세요.
                (lambda x: ' ' not in x, "카테고리명은 공백을 포함하지않습니다. 다시 입력해주세요."),
                # 카테고리명은 로마자 소문자만 입력받을 수 있습니다. 다시 입력해주세요.
                (lambda x: x.islower() and x.isalpha(), "카테고리명은 로마자 소문자만 입력받을 수 있습니다. 다시 입력해주세요."),
                 # uncategorized는수정할 수 없습니다.
                (lambda x: x != "uncategorized", "uncategorized는수정할 수 없습니다."),
            ],
            strip=False
        )
        if cat_name:
            break
    # 존재하지 않는 카테고리명입니다.
    if not cat_service.category_exists(cat_name):
        print("존재하지 않는 카테고리명입니다.")
        return

    while True:
        new_cat_name = input_with_validation(
            "새로운 카테고리: ",
            [
                # 카테고리명은 공백을 포함하지않습니다. 다시 입력해주세요.
                (lambda x: ' ' not in x, "카테고리명은 공백을 포함하지않습니다. 다시 입력해주세요"),
                # 카테고리명은 로마자 소문자만 입력받을 수 있습니다. 다시 입력해주세요.
                (lambda x: x.islower() and x.isalpha(), "카테고리명은 로마자 소문자만 입력받을 수 있습니다. 다시 입력해주세요."),
                # uncategorized로는 수정할 수 없습니다
                (lambda x: x != "uncategorized", "uncategorized로는 수정할 수 없습니다."),
                # 이미 존재하는 카테고리명입니다. 다시 입력해주세요.
                (lambda x: not cat_service.category_exists(x), "이미 존재하는 카테고리명입니다. 다시 입력해주세요."),
            ],
            strip=False
        )
        if new_cat_name == "uncategorized":
            print("uncategorized는 수정할 수 없습니다.")
            return

        if new_cat_name:
            break

    cat = cat_service.search_category_by_name(cat_name)
    cat_service.cat_repo.modify(cat_id=cat.cat_id, new_name=new_cat_name)
    print(f"수정된 카테고리는 {cat.cat_id} | {new_cat_name} 입니다.")
    print(f"성공적으로 수정이 완료되었습니다.")

def assign_category_prompt(cat_service: CategoryService, book_service: BookService) -> None:
    """
    카테고리 부여 프롬프트.
    :param book_service:
    :param cat_service:
    :return:
    """
    if len(cat_service.cat_repo.data) == 1 and cat_service.cat_repo.data[0].cat_name == "uncategorized":
        print("카테고리가 너무 적습니다. 카테고리 추가하고 다시 시도해주세요.")
        return

    while True:
        isbn = input_with_validation(
            "카테고리를 추가할 ISBN을 입력하세요:",
            [
                #     입력에 공백을 포함할 수 없습니다. 다시입력해주세요.
                (lambda x: ' ' not in x, "입력에 공백을 포함할 수 없습니다. 다시입력해주세요."),
                # 입력형식은ISBN+숫자2개(0~9)입니다. 다시입력해주세요.
                (lambda x: x.startswith("ISBN") and len(x) == 6 and x[4:6].isdigit(), "입력형식은ISBN+숫자2개(0~9)입니다. 다시입력해주세요."),

            ],
            strip=False
        )
        isbn_obj = book_service.search_isbn(isbn)
        if not isbn_obj:
            print("존재하지 않는 ISBN입니다.")
            return
        current_cat_ids = isbn_obj.cat_id.split(';') if isbn_obj.cat_id else []
        if len(current_cat_ids) >= 3:
            print("해당 ISBN은 3개의 카테고리 보유중입니다.")
            return
        if isbn_obj:
            break

    print("현재 카테고리")
    for cat_id in current_cat_ids:
        cat = cat_service.cat_repo.find(cat_id)
        if not cat:
            continue # 이상한 경우
        print(f"{cat.cat_id} {cat.cat_name}")

    while True:
        cat_name = input_with_validation(
            "추가할 카테고리명을 입력해주세요: ",
            [
                # 카테고리명은 공백을 포함하지않습니다. 다시 입력해주세요.
                (lambda x: ' ' not in x, "카테고리명은 공백을 포함하지않습니다. 다시 입력해주세요."),
                # 카테고리명은 로마자 소문자만 입력받을 수 있습니다. 다시 입력해주세요.
                (lambda x: x.islower() and x.isalpha(), "카테고리명은 로마자 소문자만 입력받을 수 있습니다. 다시 입력해주세요."),
            ],
            strip=False
        )
        # 존재하지 않는 카테고리입니다.
        if not cat_service.category_exists(cat_name):
            print("존재하지 않는 카테고리입니다.")
            return

        # uncategorized 는 추가할 수 없습니다.
        if cat_name == "uncategorized":
            print("uncategorized 는 추가할 수 없습니다.")
            return

        if cat_name:
            break
    cat = cat_service.search_category_by_name(cat_name)
    cat_service.assign_category_to_isbn(isbn_obj=isbn_obj, cat=cat)

    print(f"해당 카테고리가 추가될 책 정보")
    print(f"제목: {isbn_obj.title}")
    print(f"저자: {isbn_obj.author}")
