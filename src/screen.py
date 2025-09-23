import os

from src.context import AppContext


def clear_screen():
    os.system('cls')

def main_menu(app: AppContext):
    while True:
        clear_screen()
        if app.current_user is None:
            print("=== 도서 관리 시스템 ===")
            print("1) 로그인")
            print("2) 회원가입")
            print("3) 종료")
            choice = input("선택: ").strip()
            if choice == "1":
                login_screen(app)
            elif choice == "2":
                clear_screen()
                # signup_screen(app)
                print("회원가입 기능은 아직 구현되지 않았습니다.")
                input("엔터를 눌러 계속...")
            elif choice == "3":
                clear_screen()
                print("종료합니다.")
                input("엔터를 눌러 계속...")

                break
            else:
                input("잘못된 입력입니다. 엔터를 눌러 계속...")
        else:
            home_screen(app)

def login_screen(app: AppContext):
    clear_screen()
    print("=== 로그인 ===")
    username = input("아이디: ").strip()
    password = input("비밀번호: ").strip()
    if app.login(username, password):
        input("로그인 성공! 엔터를 눌러 계속...")
    else:
        input("로그인 실패! 엔터를 눌러 계속...")

def home_screen(app: AppContext):
    while True:
        clear_screen()
        print(f"=== 환영합니다, {app.current_user['username']} ===")
        print("1) 도서 검색")
        print("2) 대출 내역")
        print("3) 로그아웃")
        choice = input("선택: ").strip()
        if choice == "1":
            # search_books_screen(app)
            print("도서 검색 기능은 아직 구현되지 않았습니다.")
            input("엔터를 눌러 계속...")
        elif choice == "2":
            # view_loans_screen(app)
            print("대출 내역 기능은 아직 구현되지 않았습니다.")
            input("엔터를 눌러 계속...")
        elif choice == "3":
            app.logout()
            input("로그아웃 되었습니다. 엔터를 눌러 계속...")
            break
        else:
            input("잘못된 입력입니다. 엔터를 눌러 계속...")