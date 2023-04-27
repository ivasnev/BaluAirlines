import string
from random import seed
from typing import Any, Tuple
from haversine import haversine
from math import ceil
from random import randint, choices
from datetime import date, datetime, timedelta


class BaseController:
    """
    Базовый контроллер от которого наследуются остальные содержит базовый функционал
    """

    def __init__(self, session):
        self.session = session

    def generate_varchar_key(self, length: int, model: Any) -> str:
        """
        Метод для случайной генерации нового ключа строкового типа

        :param length: Длина нового ключа
        :param model: ОРМ модель класса для которого генерируем ключ
        :return: Уникальный не занятый ключ
        """
        key = ''.join(choices(string.ascii_uppercase + string.digits, k=length))
        while self.session.query(model).get(key):
            key = ''.join(choices(string.ascii_uppercase + string.digits, k=length))
        return key

    def generate_digit_varchar_key(self, length: int, model: Any) -> str:
        """
        Метод для случайной генерации нового ключа численного типа

        :param length: Длина нового ключа
        :param model: ОРМ модель класса для которого генерируем ключ
        :return: Уникальный не занятый ключ
        """
        key = ''.join(choices(string.digits, k=length))
        while self.session.query(model).get(key):
            key = ''.join(choices(string.digits, k=length))
        return key

    @staticmethod
    def get_dist(coords_f: Tuple[float], coords_s: Tuple[float]):
        """
        Метод для рассчёта растояния по координатам

        :param coords_f: Координаты первой точки
        :param coords_s: Координаты второй точки
        :return: Расстояние между точками
        """
        return haversine(coords_f[::-1], coords_s[::-1])

    @staticmethod
    def generate_cost(fare_conditions, dist, _date: date) -> float:
        """
        Метод для генерации цены за перелёт

        :param fare_conditions: Класс перелёта
        :param dist: Расстояние
        :param _date: Дата перелёта
        :return: Цена перелёта
        """
        date_to_seed = datetime(month=_date.month, day=_date.day, year=_date.year) + timedelta(hours=datetime.now().hour)
        seed(date_to_seed.ctime())
        costs_for_cord = {
            'Economy': 10,
            'Comfort': 20,
            'Business': 30
        }
        return ceil((dist * randint(50, 120) / 100) / 10) * 10 * costs_for_cord[fare_conditions]

    def base_put(self, model, key, data) -> bool:
        """
        Базовый метод обновления записи в бд

        :param model: ОРМ модель класса который обновляем
        :param key: Ключ для поиска нужного объекта
        :param data: Данные для обновления
        :return: Статус обновления(Обновлён/ не обновлён)
        """
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
