from MyAviasales.models import *
from MyAviasales.controllers.base_controller import BaseController
from MyAviasales.views.seats.schema import *
from typing import List, Optional


class SeatController(BaseController):
    """
    Контроллер для работы с бд сидений
    """

    async def get_single_seat(self, seat_no, aircraft_code) -> Optional[SeatBase]:
        """
        Метод для получение одного места

        :param seat_no: Номер места
        :param aircraft_code: Код самолёта
        :return:
        """
        res = self.session.query(Seat.aircraft_code, Seat.seat_no, Seat.fare_conditions) \
            .filter(Seat.aircraft_code == aircraft_code, Seat.seat_no == seat_no).one_or_none()
        if res:
            return SeatBase.from_orm(res)
        return res

    async def get_all_seats(self, page: int = 0) -> Optional[List[SeatBase]]:
        """
        Метод для получение всех мест

        :param page: Номер страницы
        :return: Страница из 50 записей с местами
        """
        page_size = 50
        res = self.session.query(Seat.aircraft_code, Seat.seat_no, Seat.fare_conditions).limit(page_size).offset(
            page * page_size)
        return [SeatBase.from_orm(row) for row in res if row is not None]

    async def post_seat(self, data: SeatBase) -> bool:
        """
        Метод для добавления места

        :param data: Данные для создания места
        :return: Статус создания(Создан/ не создан)
        """
        seat = self.session.query(Seat).filter(
            Seat.aircraft_code == data.aircraft_code,
            Seat.seat_no == data.seat_no
        ).one_or_none()
        if seat:
            return False
        self.session.add(Seat(aircraft_code=data.aircraft_code,
                              seat_no=data.seat_no,
                              fare_conditions=data.fare_conditions)
                         )
        self.session.flush()
        self.session.commit()
        return True

    async def delete_seat(self, seat_no: str, aircraft_code: str) -> bool:
        """
        Метод для удаление места

        :param seat_no: Номер места
        :param aircraft_code: Код самолёта
        :return: Статус удаления(Удалён/ не удалён)
        """
        deletable = self.session.query(Seat).get({'seat_no': seat_no, 'aircraft_code': aircraft_code})
        if deletable is None:
            return False
        self.session.delete(deletable)
        self.session.commit()
        return True

    async def put_seat(self, seat_no: str, aircraft_code: str, data: SeatUpdate) -> bool:
        """
        Метод для обновление информации о сидении

        :param seat_no: Номер места
        :param aircraft_code: Код самолёта
        :param data: Данные для обновления
        :return: Статус обновления(Обновлён/ не обновлён)
        """
        return self.base_put(Seat, {'seat_no': seat_no, 'aircraft_code': aircraft_code}, data)
