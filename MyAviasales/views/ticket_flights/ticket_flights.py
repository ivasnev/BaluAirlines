# coding: utf-8

from MyAviasales.controllers.ticket_flights_controller import TicketFlightController
from fastapi import APIRouter, Depends, HTTPException
from MyAviasales.DataBase.database import get_db
from .schema import TicketFlightBase, TicketFlightUpdate
from sqlalchemy.orm import Session
from typing import List, Optional

router = APIRouter(
    prefix="/ticket_flights",
    tags=["ticket_flights"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


def valid_ticket_no(code) -> bool:
    """
    Валидатор для номера билета

    :param code: Номер билета
    :return: Валидный/ не валидный
    """
    return len(code) == 13


@router.get("/")
async def multiple_get(db: Session = Depends(get_db),
                       page: Optional[int] = 0
                       ) -> Optional[List[TicketFlightBase]]:
    """
    Вьюха для получения всех связей между билетом и рейсом

    :param db: Сессия для работы с бд
    :param page: Номер страницы
    :return: Сформированый ответ в формате JSON
    """
    res = await TicketFlightController(db).get_all_ticket_flights(page=page)
    if len(res) == 0:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return res


@router.get("/{ticket_no}/{flight_id}")
async def single_get(ticket_no: str, flight_id: int, db: Session = Depends(get_db)) -> TicketFlightBase:
    """
    Вьюха для получения связи между билетом и перелётом

    :param ticket_no: Номер билета
    :param flight_id: Номер рейса
    :param db: Сессия для работы с бд
    :return: Сформированый ответ в формате JSON
    """
    if not valid_ticket_no(ticket_no):
        raise HTTPException(status_code=422, detail="ticket_no must be 13 characters")
    res = await TicketFlightController(db).get_single_ticket_flight(ticket_no, flight_id)
    if res is None:
        raise HTTPException(status_code=404, detail="Pair ticket flight not found")
    return res


@router.post("/")
async def post(data: TicketFlightBase, db: Session = Depends(get_db)) -> bool:
    """
    Вьюха для создания связи билета и перелёта

    :param data: Данные требуемые для работы контроллера
    :param db: Сессия для работы с бд
    :return: Сформированый ответ в формате JSON
    """
    res = await TicketFlightController(db).post_ticket_flight(data)
    if not res:
        raise HTTPException(status_code=404, detail="Ticket already exist")
    return res


@router.delete("/{ticket_no}/{flight_id}")
async def delete(ticket_no: str, flight_id: int, db: Session = Depends(get_db)):
    """
    Вьюха для удаления связи билета и перелёта

    :param ticket_no: Номер билета
    :param flight_id: Номер рейса
    :param db: Сессия для работы с бд
    :return: Сформированый ответ в формате JSON
    """
    if not valid_ticket_no(ticket_no):
        raise HTTPException(status_code=422, detail="ticket_no must be 13 characters")
    if not await TicketFlightController(db).delete_ticket_flight(ticket_no, flight_id):
        raise HTTPException(status_code=404, detail="Ticket not found")


@router.put("/{ticket_no}/{flight_id}")
async def put(data: TicketFlightUpdate, ticket_no: str, flight_id: int, db: Session = Depends(get_db)):
    """
    Вьюха для обновления связи билета и перелёта

    :param data: Данные требуемые для работы контроллера
    :param ticket_no: Номер билета
    :param flight_id: Номер рейса
    :param db: Сессия для работы с бд
    :return: Сформированый ответ в формате JSON
    """
    if not valid_ticket_no(ticket_no):
        raise HTTPException(status_code=422, detail="ticket_no must be 13 characters")
    if not await TicketFlightController(db).put_ticket_flight(ticket_no, flight_id, data):
        raise HTTPException(status_code=404, detail="Ticket not found")

