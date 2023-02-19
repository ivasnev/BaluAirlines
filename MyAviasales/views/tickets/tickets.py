# coding: utf-8

import json

from cornice.resource import resource, view
from sqlalchemy import update

from study_proj.controllers.ticket_controller import TicketController
from study_proj.models import Ticket
from study_proj.views.tickets.validators import (ticket_no_validator,
                                                 request_validator)


@resource(collection_path="/tickets", path="/ticket/{book_ref}/{ticket_no}")
class Ticket(object):
    def __init__(self, request, context=None):
        self.request = request
        self.controller = TicketController(self.request.db)

    def collection_get(self):
        return self.controller.get_all_tickets()

    @view(renderer="json", validators=ticket_no_validator)
    def get(self):
        return self.controller.get_single_ticket(self.request.matchdict)

    @view(renderer="json", validators=request_validator("post_ticket"))
    def collection_post(self):
        return self.controller.post_ticket(self.request.POST)

    @view(renderer="json", validators=ticket_no_validator)
    def delete(self):
        return self.controller.delete_ticket(self.request.matchdict)

    @view(renderer="json", validators=request_validator("put_ticket"))
    def put(self):
        data_to_update = {}
        keys = ['book_ref', 'passenger_id', 'passenger_name', 'contact_data']
        for key in keys:
            if self.request.POST.get(key, default=None):
                data_to_update[key] = self.request.params[key]
        return self.controller.put_ticket({**self.request.matchdict, **data_to_update})
