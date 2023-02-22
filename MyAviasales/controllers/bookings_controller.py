import json

from datetime import datetime
from MyAviasales.controllers.base_controller import BaseController
from MyAviasales.models import Booking, Ticket, TicketFlight, Flight, AirportsDatum
from .ticket_controller import TicketController
from typing import Optional, List
from MyAviasales.views.bookings.schema import BookingBase, BookingUpdate, BookingResponse, BookingPostRequest
from MyAviasales.views.tickets.schema import TicketBase


class BookingController(BaseController):
    async def get_all_bookings(self, page: int) -> Optional[List[BookingResponse]]:
        page_size = 50
        bookings_query = self.session.query(Booking.book_ref,
                                            Booking.book_date,
                                            Booking.total_amount).limit(page_size).offset(
            int(page) * page_size)
        if bookings_query is None:
            return None
        bookings = [BookingResponse.from_orm(x) for x in bookings_query if x is not None]
        for booking in bookings:
            booking.tickets = await TicketController(self.session) \
                .get_all_ticket_by_book_ref(booking.book_ref)
        return bookings

    async def get_single_booking(self, key: str) -> Optional[BookingResponse]:
        booking = self.session.query(Booking.book_ref,
                                     Booking.book_date,
                                     Booking.total_amount).filter_by(
            book_ref=key).first()
        if booking:
            booking = BookingResponse.from_orm(booking)
            booking.tickets = await TicketController(self.session).get_all_ticket_by_book_ref(key)
        return booking

    async def post_booking(self, data: BookingPostRequest) -> Optional[BookingResponse]:
        book_ref = self.generate_varchar_key(6, Booking)
        booking = Booking(book_ref=book_ref,
                          book_date=datetime.now(),
                          total_amount=0)
        self.session.add(booking)
        self.session.flush()
        total_amount = 0
        tickets_no = []
        tickets = []
        for passenger in data.passengers:
            ticket_no = self.generate_varchar_key(13, Ticket)
            tickets_no.append(ticket_no)
            ticket = Ticket(
                ticket_no=ticket_no,
                book_ref=book_ref,
                passenger_id=passenger.passenger_id,
                passenger_name=passenger.passenger_name,
                contact_data=dict(passenger.contact_data),
            )
            self.session.add(ticket)
            self.session.flush()
            tickets.append(ticket)
        for flight_id in data.flights:
            flight = self.session.query(Flight.departure_airport,
                                        Flight.arrival_airport,
                                        Flight.scheduled_departure
                                        ).filter(Flight.flight_id == flight_id).one_or_none()
            if flight is None:
                return None
            departure_airport = self.session.query(AirportsDatum.coordinates).filter(
                AirportsDatum.airport_code == flight.departure_airport).first()[0]
            arrival_airport = self.session.query(AirportsDatum.coordinates).filter(
                AirportsDatum.airport_code == flight.arrival_airport).first()[0]
            amount = self.generate_cost(
                fare_conditions=data.fare_condition,
                dist=self.get_dist(eval(departure_airport), eval(arrival_airport)),
                date=flight.scheduled_departure
            )
            for ticket_no in tickets_no:
                self.session.add(
                    TicketFlight(
                        ticket_no=ticket_no,
                        flight_id=flight_id,
                        fare_conditions=data.fare_condition,
                        amount=amount
                    )
                )
                total_amount += amount
            self.session.flush()
        booking.total_amount = total_amount
        self.session.flush()
        booking = BookingResponse.from_orm(booking)
        booking.tickets = [TicketBase.from_orm(x) for x in tickets]
        # self.session.rollback()
        self.session.commit()
        return booking

    async def delete_booking(self, key: str) -> bool:
        booking = self.session.query(Booking).get(key)
        if booking is None:
            return False
        tickets = self.session.query(Ticket).filter(Ticket.book_ref == key).all()
        for ticket in tickets:
            ticket_flight = self.session.query(TicketFlight).filter(TicketFlight.ticket_no == ticket.ticket_no).all()
            for obj_to_delete in ticket_flight:
                self.session.delete(obj_to_delete)
            self.session.flush()
            self.session.delete(ticket)
        self.session.flush()
        self.session.delete(booking)
        self.session.commit()
        return True

    async def put_booking(self, book_ref: str, data: BookingUpdate) -> bool:
        return self.base_put(Booking, book_ref, data)
        # obj_to_update = self.session.query(Booking).get(book_ref).one_or_none()
        # if obj_to_update is None:
        #     return False
        # data = data.dict()
        # for key, value in data.items():
        #     if value:
        #         obj_to_update.__setattr__(key, value)
        # self.session.flush()
        # self.session.commit()
        # return True
