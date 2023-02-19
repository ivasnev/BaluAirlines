# coding: utf-8
from study_proj.models import Flight
from cornice.resource import resource, view
import sqlalchemy as sa
from .schema import *
from cornice.validators import colander_body_validator
from study_proj.controllers.ticket_flights_controller import TicketFlightController


@resource(collection_path='/ticket_flights', path='/ticket_flights/{ticket_no}/{flight_id}')
class TicketFlights(object):

    def __init__(self, request, context=None):
        self.request = request
        self.controller = TicketFlightController(self.request.db)

    def collection_get(self) -> list:
        return self.controller.get_all_ticket_flights(int(self.request.params.get('page', default=0)))

    def get(self) -> dict:
        return self.controller.get_single_ticket_flight({
            'flight_id': self.request.matchdict['flight_id'],
            'ticket_no': self.request.matchdict['ticket_no']
        })

    # @view(schema=TicketFlightsPost(), validators=(colander_body_validator,))
    # def collection_post(self):
    #     data_to_ins = {}
    #     for key in self.request.params:
    #         data_to_ins[key] = None
    #     return self.controller.post_ticket_flight(data_to_ins)
    #
    # # TODO make cascade delete
    # def delete(self):
    #     return self.controller.delete_ticket_flight({
    #         'flight_id': self.request.matchdict['flight_id'],
    #         'ticket_no': self.request.matchdict['ticket_no']
    #     })

    @view(schema=TicketFlightsPut(), validators=(colander_body_validator,))
    def put(self):
        data_to_update = {}
        keys = [
            'amount'
        ]
        for key in keys:
            if self.request.params.get(key, default=None):
                data_to_update[key] = self.request.params[key]
        return self.controller.put_ticket_flight({
            'flight_id': self.request.matchdict['flight_id'],
            'ticket_no': self.request.matchdict['ticket_no']
        }, data_to_update)
