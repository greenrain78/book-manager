from datetime import datetime
from logging import getLogger

from src.context import AppContext
from src.core.valid import input_with_validation, parse_with_validation
from src.prompt.admin import admin_prompt
from src.prompt.user import user_prompt
from src.repository.entity import User
from src.vaild.basic import is_valid_date_format, is_previous_date
from src.vaild.start import is_valid_user_id, is_valid_password, is_valid_email, is_available_user_id, \
    is_reserved_user_id, is_not_same_as_id

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
        if now_date is not None:
            log.debug(f"유효한 날짜 입력: {now_date}")
            break

    # 날짜 등록
    app.set_current_date(now_date)
    log.debug(f"현재 날짜 설정: {now_date}")
    return None


def main_prompt(app: AppContext) -> None:
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
                print("회원가입 선택")
                signup_prompt(app=app)
            elif choice == '2':
                print("로그인 선택")
                login_prompt(app=app)
            elif choice == '3':
                print("종료 선택")
                break
            else:
                print("잘못된 입력입니다!! 1,2,3 중 하나를 입력하세요.")
        except Exception as e:
            log.error(f"메인 프롬프트 오류: {e}")
            print("오류가 발생했습니다!! 다시 시도하세요.")
    log.info(f"Main prompt 종료")
    return None

def signup_prompt(app: AppContext) -> None:
    # 회원가입 레코드 갯수 제한 검사
    if len(app.users.data) > 20:
        app.exit_with_error(f"ID갯수가 총 20개를 초과하였습니다!! 다음에 이용해주세요^^")

    # ID 입력 및 유효성 검사
    while True:
        user_id = input_with_validation(
            "ID를 입력하세요: ",
            [
                (is_valid_user_id, "ID가 4자리 이상이어야 합니다!!  다른 ID를 입력하세요."),
                (is_available_user_id, "이미 존재하는 ID입니다!!  다른 ID를 입력하세요."),
                (is_reserved_user_id, "잘못된 ID입니다!! 다른 ID를 입력하세요.")
            ]
        )
        if user_id:
            break
    log.debug(f"사용 가능한 ID 입력: {user_id}")

    # 비밀번호 입력 및 유효성 검사
    while True:
        password = input_with_validation(
            "pwd를 입력하세요 :",
            [
                (is_valid_password, "패스워드는 8자리 이상이어야 합니다!! 다른 pw를 입력하세요."),
                (lambda v: is_not_same_as_id(user_id=user_id, password=v), "pw는 ID와 동일할 수 없습니다!! 다른 pw를 입력하세요."),
            ]
        )
        if password:
            break
    log.debug(f"사용 가능한 pwd 입력: {password}")

    # 이메일 입력 및 유효성 검사
    while True:
        email = input_with_validation(
            "이메일을 입력하세요 :",
            [
                (is_valid_email, "이메일 형식은 xxx@yyy.com 형식입니다!! 형식에 맞게 입력하세요."),
            ]
        )
        if email:
            break
    log.debug(f"사용 가능한 이메일 입력: {email}")
    log.info(f"회원가입 완료: ID={user_id}, PWD={password}, EMAIL={email}")

    app.users.insert(User(user_id=user_id, pw=password, email=email))
    return None

def login_prompt(app: AppContext) -> None:
    while True:
        user_id = input_with_validation(
            "ID를 입력하세요: ",
            [
                (is_valid_user_id, "잘못된 ID입니다."),
                # (lambda v: not is_available_user_id(user_id=v, app=app), "존재하지 않는 ID입니다."),
            ]
        )
        if is_reserved_user_id(user_id=user_id):
            # 관리자 페이지로 이동
            admin_prompt(app=app)
            # 메인 프롬프트로 복귀
            return None

        if is_available_user_id(user_id=user_id, app=app):
            print(f"존재하는 ID입니다. pw를 입력해주세요.")
            continue

        if user_id:
            break
    log.debug(f"사용 가능한 ID 입력: {user_id}")
    user = next((u for u in app.users.data if u.user_id == user_id), None) # 사용자 정보 조회

    # 비밀번호 입력 및 유효성 검사
    while True:
        password = input_with_validation(
            "pwd를 입력하세요 :",
            [
                (is_valid_password, "잘못된 형식입니다!!  pw를 다시 입력하세요."),
                (lambda v: user.pw == v, "ID와 일치하는 pw가 아닙니다!!  pw를 다시 입력하세요."),
            ]
        )
        if password:
            break
    log.debug(f"사용 가능한 pwd 입력: {password}")

    # 로그인 완료 처리
    app.set_current_user(user)
    log.info(f"로그인 완료: ID={user_id}")

    # 로그인 완료 후 유저 프롬프트 이동
    user_prompt(app=app)

    # 그 후 main으로 이동함
    return None






        # password = input("pwd를 입력하세요 :").strip()
        # if is_valid_password(password=password):
        #     log.debug(f"사용 가능한 pwd 입력: {password}")
        #     break
        # else:
        #     log.debug(f"잘못된 pwd 입력: {password}")


    # # 이메일 입력 및 유효성 검사
    # while True:
    #     email = input("이메일을 입력하세요 :").strip()
    #     if is_valid_email(email=email):
    #         log.debug(f"이메일 입력: {email}")
    #         break
    #     else:
    #         log.debug(f"잘못된 이메일 입력: {email}")
    # log.info(f"회원가입 완료: ID={user_id}, PWD={password}, EMAIL={email}")
    # # 회원 가입 완료 후 로그인 프롬프트 이동
    # login_prompt(app=app)
    # return None
