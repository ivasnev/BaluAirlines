from MyAviasales.models import *
from MyAviasales.controllers.base_controller import BaseController
from sqlalchemy import or_
from MyAviasales.views.airports.schema import *
from typing import List, Optional


class AirportController(BaseController):

    async def get_single_airport(self, key) -> Optional[AirportBase]:
        """Получение одного аэропорта"""
        res = self.session.query(AirportsDatum.airport_code,
                                 AirportsDatum.airport_name,
                                 AirportsDatum.city,
                                 AirportsDatum.coordinates,
                                 AirportsDatum.timezone) \
            .filter(AirportsDatum.airport_code == key).one_or_none()
        return AirportBase.from_orm(res)

    async def get_all_airports(self) -> Optional[List[AirportBase]]:
        """Получение всех аэропортов"""
        res = self.session.query(AirportsDatum.airport_code,
                                 AirportsDatum.airport_name,
                                 AirportsDatum.city,
                                 AirportsDatum.coordinates,
                                 AirportsDatum.timezone).all()
        return [AirportBase.from_orm(row) for row in res]

    async def post_airport(self, data: AirportBase) -> bool:
        """Добавление аэропорта"""
        self.session.add(AirportsDatum(airport_code=data.airport_code,
                                       airport_name=data.airport_name.dict(),
                                       city=data.city.dict(),
                                       coordinates=data.coordinates,
                                       timezone=data.timezone))
        self.session.flush()
        self.session.commit()
        return True

    async def delete_airport(self, airport_code: str) -> bool:
        flights = self.session.query(Flight).filter(
            or_(Flight.departure_airport == airport_code, Flight.arrival_airport == airport_code)
        ).all()
        for flight in flights:
            flight.status = 'Cancelled'

        self.session.flush()
        self.session.commit()
        return True

    async def put_airport(self, airport_code, data: AirportUpdate) -> bool:
        """Обновление информации"""
        return self.base_put(AirportsDatum, airport_code, data)
