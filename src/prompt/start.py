from datetime import datetime
from logging import getLogger

from src.context import AppContext
from src.core.valid import input_with_validation, parse_with_validation
from src.vaild.basic import is_valid_date_format, is_previous_date
from src.vaild.start import is_valid_user_id, is_valid_password, is_valid_email, is_available_user_id

log = getLogger(__name__)

def date_input_prompt(app: AppContext) -> None:
    """
    날짜 입력 프롬프트
    :param app:
    :return:
    """
    # 날짜 형식 무결성 검사
    while True:
        date_str = input_with_validation(
            "날짜를 입력하세요(YYYY-MM-DD): ",
            [
                (is_valid_date_format, "잘못된 입력입니다!! 올바른 날짜를 입력하세요."),
            ]
        )
        # 날짜 파싱
        now_date = parse_with_validation(
            date_str,
            lambda v: datetime.strptime(v, "%Y-%m-%d"),
            "잘못된 입력입니다!! 올바른 날짜를 입력하세요.",
            [
                (is_previous_date, "이전 날짜를 입력했습니다!! 올바른 날짜를 입력하세요.")
            ]
        )
        # 날짜 등록
        app.set_current_date(now_date)
        log.debug(f"현재 날짜 설정: {now_date}")
        break
    return None


def main_prompt(app: AppContext) -> None:
    """
    메인 프롬프트
    :param app:
    :return:
    """
    print(f"Main")
    print(f"1. 회원가입")
    print(f"2. 로그인")
    print(f"3. 종료")
    while True:
        choice = input("명령어를 입력하세요: ").strip()
        if choice == '1':
            print("회원가입 선택")
            signup_prompt(app=app)
        elif choice == '2':
            print("로그인 선택")
        elif choice == '3':
            print("종료 선택")
            break
        else:
            print("잘못된 입력입니다!! 1,2,3 중 하나를 입력하세요.")
    log.info(f"Main prompt 종료")
    return None

def signup_prompt(app: AppContext) -> None:

    # ID 입력 및 유효성 검사
    while True:
        user_id = input("ID를 입력하세요: ").strip()
        if not is_valid_user_id(user_id=user_id):
            log.debug(f"잘못된 ID 입력: {user_id}")
            continue
        if is_available_user_id(user_id=user_id):
            log.debug(f"사용 가능한 ID 입력: {user_id}")
            break
        else:
            log.debug(f"이미 사용중인 ID 입력: {user_id}")

    # 비밀번호 입력 및 유효성 검사
    while True:
        password = input("pwd를 입력하세요 :").strip()
        if is_valid_password(password=password):
            log.debug(f"사용 가능한 pwd 입력: {password}")
            break
        else:
            log.debug(f"잘못된 pwd 입력: {password}")

    # 이메일 입력 및 유효성 검사
    while True:
        email = input("이메일을 입력하세요 :").strip()
        if is_valid_email(email=email):
            log.debug(f"이메일 입력: {email}")
            break
        else:
            log.debug(f"잘못된 이메일 입력: {email}")
    log.info(f"회원가입 완료: ID={user_id}, PWD={password}, EMAIL={email}")
    # 회원 가입 완료 후 로그인 프롬프트 이동
    login_prompt(app=app)
    return None

def login_prompt(app: AppContext) -> None:
    while True:
        user_id = input_with_validation(
            "ID를 입력하세요: ",
            [
                (is_valid_user_id, "잘못된 ID입니다."),
                (lambda v: not is_available_user_id(v), "존재하지 않는 ID입니다."),
            ]
        )

        # user_id = input("ID를 입력하세요: ").strip()
        # if not is_valid_user_id(user_id=user_id):
        #     log.debug(f"잘못된 ID 입력: {user_id}")
        #     continue
        # if is_available_user_id(user_id=user_id):
        #     print(f"존재하지 않는 ID입니다!! ID를 다시 입력하세요.")
        #     log.debug(f"존재하지 않는 ID 입력: {user_id}")
        #     continue
        # else:
        #     log.debug(f"존재하는 ID 입력: {user_id}")
        #     break

    while True:
        password = input("pwd를 입력하세요 :").strip()
        if is_valid_password(password=password):
            log.debug(f"사용 가능한 pwd 입력: {password}")
            break
    return None