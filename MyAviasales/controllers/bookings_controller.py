import json

from datetime import datetime
from MyAviasales.controllers.base_controller import BaseController
from MyAviasales.models import Booking, Ticket, TicketFlight, Flight, AirportsDatum
from .ticket_controller import TicketController
from typing import Optional, List
from MyAviasales.views.bookings.schema import BookingBase, BookingUpdate, BookingResponse, BookingPostRequest


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

    async def post_booking(self, data: BookingPostRequest) -> bool:
        book_ref = self.generate_varchar_key(6, Booking)
        total_amount = 0
        tickets = []
        for passenger in data.passengers:
            ticket_no = self.generate_varchar_key(13, Ticket)
            tickets.append(ticket_no)
            self.session.add(Ticket(
                ticket_no=ticket_no,
                book_ref=book_ref,
                passenger_id=passenger.passenger_id,
                passenger_name=passenger.passenger_name,
                contact_data=passenger.contact_data,
            ))
            self.session.flush()
        for flight_id in data.flights:
            flight = self.session.query(Flight.departure_airport,
                                        Flight.arrival_airport
                                        ).get(flight_id).one_or_none()
            departure_airport = self.session.query(AirportsDatum.coordinates).filter(
                AirportsDatum.airport_code == flight.departure_airport).first()[0]
            arrival_airport = self.session.query(AirportsDatum.coordinates).filter(
                AirportsDatum.airport_code == flight.arrival_airport).first()[0]
            amount = self.get_dist(eval(departure_airport), eval(arrival_airport))
            for ticket_no in tickets:
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
        self.session.add(Booking(book_ref=book_ref,
                                 book_date=datetime.now(),
                                 total_amount=total_amount,
                                 ))
        self.session.flush()
        self.session.rollback()
        # self.session.commit()
        return True

    async def delete_booking(self, key: str) -> bool:
        booking = self.session.query(Booking).get(key).one_or_none()
        if booking is None:
            return False
        tickets = self.session.query(Ticket).get(book_ref=key).all()
        for ticket in tickets:
            ticket_flight = self.session.query(TicketFlight).get(ticket.ticket_no).all()
            self.session.delete(ticket_flight)
            self.session.flush()
        self.session.delete(tickets)
        self.session.flush()
        self.session.delete(booking)
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
