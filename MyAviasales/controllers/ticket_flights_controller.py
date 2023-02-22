from MyAviasales.controllers.base_controller import BaseController
from MyAviasales.models import TicketFlight


class TicketFlightController(BaseController):
    async def get_all_ticket_flights(self, page: int) -> list:
        page_size = 50
        ticket_flight_query = await self.session.query(TicketFlight.ticket_no,
                                                 TicketFlight.flight_id,
                                                 TicketFlight.fare_conditions,
                                                 TicketFlight.amount
                                                 ).limit(page_size).offset(page * page_size)
        ticket_flights = [x._asdict() for x in ticket_flight_query if x is not None]
        for ticket_flight in ticket_flights:
            if ticket_flight['amount']:
                ticket_flight['amount'] = float(ticket_flight['amount'])
        return ticket_flights

    async def get_single_ticket_flight(self, key: dict) -> dict:
        ticket_flight = await self.session.query(TicketFlight.ticket_no,
                                           TicketFlight.flight_id,
                                           TicketFlight.fare_conditions,
                                           TicketFlight.amount
                                           ).filter_by(ticket_no=key['ticket_no'],
                                                       flight_id=key['flight_id']
                                                       ).first()
        if ticket_flight:
            ticket_flight = ticket_flight._asdict()
            if ticket_flight['amount']:
                ticket_flight['amount'] = float(ticket_flight['amount'])
        return ticket_flight

    async def post_ticket_flight(self, data: dict) -> bool:
        await self.session.add(TicketFlight(ticket_no=data['ticket_no'],
                                      flight_id=data['flight_id'],
                                      fare_conditions=data['fare_conditions'],
                                      amount=data['amount']
                                      ))
        await self.session.flush()
        await self.session.commit()
        return True

    async def delete_ticket_flight(self, key: dict) -> bool:
        await self.session.delete(await self.session.query(TicketFlight).get(key))
        return True

    async def put_ticket_flight(self, _key: dict, data: dict) -> bool:
        obj_to_update = await self.session.query(TicketFlight).get(_key)
        print(obj_to_update.__dict__.keys())
        for key, value in data.items():
            obj_to_update.__setattr__(key, value)
        await self.session.flush()
        await self.session.commit()
        return True
