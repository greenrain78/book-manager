from src.controller.prompt import PromptType
from src.prompt.common import yes_no_prompt


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
