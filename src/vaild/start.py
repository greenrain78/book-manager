import re


def is_valid_user_id(user_id: str) -> bool:
    """
    사용자 ID 유효성 검사
    - 문자열 길이가 4~12자
    - 허용 문자: 로마자 대/소문자, 숫자(0-9)
    - 공백류는 어디에도 포함 불가
    - 예를 들어, “user”, “user1234”, “1234” 모두 문법적으로 올바른 ID입니다.
    - 정규식: [A-Za-z0-9]{4,12}
    :param user_id:
    :return:
    """
    # 정규식으로 검사
    pattern = re.compile(r'^[A-Za-z0-9]{4,12}$')
    if not pattern.match(user_id):
        return False

    # # 공백류 검사
    # if any(ch.isspace() for ch in user_id):
    #     return False
    #
    # # 문자열 길이 검사
    # if len(user_id) < 4 or len(user_id) > 12:
    #     return False
    #
    # # 허용 문자 검사
    # for ch in user_id:
    #     if not (ch.isalpha() or ch.isdigit()):
    #         return False
    return True # 통과

def is_available_user_id(user_id: str) -> bool:
    return True

def is_reserved_user_id(user_id: str) -> bool:
    """
    예약어 검사
    예를 들어, “Admin”, “ADMIN”은 모두 예약어이므로 금지됩니다.
    또한, “adminadmin”, “admin1234”와 같이 예약어가 포함한 모든 문자열은 금지합니다.
    :param user_id:
    :return:
    """

    reserved_words = ["admin", ]
    lower_user_id = user_id.lower()
    for word in reserved_words:
        if word in lower_user_id:
            return False

    return True

def is_valid_password(password: str) -> bool:
    """
    비밀번호 유효성 검사
    - 문자열 길이가 8자 이상
    - 허용 문자: 로마자 대/소문자, 숫자(0-9), 특수문자
    - 사용 가능한 특수문자: !, @, #, $, % ->
    - 공백류는 어디에도 포함 불가
    - 예를 들어, “pass1234”, “passpass”, “12341234” 모두  문법적으로 올바른 PW입니다.
    :param password:
    :return:
    """
    # 정규식으로 검사
    pattern = re.compile(r'^[A-Za-z0-9!@#$%]{8,}$')
    if not pattern.match(password):
        return False
    return True

def is_not_same_as_id(user_id: str, password: str) -> bool:
    """
    비밀번호가 ID와 동일하지 않은지 검사
    :param user_id:
    :param password:
    :return:
    """
    return user_id != password

def is_valid_email(email: str) -> bool:
    """
    이메일 유효성 검사
    - 문자열 길이가 50자 이하
    - xxx@yyy.com  형태의 이메일 주소만 허용함
    - @ 앞 뒤의 “xxx”, “yyy”안에는 로마자 대/소문자, 숫자(0-9)의 조합만 허용
    - 공백류는 어디에도 포함 불가
    :param email:
    :return:
    """
    # 정규식으로 검사
    pattern = re.compile(r'^[A-Za-z0-9]+@[A-Za-z0-9]+\.com$')
    if not pattern.match(email):
        return False
    return True