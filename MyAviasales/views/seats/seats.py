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
    """
    Валидатор номера сиденья в самолёте

    :param code:
    :return: Валидный/ не валидный
    """
    return 2 <= len(code) <= 3


def valid_aircraft_code(code) -> bool:
    """
    Валидатор кода самолёта

    :param code: Код самолёта
    :return: Валидный/ не валидный
    """
    return len(code) == 3


@router.get("/")
async def multiple_get(db: Session = Depends(get_db),
                       page: Optional[int] = 0
                       ) -> Optional[List[SeatBase]]:
    """
    Вьюха для получения всех сидений

    :param db: Сессия для работы с бд
    :param page: Номер страницы
    :return: Сформированый ответ в формате JSON
    """
    res = await SeatController(db).get_all_seats(page=page)
    if len(res) == 0:
        raise HTTPException(status_code=404, detail="Seat not found")
    return res


@router.get("/{aircraft_code}/{seat_no}")
async def single_get(seat_no: str, aircraft_code: str, db: Session = Depends(get_db)) -> SeatBase:
    """
    Вьюха для получения сиденья по его номеру и номеру самолёта

    :param seat_no: Номер места в самолёте
    :param aircraft_code: Код самолёта
    :param db: Сессия для работы с бд
    :return: Сформированый ответ в формате JSON
    """
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
    """
    Вьюха для создания сиденья в самолёте

    :param data: Данные требуемые для работы контроллера
    :param db: Сессия для работы с бд
    :return: Сформированый ответ в формате JSON
    """
    res = await SeatController(db).post_seat(data)
    if not res:
        raise HTTPException(status_code=404, detail="Seat already exist")
    return res


@router.delete("/{aircraft_code}/{seat_no}")
async def delete(seat_no: str, aircraft_code: str, db: Session = Depends(get_db)):
    """
    Вьюха для удаления сиденья

    :param seat_no: Номер места в самолёте
    :param aircraft_code: Код самолёта
    :param db: Сессия для работы с бд
    :return: Сформированый ответ в формате JSON
    """
    if not valid_seat_no(seat_no):
        raise HTTPException(status_code=422, detail="seat_no must be 3 characters")
    if not valid_aircraft_code(aircraft_code):
        raise HTTPException(status_code=422, detail="aircraft_code must be 3 characters")
    if not await SeatController(db).delete_seat(seat_no, aircraft_code):
        raise HTTPException(status_code=404, detail="Seat not found")


@router.put("/{aircraft_code}/{seat_no}")
async def put(data: SeatUpdate, seat_no: str, aircraft_code: str, db: Session = Depends(get_db)):
    """
    Вьюха для обновления сиденья

    :param data: Данные требуемые для работы контроллера
    :param seat_no: Номер места в самолёте
    :param aircraft_code: Код самолёта
    :param db: Сессия для работы с бд
    :return: Сформированый ответ в формате JSON
    """
    if not valid_seat_no(seat_no):
        raise HTTPException(status_code=422, detail="seat_no must be 3 characters")
    if not valid_aircraft_code(aircraft_code):
        raise HTTPException(status_code=422, detail="aircraft_code must be 3 characters")
    if not await SeatController(db).put_seat(seat_no, aircraft_code, data):
        raise HTTPException(status_code=404, detail="Seat not found")
