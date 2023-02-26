from MyAviasales.controllers.base_controller import BaseController
from MyAviasales.views.ticket_flights.schema import *
from MyAviasales.models import TicketFlight
from typing import Optional, List


class TicketFlightController(BaseController):
    async def get_all_ticket_flights(self, page: int) -> Optional[List[TicketFlightBase]]:
        page_size = 50
        ticket_flight_query = self.session.query(TicketFlight
                                                 ).limit(page_size).offset(page * page_size)
        ticket_flights = [TicketFlightBase.from_orm(x) for x in ticket_flight_query if x is not None]
        return ticket_flights

    async def get_single_ticket_flight(self, ticket_no: str, flight_id: int) -> Optional[TicketFlightBase]:
        ticket_flight = self.session.query(TicketFlight
                                           ).filter_by(ticket_no=ticket_no,
                                                       flight_id=flight_id
                                                       ).one_or_none()
        if ticket_flight:
            return TicketFlightBase.from_orm(ticket_flight)
        return ticket_flight

    async def post_ticket_flight(self, data: TicketFlightBase) -> bool:
        ticket_flight = self.session.query(TicketFlight).filter(
            TicketFlight.ticket_no == data.ticket_no,
            TicketFlight.flight_id == data.flight_id
        ).one_or_none()
        if ticket_flight:
            return False
        self.session.add(TicketFlight(ticket_no=data.ticket_no,
                                      flight_id=data.flight_id,
                                      fare_conditions=data.fare_conditions,
                                      amount=data.amount
                                      ))
        self.session.flush()
        self.session.commit()
        return True

    async def delete_ticket_flight(self, ticket_no: str, flight_id: int) -> bool:
        ticket_flight = self.session.query(TicketFlight).filter(
            TicketFlight.ticket_no == ticket_no,
            TicketFlight.flight_id == flight_id
        ).one_or_none()
        if ticket_flight is None:
            return False
        self.session.delete(self.session.query(TicketFlight).get({'ticket_no': ticket_no, 'flight_id': flight_id}))
        self.session.commit()
        return True

    async def put_ticket_flight(self, ticket_no: str, flight_id: int, data: TicketFlightUpdate) -> bool:
        return self.base_put(TicketFlight, {'ticket_no': ticket_no, 'flight_id': flight_id}, data)
