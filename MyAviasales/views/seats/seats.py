# coding: utf-8
from MyAviasales.controllers.seat_controller import SeatController
from fastapi import APIRouter, Depends, HTTPException
from MyAviasales.DataBase.database import get_db
from .schema import SeatBase, SeatUpdate
from sqlalchemy.orm import Session
from typing import List, Optional

router = APIRouter(
    prefix="/seats",
    tags=["seats"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


def valid_seat_no(code) -> bool:
    return 2 <= len(code) <= 3


def valid_aircraft_code(code) -> bool:
    return len(code) == 3


@router.get("/")
async def multiple_get(db: Session = Depends(get_db),
                       page: Optional[int] = 0
                       ) -> Optional[List[SeatBase]]:
    res = await SeatController(db).get_all_seats(page=page)
    if len(res) == 0:
        raise HTTPException(status_code=404, detail="Seat not found")
    return res


@router.get("/{aircraft_code}/{seat_no}")
async def single_get(seat_no: str, aircraft_code: str, db: Session = Depends(get_db)) -> SeatBase:
    if not valid_seat_no(seat_no):
        raise HTTPException(status_code=422, detail="seat_no must be 3 characters")
    if not valid_aircraft_code(aircraft_code):
        raise HTTPException(status_code=422, detail="aircraft_code must be 3 characters")
    res = await SeatController(db).get_single_seat(seat_no, aircraft_code)
    if res is None:
        raise HTTPException(status_code=404, detail="Seat not found")
    return res


@router.post("/", responses={404: {"description": "Seat already exist"}})
async def post(data: SeatBase, db: Session = Depends(get_db)) -> bool:
    res = await SeatController(db).post_seat(data)
    if not res:
        raise HTTPException(status_code=404, detail="Seat already exist")
    return res


@router.delete("/{aircraft_code}/{seat_no}")
async def delete(seat_no: str, aircraft_code: str, db: Session = Depends(get_db)):
    if not valid_seat_no(seat_no):
        raise HTTPException(status_code=422, detail="seat_no must be 3 characters")
    if not valid_aircraft_code(aircraft_code):
        raise HTTPException(status_code=422, detail="aircraft_code must be 3 characters")
    if not await SeatController(db).delete_seat(seat_no, aircraft_code):
        raise HTTPException(status_code=404, detail="Seat not found")


@router.put("/{aircraft_code}/{seat_no}")
async def put(data: SeatUpdate, seat_no: str, aircraft_code: str, db: Session = Depends(get_db)):
    if not valid_seat_no(seat_no):
        raise HTTPException(status_code=422, detail="seat_no must be 3 characters")
    if not valid_aircraft_code(aircraft_code):
        raise HTTPException(status_code=422, detail="aircraft_code must be 3 characters")
    if not await SeatController(db).put_seat(seat_no, aircraft_code, data):
        raise HTTPException(status_code=404, detail="Seat not found")

# from study_proj.controllers.seat_controller import SeatController
# from study_proj.views.seats.validators import (SeatsPostValidator, SeatsPutValidator, id_validator)
# from cornice.resource import resource, view
# from sqlalchemy import update
# from study_proj.models import Seat
# from cornice.validators import colander_body_validator
# 
# 
# @resource(collection_path='/seats', path='/seats/{aircraft_code}/{seat_no}')
# class Seats(object):
# 
#     def __init__(self, request, context=None):
#         self.request = request
#         self.controller = SeatController(self.request.db)
# 
#     @view(renderer="json", validators=id_validator)
#     def get(self):
#         """Получение одного места"""
#         return self.controller.get_single_seat(self.request.matchdict)
# 
#     def collection_get(self):
#         """Получение всех мест"""
#         return self.controller.get_all_seats()
# 
#     @view(renderer="json", schema=SeatsPostValidator(), validators=colander_body_validator)
#     def collection_post(self):
#         """Добавление места"""
#         data_to_insert = {}
#         for key in self.request.params:
#             if self.request.params[key] != 'null' and self.request.params[key]:
#                 data_to_insert[key] = self.request.params[key]
#             else:
#                 data_to_insert[key] = None
#         return self.controller.post_seat(data_to_insert)
# 
#     @view(renderer="json", validators=id_validator)
#     def delete(self):
#         """Удаление места"""
#         return self.controller.delete_seat(self.request.matchdict)
# 
#     @view(renderer="json", schema=SeatsPutValidator(), validators=colander_body_validator)
#     def put(self):
#         """Обновление информации"""
#         data_to_update = {}
#         for key in self.request.params:
#             if self.request.params.get(key, default=None):
#                 data_to_update[key] = self.request.params[key]
#         return self.controller.put_seat(self.request.matchdict, data_to_update)
