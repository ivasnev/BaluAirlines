from MyAviasales.models import *
from MyAviasales.controllers.base_controller import BaseController
from MyAviasales.views.seats.schema import *
from typing import List, Optional


class SeatController(BaseController):

    async def get_single_seat(self, seat_no, aircraft_code) -> Optional[SeatBase]:
        """Получение одного места"""
        res = self.session.query(Seat.aircraft_code, Seat.seat_no, Seat.fare_conditions) \
            .filter(Seat.aircraft_code == aircraft_code, Seat.seat_no == seat_no).one_or_none()
        if res:
            return SeatBase.from_orm(res)
        return res

    async def get_all_seats(self, page: int = 0) -> Optional[List[SeatBase]]:
        """Получение всех мест"""
        page_size = 50
        res = self.session.query(Seat.aircraft_code, Seat.seat_no, Seat.fare_conditions).limit(page_size).offset(
            page * page_size)
        return [SeatBase.from_orm(row) for row in res if row is not None]

    async def post_seat(self, data: SeatBase) -> bool:
        """Добавление места"""
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
        """Удаление места"""
        deletable = self.session.query(Seat).get({'seat_no': seat_no, 'aircraft_code': aircraft_code})
        if deletable is None:
            return False
        self.session.delete(deletable)
        self.session.commit()
        return True

    async def put_seat(self, seat_no: str, aircraft_code: str, data: SeatUpdate) -> bool:
        """Обновление информации"""
        return self.base_put(Seat, {'seat_no': seat_no, 'aircraft_code': aircraft_code}, data)
