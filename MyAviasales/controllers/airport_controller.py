from MyAviasales.models import *
from MyAviasales.controllers.base_controller import BaseController
from sqlalchemy import or_
from MyAviasales.views.airports.schema import *
from typing import List, Optional


class AirportController(BaseController):
    """
    Контроллер для работы с бд аэропортов
    """

    async def get_single_airport(self, key: str) -> Optional[AirportBase]:
        """
        Получение одного аэропорта

        :param key: Код аэропорта
        :return: Аэропорт в единственном экземпляре
        """
        res = self.session.query(AirportsDatum.airport_code,
                                 AirportsDatum.airport_name,
                                 AirportsDatum.city,
                                 AirportsDatum.coordinates,
                                 AirportsDatum.timezone) \
            .filter(AirportsDatum.airport_code == key).one_or_none()
        return AirportBase.from_orm(res)

    async def get_all_airports(self) -> Optional[List[AirportBase]]:
        """
        Получение всех аэропортов

        :return: Список аэропортов
        """
        res = self.session.query(AirportsDatum.airport_code,
                                 AirportsDatum.airport_name,
                                 AirportsDatum.city,
                                 AirportsDatum.coordinates,
                                 AirportsDatum.timezone).all()
        return [AirportBase.from_orm(row) for row in res]

    async def post_airport(self, data: AirportBase) -> bool:
        """
        Добавление аэропорта

        :param data: Данные для добавления аэропорта
        :return: Статус создания(Создан/ не создан)
        """
        airport = self.session.query(AirportsDatum).filter(
            AirportsDatum.airport_code == data.airport_code
        ).one_or_none()
        if airport:
            return False
        self.session.add(AirportsDatum(airport_code=data.airport_code,
                                       airport_name=data.airport_name.dict(),
                                       city=data.city.dict(),
                                       coordinates=data.coordinates,
                                       timezone=data.timezone))
        self.session.flush()
        self.session.commit()
        return True

    async def delete_airport(self, airport_code: str) -> bool:
        """
        Метод для удаления аэропорта

        :param airport_code: Код аэропорта
        :return: Статус удаления(Удалён/ не удалён)
        """
        flights = self.session.query(Flight).filter(
            or_(Flight.departure_airport == airport_code, Flight.arrival_airport == airport_code)
        ).all()
        for flight in flights:
            flight.status = 'Cancelled'

        self.session.flush()
        self.session.commit()
        return True

    async def put_airport(self, airport_code, data: AirportUpdate) -> bool:
        """
        Обновление информации

        :param airport_code: Код аэропорта для обновления
        :param data: Данные для обновления
        :return: Статус обновления(Обновлён/ не обновлён)
        """
        return self.base_put(AirportsDatum, airport_code, data)
