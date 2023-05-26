# coding: utf-8
from MyAviasales.controllers.admin_controller import AdminController
from fastapi import APIRouter, Depends, HTTPException
from MyAviasales.DataBase.database import get_db
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/clear_db")
async def clear_db(password: str = "IAMPUSSYBOY", db: Session = Depends(get_db)) -> str:
    """
    Очистка бд

    :param password: пароль
    :param db: Сессия для работы с бд
    :return:
    """
    return await AdminController(db).clear_all_tables(password)


@router.get("/update_date")
async def update_date(date: datetime = datetime.now(), db: Session = Depends(get_db)) -> str:
    """
    Обновление даты в бд

    :param date: Новая дата
    :param db: Сессия для работы с бд
    :return:
    """
    return await AdminController(db).update_date(new_date_time=date)
