from src.context import AppContext
from src.repository.entity import Category, ISBN
from src.repository.manager import CategoryRepository, ISBNRepository


class CategoryService:
    def __init__(self, app: AppContext, navi = None):
        self.app = app
        self.cat_repo: CategoryRepository = app.cat_repo
        self.isbn_repo: ISBNRepository = app.isbn_repo

    def search_by_category(self, expr: str) -> list:
        # 표햔식을 입력받아
        tokens = parse_category_expression(expr)

        # 모든 카테고리 로드
        cats = self.cat_repo.data
        cat_name_to_id = {c.cat_name: c.cat_id for c in cats}

        matched_isbn = []
        for isbn_obj in self.isbn_repo.data:
            if evaluate_category_expression(tokens, cat_name_to_id, isbn_obj):
                matched_isbn.append(isbn_obj)
        return matched_isbn

    def search_category_by_name(self, cat_name: str):
        return self.cat_repo.find_by_name(cat_name)

    def add_category(self, cat_name):
        new_cat_id = self.generate_category_id()
        new_cat = Category(cat_id=new_cat_id, cat_name=cat_name)
        self.cat_repo.insert(category=new_cat)
        return new_cat

    def generate_category_id(self) -> str:
        existing_ids = [int(cat.cat_id[3:]) for cat in self.cat_repo.data if cat.cat_id.startswith("CAT") and cat.cat_id[3:].isdigit()]
        next_id_num = max(existing_ids, default=0) + 1
        return f"CAT{next_id_num:02d}"

    def category_exists(self, cat_name: str) -> bool:
        return self.cat_repo.find_by_name(cat_name) is not None

    def merge_category(self, new_cat_name: str, cat_name_1: str, cat_name_2: str) -> Category:
        cat1 = self.cat_repo.find_by_name(cat_name_1)
        cat2 = self.cat_repo.find_by_name(cat_name_2)

        if not cat1 or not cat2:
            raise ValueError("병합할 카테고리 중 하나 이상이 존재하지 않습니다.")

        # new가 존재하지 않으면 생성 존재하면 그대로 사용
        new_cat = self.cat_repo.find_by_name(new_cat_name)
        if not new_cat:
            new_cat = self.add_category(new_cat_name)

        for isbn_obj in self.isbn_repo.data:
            cat_ids = isbn_obj.cat_id.split(';')
            if cat1.cat_id in cat_ids or cat2.cat_id in cat_ids:
                # 기존 카테고리 ID 제거
                cat_ids = [cid for cid in cat_ids if cid != cat1.cat_id and cid != cat2.cat_id]
                # 새로운 카테고리 ID 추가
                cat_ids.append(new_cat.cat_id)
                isbn_obj.cat_id = ';'.join(cat_ids)
        self.isbn_repo.save_all()
        self.cat_repo.delete(cat1.cat_id)
        self.cat_repo.delete(cat2.cat_id)
        return new_cat

    # 카테고리 부여
    def assign_category_to_isbn(self, isbn_obj: ISBN, cat: Category) -> None:
        current_cat_ids = isbn_obj.cat_id.split(';') if isbn_obj.cat_id else []
        if cat.cat_id in current_cat_ids:
            return  # 이미 부여된 카테고리
        if len(current_cat_ids) >= 3:
            return  # 최대 카테고리 수 초과
         # 카테고리 추가
        current_cat_ids.append(cat.cat_id)
        isbn_obj.cat_id = ';'.join(current_cat_ids)
        return


def parse_category_expression(expr: str) -> list:
    tokens = []
    buf = ""
    i = 0
    while i < len(expr):
        if expr[i] == '!':
            # ! 다음의 이름까지 하나의 토큰으로
            j = i + 1
            name = ""
            while j < len(expr) and expr[j] not in ['&', '|', '!']:
                name += expr[j]
                j += 1
            tokens.append("!" + name)
            i = j
        elif expr[i] in ['&', '|']:
            if buf:
                tokens.append(buf)
                buf = ""
            tokens.append(expr[i])
            i += 1
        else:
            buf += expr[i]
            i += 1

    if buf:
        tokens.append(buf)

    return tokens


def evaluate_category_expression(tokens: list, cat_name_to_id: dict, isbn_obj) -> bool:
    """
    tokens: ['science', '&', 'space']
    cat_name_to_id: {'science': 'CAT01', 'space':'CAT02'}
    isbn_obj.cat_id: 'CAT01;CAT02' 형태 가능
    """
    # ISBN 의 모든 cat_id 목록
    isbn_cats = isbn_obj.cat_id.split(';')

    def eval_token(token):
        if token.startswith("!"):
            name = token[1:]
            return cat_name_to_id.get(name) not in isbn_cats
        else:
            return cat_name_to_id.get(token) in isbn_cats

    # 매우 간단한 좌→우 평가 방식
    result = eval_token(tokens[0])

    i = 1
    while i < len(tokens):
        op = tokens[i]
        right = eval_token(tokens[i + 1])

        if op == '&':
            result = result and right
        elif op == '|':
            result = result or right
        i += 2

    return result
