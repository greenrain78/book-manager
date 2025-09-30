
def is_valid_user_id(user_id: str) -> bool:
    """
    사용자 ID 유효성 검사
    - 영문자와 숫자로만 구성되어야 합니다.
    :param user_id:
    :return:
    """
    if len(user_id) < 4:
        print(f"ID가 4자리 이상이어야 합니다!!  다른 ID를 입력하세요.")
        return False
    return True

def is_valid_password(password: str) -> bool:
    """
    비밀번호 유효성 검사
    - 영문자, 숫자, 특수문자 포함 8자리 이상이어야 합니다.
    :param password:
    :return:
    """
    if len(password) < 8:
        print(f"비밀번호가 8자리 이상이어야 합니다!! 다른 비밀번호를 입력하세요.")
        return False
    has_letter = any(c.isalpha() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)
    if not (has_letter and has_digit and has_special):
        print(f"비밀번호는 영문자, 숫자, 특수문자를 모두 포함해야 합니다!! 다른 비밀번호를 입력하세요.")
        return False
    return True