# coding: utf-8
from MyAviasales.controllers.ticket_controller import TicketController
from fastapi import APIRouter, Depends, HTTPException
from MyAviasales.DataBase.database import get_db
from .schema import TicketBase, TicketUpdate, TicketPost
from sqlalchemy.orm import Session
from typing import List, Optional

router = APIRouter(
    prefix="/tickets",
    tags=["tickets"],
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
                       ) -> Optional[List[TicketBase]]:
    """
    Вьюха для получения всех билетов

    :param db: Сессия для работы с бд
    :param page: Номер страницы
    :return: Сформированый ответ в формате JSON
    """
    res = await TicketController(db).get_all_tickets(page=page)
    if len(res) == 0:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return res


@router.get("/{ticket_no}")
async def single_get(ticket_no: str, db: Session = Depends(get_db)) -> TicketBase:
    """
    Вьюха для получения билета по номеру

    :param ticket_no: Номер билета
    :param db: Сессия для работы с бд
    :return: Сформированый ответ в формате JSON
    """
    if not valid_ticket_no(ticket_no):
        raise HTTPException(status_code=422, detail="ticket_no must be 13 characters")
    res = await TicketController(db).get_single_ticket(ticket_no)
    if res is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return res


@router.post("/")
async def post(data: TicketPost, db: Session = Depends(get_db)) -> bool:
    """
    Вьюха для создания билета

    :param data: Данные требуемые для работы контроллера
    :param db: Сессия для работы с бд
    :return: Сформированый ответ в формате JSON
    """
    return await TicketController(db).post_ticket(data)


@router.delete("/{ticket_no}")
async def delete(ticket_no: str, db: Session = Depends(get_db)):
    """
    Вьюха для удаления билета

    :param ticket_no: Номер билета
    :param db: Сессия для работы с бд
    :return: Сформированый ответ в формате JSON
    """
    if not valid_ticket_no(ticket_no):
        raise HTTPException(status_code=422, detail="ticket_no must be 13 characters")
    if not await TicketController(db).delete_ticket(ticket_no):
        raise HTTPException(status_code=404, detail="Ticket not found")


@router.put("/{ticket_no}")
async def put(data: TicketUpdate, ticket_no: str, db: Session = Depends(get_db)):
    """
    Вьюха для обновления билета

    :param data: Данные требуемые для работы контроллера
    :param ticket_no: Номер билета
    :param db: Сессия для работы с бд
    :return: Сформированый ответ в формате JSON
    """
    if not valid_ticket_no(ticket_no):
        raise HTTPException(status_code=422, detail="ticket_no must be 13 characters")
    if not await TicketController(db).put_ticket(ticket_no, data):
        raise HTTPException(status_code=404, detail="Ticket not found")
