from src.repository.manager import UsersRepository

if __name__ == "__main__":
    # 테스트용 코드
    test_file = "data/users.txt"
    fm = UsersRepository(test_file)
    lines = fm.to_list_of_dicts()
    for line in lines:
        print(line)

