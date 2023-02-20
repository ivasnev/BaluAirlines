import string
from random import random
from typing import Any, List, Tuple
from math import sqrt


class BaseController:

    def __init__(self, session):
        self.session = session

    def generate_varchar_key(self, length: int, model: Any) -> str:
        """Случайная генерация нового ключа для резервации"""
        book_ref = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        while self.session.query(model).get(book_ref):
            book_ref = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return book_ref

    @staticmethod
    def get_dist(coords: List[Tuple[float]]):
        return sqrt((coords[0][0] - coords[0][1]) ** 2 + (coords[1][0] - coords[1][1]) ** 2)

    @staticmethod
    def generate_cost(fare_conditions, dist) -> float:
        costs_for_cord = {
            'Economy': 1113,
            'Comfort': 1870,
            'Business': 3305
        }
        return round(dist * costs_for_cord[fare_conditions], 2)
