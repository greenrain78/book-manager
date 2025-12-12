from logging import getLogger

from src.controller.prompt import PromptType
from src.prompt.common import yes_no_prompt

log = getLogger(__name__)


def main_prompt() -> PromptType:
    """
    메인 프롬프트
    :param app:
    :return:
    """
    while True:
        try:
            print(f"Main")
            print(f"1. 회원가입")
            print(f"2. 로그인")
            print(f"3. 종료")
            choice = input("명령어를 입력하세요: ").strip()
            if choice == '1':
                return PromptType.SIGNUP

            elif choice == '2':
                return PromptType.LOGIN

            elif choice == '3':
                if yes_no_prompt(f"정말 종료하시겠습니까? (Y/N):"):
                    return PromptType.EXIT
            else:
                print("잘못된 입력입니다!! 1,2,3 중 하나를 입력하세요.")
        except Exception as e:
            # 방어코드가 아닌 로깅용 코드
            log.error(f"메인 프롬프트 오류: {e}")
            print("오류가 발생했습니다!! 다시 시도하세요.")


def admin_prompt() -> PromptType:
    """
    관리자 프롬프트
    :return:
    """
    while True:
        print(f"Admin")
        print(f"1. 도서 추가")
        print(f"2. 도서 삭제")
        print(f"3. 도서 수정")
        print(f"4. 카테고리 관리")
        print(f"5. 로그아웃")

        choice = input("명령어를 입력하세요: ").strip()
        if choice == '1':
            return PromptType.ADMIN_BOOK_ADD
        elif choice == '2':
            return PromptType.ADMIN_BOOK_DELETE
        elif choice == '3':
            return PromptType.ADMIN_BOOK_MODIFY
        elif choice == '4':
            return PromptType.CATEGORY_MENU
        elif choice == '5':
            confirm = yes_no_prompt(f"정말 로그아웃하시겠습니까? (Y/N):")
            if confirm:
                return PromptType.LOGOUT
        else:
            print("입력에 해당하는 명령어가 없습니다. 다시 입력해 주세요.")


def category_prompt() -> PromptType:
    while True:
        print(f"Category Management")
        print(f"1. 카테고리 신설")
        print(f"2. 카테고리 삭제")
        print(f"3. 카테고리 병합")
        print(f"4. 카테고리 수정")
        print(f"5. 카테고리 부여")
        print(f"6. 뒤로가기")
        choice = input("명령어를 입력하세요: ").strip()
        if choice == '1':
            return PromptType.CATEGORY_ADD
        elif choice == '2':
            return PromptType.CATEGORY_DELETE
        elif choice == '3':
            return PromptType.CATEGORY_MERGE
        elif choice == '4':
            return PromptType.CATEGORY_MODIFY
        elif choice == '5':
            return PromptType.CATEGORY_ASSIGN
        elif choice == '6':
            return PromptType.ADMIN_MENU
        else:
            print("잘못된 입력입니다!! 1,2,3,4,5,6 중 하나를 입력하세요.")


def user_prompt() -> PromptType:
    while True:
        print(f"UserPrompt")
        print(f"1. 검색")
        print(f"2. 대출")
        print(f"3. 반납")
        print(f"4. 로그아웃")
        choice = input("명령어를 입력하세요: ").strip()
        if choice == '1':
            return PromptType.SEARCH_MENU
        elif choice == '2':
            return PromptType.BOOK_BORROW
        elif choice == '3':
            return PromptType.BOOK_RETURN
        elif choice == '4':
            confirm = yes_no_prompt(f"정말 로그아웃하시겠습니까? (Y/N):")
            if confirm:
                return PromptType.LOGOUT
        else:
            print("잘못된 입력입니다!! 1,2,3,4 중 하나를 입력하세요.")



def search_prompt() -> PromptType:
    while True:
        print(f"검색하고 싶은 종류를 골라주세요.")
        print(f"1. 도서 검색")
        print(f"2. 카테고리 검색")
        choice = input("명령어를 입력하세요: ").strip()
        if choice == '1':
            return PromptType.SEARCH_BOOK
        elif choice == '2':
            return PromptType.SEARCH_CATEGORY
        else:
            print("잘못된 입력입니다!! 1,2 중 하나를 입력하세요.")
