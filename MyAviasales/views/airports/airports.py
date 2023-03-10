# coding: utf-8
from MyAviasales.controllers.airport_controller import AirportController
from fastapi import APIRouter, Depends, HTTPException
from MyAviasales.DataBase.database import get_db
from .schema import *
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(
    prefix="/airports",
    tags=["airports"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


def valid_airport_code(code) -> bool:
    return len(code) == 3


@router.get("/")
async def multiple_get(db: Session = Depends(get_db)
                       ) -> Optional[List[AirportBase]]:
    res = await AirportController(db).get_all_airports()
    if len(res) == 0:
        raise HTTPException(status_code=404, detail="Airport not found")
    return res


@router.get("/{airport_code}")
async def single_get(airport_code: str, db: Session = Depends(get_db)) -> AirportBase:
    if not valid_airport_code(airport_code):
        raise HTTPException(status_code=422, detail="airport_code must be 3 characters")
    res = await AirportController(db).get_single_airport(airport_code)
    if res is None:
        raise HTTPException(status_code=404, detail="Airport not found")
    return res


@router.post("/", responses={404: {"description": "Airport already exist"}})
async def post(data: AirportBase, db: Session = Depends(get_db)) -> bool:
    res = await AirportController(db).post_airport(data)
    if not res:
        raise HTTPException(status_code=404, detail="Airport already exist")
    return res


@router.delete("/{airport_code}")
async def delete(airport_code: str, db: Session = Depends(get_db)):
    if not valid_airport_code(airport_code):
        raise HTTPException(status_code=422, detail="airport_code must be 3 characters")
    if not await AirportController(db).delete_airport(airport_code):
        raise HTTPException(status_code=404, detail="Airport not found")


@router.put("/{airport_code}")
async def put(data: AirportUpdate, airport_code: str, db: Session = Depends(get_db)):
    if not valid_airport_code(airport_code):
        raise HTTPException(status_code=422, detail="airport_code must be 3 characters")
    if not await AirportController(db).put_airport(airport_code, data):
        raise HTTPException(status_code=404, detail="Airport not found")
