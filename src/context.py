

class AppContext:
    def __init__(self):
        self.current_date = None
        self.current_user = None



    def login(self, username, password):
        # 실제 애플리케이션에서는 데이터베이스 조회 등을 통해 인증을 수행합니다.
        # 여기서는 단순히 하드코딩된 사용자로 예시를 들겠습니다.
        if username == "admin" and password == "password":
            self.current_user = {"username": username}
            return True
        return False


    def logout(self):
        self.current_user = None

    def set_current_date(self, now_date):
        self.current_date = now_date