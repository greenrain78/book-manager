# y N 입력 프롬프트
def yes_no_prompt(prompt: str, error_msg: str = "잘못된 입력입니다. 'y' 또는 'n'을 입력하세요.") -> bool:
    """
    Y/N 입력 프롬프트
    :param prompt:
    :param error_msg:
    :return:
    """
    while True:
        choice = input(f"{prompt}").strip().lower()
        if choice in ['y', 'n']:
            return choice == 'y'
        else:
            print(error_msg)
