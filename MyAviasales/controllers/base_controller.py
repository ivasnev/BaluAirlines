import string
from random import random
from typing import Any, List, Tuple
from haversine import haversine
from math import ceil
from random import randint, choices


class BaseController:

    def __init__(self, session):
        self.session = session

    async def generate_varchar_key(self, length: int, model: Any) -> str:
        """Случайная генерация нового ключа для резервации"""
        key = ''.join(choices(string.ascii_uppercase + string.digits, k=length))
        while await self.session.query(model).get(key):
            key = ''.join(choices(string.ascii_uppercase + string.digits, k=length))
        return key

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

    async def base_put(self, model, key, data) -> bool:
        obj_to_update = await self.session.query(model).get(key).one_or_none()
        if obj_to_update is None:
            return False
        data = data.dict()
        for key, value in data.items():
            if value:
                obj_to_update.__setattr__(key, value)
        await self.session.flush()
        await self.session.commit()
        return True
