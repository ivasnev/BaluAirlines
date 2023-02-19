from study_proj.controllers.airport_controller import AirportController
from study_proj.views.airports.validators import (AirportsPostValidator, AirportsPutValidator, id_validator)
from cornice.resource import resource, view
from sqlalchemy import update
from study_proj.models import AirportsDatum
from cornice.validators import colander_body_validator
import json


@resource(collection_path='/airports', path='/airports/{airport_code}')
class Airports(object):

    def __init__(self, request, context=None):
        self.request = request
        self.controller = AirportController(self.request.db)

    @view(renderer="json", validators=id_validator)
    def get(self):
        """Получение одного аэропорта"""
        return self.controller.get_single_airport(self.request.matchdict['airport_code'])

    def collection_get(self):
        """Получение всех аэропортов"""
        return self.controller.get_all_airports()

    @view(renderer="json", schema=AirportsPostValidator(), validators=colander_body_validator)
    def collection_post(self):
        """Добавление аэропорта"""
        data_to_insert = {}
        for key in self.request.params:
            if self.request.params[key] != 'null' and self.request.params[key]:
                if key in ['airport_name', 'city']:
                    data_to_insert[key] = json.loads(self.request.params[key])
                else:
                    data_to_insert[key] = self.request.params[key]
            else:
                data_to_insert[key] = None
        return self.controller.post_airport(data_to_insert)

    @view(renderer="json", validators=id_validator)
    def delete(self):
        """Удаление аэропорта"""
        return self.controller.delete_airport(self.request.matchdict)

    @view(renderer="json", schema=AirportsPutValidator(), validators=colander_body_validator)
    def put(self):
        """Обновление информации"""
        data_to_update = {}
        for key in self.request.params:
            if key in ["airport_name", "city"]:
                data_to_update[key] = json.loads(self.request.params[key])
            else:
                if self.request.params.get(key, default=None):
                    data_to_update[key] = self.request.params[key]
        return self.controller.put_airport(self.request.matchdict, data_to_update)