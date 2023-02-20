from MyAviasales.models import *
from MyAviasales.controllers.base_controller import BaseController
from sqlalchemy import or_


class AirportController(BaseController):

    async def get_single_airport(self, key):
        """Получение одного аэропорта"""
        res = self.session.query(AirportsDatum.airport_code, AirportsDatum.airport_name, AirportsDatum.timezone) \
            .filter(AirportsDatum.airport_code == key).one_or_none()

        return res._asdict()

    async def get_all_airports(self):
        """Получение всех аэропортов"""
        res = self.session.query(AirportsDatum.airport_code, AirportsDatum.airport_name).all()
        return [row._asdict() for row in res]

    async def post_airport(self, data):
        """Добавление аэропорта"""
        self.session.add(AirportsDatum(airport_code=data['airport_code'],
                                       airport_name=data['airport_name'],
                                       city=data['city'],
                                       coordinates=data['coordinates'],
                                       timezone=data['timezone']))
        self.session.flush()
        self.session.commit()
        return True

    async def delete_airport(self, data):
        flights = self.session.query(Flight).filter(
            or_(Flight.departure_airport == data['airport_code'], Flight.arrival_airport == data['airport_code'])
        ).all()
        for flight in flights:
            flight.status = 'Cancelled'

        self.session.flush()
        self.session.commit()
        return True

    async def put_airport(self, keys, data):
        """Обновление информации"""

        obj = self.session.query(AirportsDatum). \
            filter(AirportsDatum.airport_code == keys['airport_code']).one_or_none()

        for key in data:
            obj.__setattr__(key, data[key])

        self.session.flush()
        self.session.commit()
        return True
