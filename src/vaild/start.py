
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

def is_available_user_id(user_id: str) -> bool:
    #todo: DB 조회해서 중복 검사
    return True

def is_valid_password(password: str) -> bool:
    """
    비밀번호 유효성 검사
    - 영문자, 숫자, 특수문자 포함 8자리 이상이어야 합니다.
    :param password:
    :return:
    """
    #todo : 정규식으로 검사
    return True

def is_valid_email(email: str) -> bool:
    """
    이메일 유효성 검사
    - 기본적인 형식 검사
    :param email:
    :return:
    """
    #todo : 정규식으로 검사
    return True