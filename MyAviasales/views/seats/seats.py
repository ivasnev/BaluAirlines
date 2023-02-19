from study_proj.controllers.seat_controller import SeatController
from study_proj.views.seats.validators import (SeatsPostValidator, SeatsPutValidator, id_validator)
from cornice.resource import resource, view
from sqlalchemy import update
from study_proj.models import Seat
from cornice.validators import colander_body_validator


@resource(collection_path='/seats', path='/seats/{aircraft_code}/{seat_no}')
class Seats(object):

    def __init__(self, request, context=None):
        self.request = request
        self.controller = SeatController(self.request.db)

    @view(renderer="json", validators=id_validator)
    def get(self):
        """Получение одного места"""
        return self.controller.get_single_seat(self.request.matchdict)

    def collection_get(self):
        """Получение всех мест"""
        return self.controller.get_all_seats()

    @view(renderer="json", schema=SeatsPostValidator(), validators=colander_body_validator)
    def collection_post(self):
        """Добавление места"""
        data_to_insert = {}
        for key in self.request.params:
            if self.request.params[key] != 'null' and self.request.params[key]:
                data_to_insert[key] = self.request.params[key]
            else:
                data_to_insert[key] = None
        return self.controller.post_seat(data_to_insert)

    @view(renderer="json", validators=id_validator)
    def delete(self):
        """Удаление места"""
        return self.controller.delete_seat(self.request.matchdict)

    @view(renderer="json", schema=SeatsPutValidator(), validators=colander_body_validator)
    def put(self):
        """Обновление информации"""
        data_to_update = {}
        for key in self.request.params:
            if self.request.params.get(key, default=None):
                data_to_update[key] = self.request.params[key]
        return self.controller.put_seat(self.request.matchdict, data_to_update)
