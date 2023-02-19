# coding: utf-8
from MyAviasales.controllers.flights_controller import FlightController
from fastapi import APIRouter, Depends, HTTPException, Path
from MyAviasales.DataBase.database import get_db
from .schema import *
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

router = APIRouter(
    prefix="/flights",
    tags=["flights"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


def valid_flight_no(code) -> bool:
    return len(code) == 6


@router.get("/all")
async def multiple_get(page: Optional[int] = 0,
                       db: Session = Depends(get_db)
                       ) -> Optional[List[FlightBase]]:
    res = await FlightController(db).get_all_flights(page=page)
    if len(res) == 0:
        raise HTTPException(status_code=404, detail="Flight not found")
    return res


@router.get("/")
async def filter_get(
        departure_airport: Optional[str] = 'VKO',
        arrival_airport: Optional[str] = 'VVO',
        max_transits: Optional[int] = 2,
        departure_date: Optional[datetime] = datetime.now(),
        db: Session = Depends(get_db),
) -> List[Optional[FlightPath]]:
    res = await FlightController(db).get_flights_from_to_(
        departure_date=departure_date,
        departure_airport=departure_airport,
        arrival_airport=arrival_airport,
        max_transits=max_transits
    )
    if len(res) == 0:
        raise HTTPException(status_code=404, detail="Flight not found")
    return res


@router.get("/no/{flight_no}")
async def single_get(flight_no: str,
                     date: Optional[datetime] = datetime.now(),
                     db: Session = Depends(get_db)) -> FlightBase:
    if not valid_flight_no(flight_no):
        raise HTTPException(status_code=422, detail="flight_no must be 6 characters")
    res = await FlightController(db).get_single_flight_by_no_and_date(flight_no, date)
    if res is None:
        raise HTTPException(status_code=404, detail="Flight not found")
    return res


@router.get("/id/{flight_id}")
async def single_get(flight_id: int, db: Session = Depends(get_db)) -> FlightBase:
    res = await FlightController(db).get_single_flight_by_id(flight_id)
    if res is None:
        raise HTTPException(status_code=404, detail="Flight not found")
    return res


@router.get("/path/{departure_airport}/{arrival_airport}")
async def single_get(departure_airport: str,
                     arrival_airport: str,
                     departure_date: Optional[datetime] = datetime.now(),
                     db: Session = Depends(get_db)) -> FlightBase:
    res = await FlightController(db).get_single_flight_from_to(
        departure_airport, arrival_airport, departure_date)
    if res is None:
        raise HTTPException(status_code=404, detail="Flight not found")
    return res


@router.post("/")
async def post(data: FlightBase, db: Session = Depends(get_db)) -> FlightBase:
    res = await FlightController(db).post_flight(data)
    return res


@router.delete("/{flight_id}")
async def delete(flight_id: int, db: Session = Depends(get_db)):
    if not await FlightController(db).delete_flight(flight_id):
        raise HTTPException(status_code=404, detail="Flight not found")


@router.put("/{flight_id}")
async def put(data: FlightUpdate, flight_id: int, db: Session = Depends(get_db)):
    if not await FlightController(db).put_flight(flight_id, data):
        raise HTTPException(status_code=404, detail="Flight not found")
