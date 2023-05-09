# coding: utf-8
from MyAviasales.controllers.bookings_controller import BookingController
from fastapi import APIRouter, Depends, HTTPException
from MyAviasales.DataBase.database import get_db
from .schema import *
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(
    prefix="/bookings",
    tags=["bookings"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


def valid_book_ref(code) -> bool:
    """
    Валидатор для номера бронирования

    :param code: Номер бронирования
    :return: Валидный/ не валидный
    """
    return len(code) < 7


@router.get("/")
async def multiple_get(page: Optional[int] = 0,
                       db: Session = Depends(get_db)
                       ) -> Optional[List[BookingResponse]]:
    """
    Вьюха для списка бронирований
    
    :param page: Номер страницы
    :param db: Сессия для работы с бд
    :return: Сформированый ответ в формате JSON
    """
    res = await BookingController(db).get_all_bookings(page=page)
    if len(res) == 0:
        raise HTTPException(status_code=404, detail="Booking not found")
    return res


@router.get("/{book_ref}")
async def single_get(book_ref: str, db: Session = Depends(get_db)) -> BookingResponse:
    """
    Вьюха для одного бронирования
    
    :param book_ref: Номер бронирования
    :param db: Сессия для работы с бд
    :return: Сформированый ответ в формате JSON
    """
    if not valid_book_ref(book_ref):
        raise HTTPException(status_code=422, detail="book_ref must be less than 7 characters")
    res = await BookingController(db).get_single_booking(book_ref)
    if res is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return res


@router.post("/", responses={404: {"description": "Booking already exist"}})
async def post(data: BookingPostRequest, db: Session = Depends(get_db)) -> Optional[BookingResponse]:
    """
    Вьюха для создания бронирования
    
    :param data: Данные требуемые для работы контроллера
    :param db: Сессия для работы с бд
    :return: Сформированый ответ в формате JSON
    """
    res = await BookingController(db).post_booking(data)
    if not res:
        raise HTTPException(status_code=404, detail="Booking already exist")
    return res


@router.delete("/{book_ref}")
async def delete(book_ref: str, db: Session = Depends(get_db)):
    """
    Вьюха для удаления бронирования
    
    :param book_ref: Номер бронирования
    :param db: Сессия для работы с бд
    :return: Сформированый ответ в формате JSON
    """
    if not await BookingController(db).delete_booking(book_ref):
        raise HTTPException(status_code=404, detail="Booking not found")


@router.put("/{book_ref}")
async def put(data: BookingUpdate, book_ref: str, db: Session = Depends(get_db)):
    """
    Вьюха для обновления бронирования
    
    :param data: Данные требуемые для работы контроллера
    :param book_ref: Номер бронирования
    :param db: Сессия для работы с бд
    :return: Сформированый ответ в формате JSON
    """
    if not await BookingController(db).put_booking(book_ref, data):
        raise HTTPException(status_code=404, detail="Booking not found")
