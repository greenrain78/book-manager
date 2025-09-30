import os


def clear_prompt():
    os.system('cls')


# y N 입력 프롬프트
def yes_no_prompt(prompt: str) -> bool:
    while True:
        choice = input(f"{prompt} (y/n): ").strip().lower()
        if choice in ['y', 'n']:
            return choice == 'y'
        else:
            print("잘못된 입력입니다. 'y' 또는 'n'을 입력하세요.")
