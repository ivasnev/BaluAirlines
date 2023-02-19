# coding: utf-8
from MyAviasales.controllers.aircraft_controller import AircraftController
from fastapi import APIRouter, Depends, HTTPException, Path
from MyAviasales.DataBase.database import get_db
from .schema import *
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(
    prefix="/aircraft",
    tags=["aircraft"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


def valid_aircraft_code(code) -> bool:
    return len(code) == 3


@router.get("/")
async def multiple_get(db: Session = Depends(get_db)) -> List[AircraftBase]:
    res = await AircraftController(db).get_all_aircraft()
    if res is None:
        raise HTTPException(status_code=404, detail="Aircraft not found")
    return res


@router.get("/{aircraft_code}")
async def single_get(aircraft_code: str, db: Session = Depends(get_db)) -> AircraftBase:
    if not valid_aircraft_code(aircraft_code):
        raise HTTPException(status_code=422, detail="aircraft_code must be 3 characters")
    res = await AircraftController(db).get_single_aircraft(aircraft_code)
    if res is None:
        raise HTTPException(status_code=404, detail="Aircraft not found")
    return res


@router.post("/", responses={404: {"description": "Aircraft already exist"}})
async def post(data: AircraftBase, db: Session = Depends(get_db)) -> AircraftBase:
    res = await AircraftController(db).post_aircraft(data)
    if res is None:
        raise HTTPException(status_code=404, detail="Aircraft already exist")
    return res


@router.delete("/{aircraft_code}")
async def delete(aircraft_code: str, db: Session = Depends(get_db)) -> AircraftBase:
    if not valid_aircraft_code(aircraft_code):
        raise HTTPException(status_code=422, detail="aircraft_code must be 3 characters")
    res = await AircraftController(db).delete_aircraft(aircraft_code)
    if res is None:
        raise HTTPException(status_code=404, detail="Aircraft not found")
    return res


@router.put("/{aircraft_code}")
async def put(data: AircraftUpdate, aircraft_code: str, db: Session = Depends(get_db)) -> AircraftBase:
    if not valid_aircraft_code(aircraft_code):
        raise HTTPException(status_code=422, detail="aircraft_code must be 3 characters")
    res = await AircraftController(db).put_aircraft(aircraft_code, data)
    if res is None:
        raise HTTPException(status_code=404, detail="Aircraft not found")
    return res
