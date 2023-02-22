from MyAviasales.models import *
from MyAviasales.controllers.base_controller import BaseController
from MyAviasales.views.seats.schema import *
from typing import List, Optional
import json


class SeatController(BaseController):

    async def get_single_seat(self, aircraft_code, seat_no) -> SeatBase:
        """Получение одного места"""
        res = self.session.query(Seat.aircraft_code, Seat.seat_no, Seat.fare_conditions) \
            .filter(Seat.aircraft_code == aircraft_code, Seat.seat_no == seat_no).one_or_none()
        return SeatBase.from_orm(res)

    async def get_all_seats(self) -> Optional[List[SeatBase]]:
        """Получение всех мест"""
        res = self.session.query(Seat.aircraft_code, Seat.seat_no).all()
        return [SeatBase.from_orm(row) for row in res]

    async def post_seat(self, data: SeatBase) -> bool:
        """Добавление места"""
        self.session.add(Seat(aircraft_code=data.aircraft_code,
                              seat_no=data.seat_no,
                              fare_conditions=data.fare_conditions)
                         )
        self.session.flush()
        self.session.commit()
        return True

    async def delete_seat(self, seat_no: str, aircraft_code: str) -> bool:
        """Удаление места"""
        deletable = self.session.query(Seat).get(seat_no=seat_no, aircraft_code=aircraft_code)
        self.session.delete(deletable)
        self.session.commit()
        return True

    async def put_seat(self, seat_no: str, aircraft_code: str, data: SeatUpdate) -> bool:
        """Обновление информации"""
        return self.base_put(Seat, {'seat_no': seat_no, 'aircraft_code': aircraft_code}, data)
