from MyAviasales.controllers.base_controller import BaseController
from MyAviasales.models import AircraftsDatum, Flight
from typing import Union, List
from MyAviasales.views.aircraft_data.schema import AircraftBase, AircraftUpdate


class AircraftController(BaseController):
    async def get_all_aircraft(self) -> Union[List[AircraftBase], None]:
        aircraft = await self.session.query(
            AircraftsDatum.aircraft_code, AircraftsDatum.model, AircraftsDatum.range
        ).all()
        return [AircraftBase.parse_obj(row._asdict()) for row in aircraft]

    async def get_single_aircraft(self, key: str) -> Union[AircraftBase, None]:
        aircraft = await self.session.query(
                AircraftsDatum.aircraft_code, AircraftsDatum.model, AircraftsDatum.range
            ).filter(
                AircraftsDatum.aircraft_code == key
            ).one_or_none()
        if aircraft:
            return AircraftBase.from_orm(aircraft)
        else:
            return None

    async def post_aircraft(self, data: AircraftBase) -> Union[AircraftBase, None]:
        if await self.get_single_aircraft(data.aircraft_code):
            return None
        obj_to_add = AircraftsDatum(
            aircraft_code=data.aircraft_code,
            model=dict(data.model),
            range=data.range,
        )
        await self.session.add(obj_to_add)
        await self.session.commit()
        return AircraftBase.from_orm(obj_to_add)

    # TODO какая-то херь а не делит
    async def delete_aircraft(self, key: str) -> Union[AircraftBase, None]:
        # При удалении самолета произойдет конфликт со значениями в таблице рейсов
        aircraft = await self.session.query(AircraftsDatum).get(key)
        if aircraft is None:
            return None
        flights = await self.session.query(Flight).filter(Flight.aircraft_code == key).all()
        for flight in flights:
            flight.status = 'Cancelled'
            await self.session.add(flight)
            await self.session.flush()
        return AircraftBase.from_orm(aircraft)

    async def put_aircraft(self, key: str, data: AircraftUpdate) -> Union[AircraftBase, None]:
        aircraft = await self.session.query(AircraftsDatum).filter(
            AircraftsDatum.aircraft_code == key
        ).one_or_none()
        if aircraft is None:
            return None
        print(data.range)
        if data.range:
            aircraft.range = data.range
        if data.model:
            aircraft.model = dict(data.model)
        await self.session.add(aircraft)
        await self.session.flush()
        await self.session.commit()
        return AircraftBase.from_orm(aircraft)
