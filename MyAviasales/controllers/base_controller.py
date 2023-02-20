import string
from random import random
from typing import Any, List, Tuple
from haversine import haversine
from math import ceil
from random import randint


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
    def get_dist(coords_f: Tuple[float], coords_s: Tuple[float]):
        return haversine(coords_f[::-1], coords_s[::-1])

    @staticmethod
    def generate_cost(fare_conditions, dist) -> float:
        costs_for_cord = {
            'Economy': 10,
            'Comfort': 20,
            'Business': 30
        }
        return ceil((dist*randint(50, 120)/100) / 10) * 10 * costs_for_cord[fare_conditions]
