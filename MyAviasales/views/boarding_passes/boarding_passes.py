# coding: utf-8

from MyAviasales.controllers.boarding_pass_controller import BoardingPassController
from fastapi import APIRouter, Depends, HTTPException
from MyAviasales.DataBase.database import get_db
from .schema import *
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(
    prefix="/boarding_pass",
    tags=["boarding_pass"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


def valid_ticket_no(code) -> bool:
    return 0 < len(code) <= 13


@router.get("/")
async def multiple_get(db: Session = Depends(get_db),
                       page: Optional[int] = 0
                       ) -> Optional[List[BoardingPassBase]]:
    res = await BoardingPassController(db).get_all_boarding_passes(page=page)
    if len(res) == 0:
        raise HTTPException(status_code=404, detail="Boarding passes not found")
    return res


@router.get("/{flight_id}/{ticket_no}")
async def single_get(ticket_no: str, flight_id: int, db: Session = Depends(get_db)) -> BoardingPassBase:
    if not valid_ticket_no(ticket_no):
        raise HTTPException(status_code=422, detail="ticket_no must be 3 characters")
    res = await BoardingPassController(db).get_single_boarding_pass(ticket_no, flight_id)
    if res is None:
        raise HTTPException(status_code=404, detail="Boarding pass not found")
    return res


@router.post("/")
async def post(data: BoardingPassPost, db: Session = Depends(get_db)) -> bool:
    controller = BoardingPassController(db)
    if not await controller.ticket_flight_exist(data.flight_id, data.ticket_no):
        raise HTTPException(status_code=422, detail="ticket_no not exist on this flight")
    if not await controller.seat_no_available(data.flight_id, data.seat_no):
        raise HTTPException(status_code=422, detail="Seat already booked")
    res = await BoardingPassController(db).post_boarding_pass(data)
    if not res:
        raise HTTPException(status_code=422, detail="Boarding pass already exist")
    return res


@router.delete("/{flight_id}/{ticket_no}")
async def delete(ticket_no: str, flight_id: int, db: Session = Depends(get_db)):
    if not valid_ticket_no(ticket_no):
        raise HTTPException(status_code=422, detail="ticket_no must be 3 characters")
    if not await BoardingPassController(db).delete_boarding_pass(ticket_no, flight_id):
        raise HTTPException(status_code=404, detail="Boarding pass not found")


@router.put("/{flight_id}/{ticket_no}")
async def put(data: BoardingPassUpdate, ticket_no: str, flight_id: int, db: Session = Depends(get_db)):
    if not valid_ticket_no(ticket_no):
        raise HTTPException(status_code=422, detail="ticket_no must be 3 characters")
    if not await BoardingPassController(db).put_boarding_pass(ticket_no, flight_id, data):
        raise HTTPException(status_code=404, detail="Boarding pass not found")
