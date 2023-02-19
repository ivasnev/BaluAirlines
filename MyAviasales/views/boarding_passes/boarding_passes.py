# coding: utf-8
from cornice.resource import resource, view

from study_proj.controllers.boarding_pass_controller import BoardingPassController
from study_proj.views.boarding_passes.validators import (request_validator)


@resource(collection_path="/boarding_passes", path="/boarding_pass/{ticket_no}/{flight_id}")
class BoardingPass(object):
    def __init__(self, request, context=None):
        self.request = request
        self.controller = BoardingPassController(self.request.db)

    def collection_get(self):
        return self.controller.get_all_boarding_passes()

    @view(renderer="json")
    def get(self):
        return self.controller.get_single_boarding_pass(self.request.matchdict)

    @view(renderer="json", validators=request_validator("post_boarding_pass"))
    def collection_post(self):
        return self.controller.post_boarding_pass(self.request.POST)

    @view(renderer="json")
    def delete(self):
        return self.controller.delete_boarding_pass(self.request.matchdict)

    @view(renderer="json", validators=request_validator("put_boarding_pass"))
    def put(self):
        # data_to_update = {}
        # keys = ['ticket_no', 'flight_id', 'boarding_no', 'seat_no']
        # for key in keys:
        #     if self.request.POST.get(key, default=None):
        #         data_to_update[key] = self.request.params[key]
        return self.controller.put_ticket({**self.request.matchdict, **self.request.POST})
