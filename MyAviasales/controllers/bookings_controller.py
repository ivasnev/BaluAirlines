import json

from MyAviasales.controllers.base_controller import BaseController
from MyAviasales.models import Booking, Ticket, TicketFlight, Seat, Flight
from .ticket_controller import TicketController
from typing import Optional, List
from MyAviasales.views.bookings.schema import BookingBase, BookingUpdate, BookingResponse


class BookingController(BaseController):
    async def get_all_bookings(self, page: int) -> Optional[List[BookingBase]]:
        page_size = 50
        with self.session.begin():
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

    async def get_single_booking(self, key: str) -> Optional[BookingBase]:
        booking = self.session.query(Booking.book_ref,
                                     Booking.book_date,
                                     Booking.total_amount).filter_by(
            book_ref=key).first()
        if booking:
            booking = BookingResponse.from_orm(booking)
            booking.tickets = TicketController(self.session).get_all_ticket_by_book_ref(key)
        return booking

    async def post_booking(self, data: dict) -> bool:
        book_ref = self.generate_varchar_key(6, Booking)
        self.session.add(Booking(book_ref=book_ref,
                                 book_date=data['book_date'],
                                 total_amount=0,
                                 ))
        self.session.flush()
        for passenger in data['passengers']:
            ticket_no = self.generate_varchar_key(13, Ticket)
            self.session.add(
                Ticket(
                    ticket_no=ticket_no,
                    book_ref=book_ref,
                    passenger_id=passenger['passenger_id'],
                    passenger_name=passenger['passenger_name'],
                    contact_data=json.loads(data["contact_data"]) if passenger.get('contact_data') else None,
                )
            )
            self.session.flush()
            amounts = {'Business': 51235.75, 'Economy': 15959.84, 'Comfort': 32740.55}
            for flight in data['flights']:
                booking = self.session.query(Booking).get(book_ref)
                fare_conditions = self.session.query(Seat.fare_conditions).filter(
                    Flight.flight_id == flight['flight_id']).filter(Flight.aircraft_code == Seat.aircraft_code)
                self.session.add(
                    TicketFlight(
                        ticket_no=ticket_no,
                        flight_id=flight['flight_id'],
                        fare_conditions=fare_conditions,
                        amount=amounts[fare_conditions],
                    )
                )
                booking.total_amount += amounts[fare_conditions]
                self.session.flush()
        self.session.commit()
        return True

    async def delete_booking(self, key: str) -> bool:
        self.session.delete(self.session.query(Booking).get(key))
        return True

    async def put_booking(self, _key: str, data: dict) -> bool:
        obj_to_update = self.session.query(Booking).filter_by(
            book_ref=_key).first()
        for key, value in data.items():
            obj_to_update.__setattr__(key, value)
        self.session.flush()
        self.session.commit()
        return True
