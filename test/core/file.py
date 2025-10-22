from src.repository.manager import UsersRepository

if __name__ == "__main__":
    # 테스트용 코드
    fm = UsersRepository(path="data/users.txt")

    print(fm.data)

