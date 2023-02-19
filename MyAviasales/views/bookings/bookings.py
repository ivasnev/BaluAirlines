# coding: utf-8
from study_proj.models import Booking
from cornice.resource import resource, view
import sqlalchemy as sa
from .schema import *
from cornice.validators import colander_body_validator
from study_proj.controllers.bookings_controller import BookingController


@resource(collection_path='/bookings', path='/bookings/{book_ref}')
class Bookings(object):

    def __init__(self, request, context=None):
        self.request = request
        self.controller = BookingController(self.request.db)

    def collection_get(self) -> list:
        return self.controller.get_all_bookings(int(self.request.params.get('page', default=0)))

    def get(self) -> dict:
        return self.controller.get_single_booking(self.request.matchdict['book_ref'])

    @view(schema=BookingPost(), validators=(colander_body_validator,))
    def collection_post(self):
        return self.controller.post_booking({'book_ref': self.request.params['book_ref'],
                                             'book_date': self.request.params['book_date'],
                                             'total_amount': self.request.params['total_amount']})

    # TODO make cascade delete
    def delete(self):
        return self.controller.delete_booking(self.request.matchdict['book_ref'])

    @view(schema=BookingPut(), validators=(colander_body_validator,))
    def put(self):
        data_to_update = {}
        keys = ['book_date', 'total_amount', 'book_ref']
        for key in keys:
            if self.request.params.get(key, default=None):
                data_to_update[key] = self.request.params[key]
        return self.controller.put_booking(self.request.matchdict['book_ref'], data_to_update)
