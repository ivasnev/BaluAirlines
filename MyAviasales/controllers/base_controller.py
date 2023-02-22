import string
from random import random, seed
from typing import Any, List, Tuple
from haversine import haversine
from math import ceil
from random import randint, choices
from datetime import date, datetime, timedelta


class BaseController:

    def __init__(self, session):
        self.session = session

    def generate_varchar_key(self, length: int, model: Any) -> str:
        """Случайная генерация нового ключа для резервации"""
        key = ''.join(choices(string.ascii_uppercase + string.digits, k=length))
        while self.session.query(model).get(key):
            key = ''.join(choices(string.ascii_uppercase + string.digits, k=length))
        return key

    @staticmethod
    def get_dist(coords_f: Tuple[float], coords_s: Tuple[float]):
        return haversine(coords_f[::-1], coords_s[::-1])

    @staticmethod
    def generate_cost(fare_conditions, dist, date: date) -> float:
        date_to_seed = datetime(month=date.month, day=date.day, year=date.year) + timedelta(hours=datetime.now().hour)
        seed(date_to_seed.ctime())
        costs_for_cord = {
            'Economy': 10,
            'Comfort': 20,
            'Business': 30
        }
        return ceil((dist*randint(50, 120)/100) / 10) * 10 * costs_for_cord[fare_conditions]

    def base_put(self, model, key, data) -> bool:
        obj_to_update = self.session.query(model).get(key)
        if obj_to_update is None:
            return False
        data = data.dict()
        for key, value in data.items():
            if value:
                obj_to_update.__setattr__(key, value)
        self.session.flush()
        self.session.commit()
        return True
