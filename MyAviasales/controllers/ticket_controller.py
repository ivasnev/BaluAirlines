from MyAviasales.views.tickets.schema import *
from MyAviasales.controllers.base_controller import BaseController
from MyAviasales.models import Booking, Ticket, TicketFlight, BoardingPass
from typing import Optional, List


class TicketController(BaseController):
    async def get_all_ticket_by_book_ref(self, key: str) -> Optional[List[TicketBase]]:
        tickets = self.session.query(
            Ticket.ticket_no, Ticket.book_ref, Ticket.passenger_id, Ticket.passenger_name, Ticket.contact_data
        ).filter(
            Ticket.book_ref == key
        ).all()
        return [TicketBase.from_orm(x) for x in tickets if x is not None]

    async def get_all_tickets(self, page: int = 0) -> Optional[List[TicketBase]]:
        page_size = 50
        tickets = self.session.query(
            Ticket
        ).limit(page_size).offset(
            page * page_size)
        return [TicketBase.from_orm(row) for row in tickets]

    async def get_single_ticket(self, ticket_no: str) -> Optional[TicketBase]:
        ticket = self.session.query(
            Ticket
        ).filter(
            Ticket.ticket_no == ticket_no
        ).one_or_none()
        if ticket:
            return TicketBase.from_orm(ticket)
        return ticket

    async def post_ticket(self, data: TicketPost):
        ticket_no = self.generate_digit_varchar_key(13, Ticket)
        self.session.add(Ticket(
            ticket_no=ticket_no,
            book_ref=data.book_ref,
            passenger_id=data.passenger_id,
            passenger_name=data.passenger_name,
            contact_data=data.contact_data.dict(),
        ))
        self.session.commit()
        return True

    async def delete_ticket(self, ticket_no: str):
        ticket = self.session.query(Ticket).filter(
            Ticket.ticket_no == ticket_no
        ).one_or_none()
        if ticket is None:
            return False
        ticket_amount = 0
        ticket_flights = self.session.query(TicketFlight).filter(TicketFlight.ticket_no == ticket.ticket_no).all()
        boarding_passes = self.session.query(BoardingPass).filter(BoardingPass.ticket_no == ticket.ticket_no)
        for boarding_pass in boarding_passes:
            self.session.delete(boarding_pass)
        self.session.flush()
        for ticket_flight in ticket_flights:
            ticket_amount += ticket_flight.amount
            self.session.delete(ticket_flight)
        self.session.flush()
        booking = self.session.query(Booking).get(ticket.book_ref)
        booking.total_amount -= ticket_amount
        self.session.add(booking)
        self.session.flush()
        self.session.delete(ticket)
        self.session.commit()
        return True

    async def put_ticket(self, ticket_no: str, data: TicketUpdate):
        return self.base_put(Ticket, ticket_no, data)
