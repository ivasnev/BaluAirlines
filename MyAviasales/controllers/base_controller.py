import string
from random import random
from typing import Any


class BaseController:

    def __init__(self, session):
        self.session = session

    async def generate_varchar_key(self, length: int, model: Any) -> str:
        """Случайная генерация нового ключа для резервации"""
        book_ref = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        while not self.session.query(model).get(book_ref):
            book_ref = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return book_ref
