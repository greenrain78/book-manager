from src.context import AppContext
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
