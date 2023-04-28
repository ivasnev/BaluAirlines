# coding: utf-8
from MyAviasales.controllers.flights_controller import FlightController
from fastapi import APIRouter, Depends, HTTPException
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
    """
    Валидатор номера рейса

    :param code: Номер рейса
    :return: Валидный/ не валидный
    """
    return len(code) == 6


def valid_fare_conditions(v) -> bool:
    """
    Валидатор класса перелёта

    :param v: Класс перелёта
    :return: Валидный/ не валидный
    """
    enum = ['Economy', 'Comfort', 'Business']
    return v in enum


def valid_airport_code(v) -> bool:
    """
    Валидатор кода аэропорта

    :param v: Код аэропорта
    :return: Валидный/ не валидный
    """
    return len(v) == 3


@router.get("/all")
async def multiple_get(page: Optional[int] = 0,
                       db: Session = Depends(get_db)
                       ) -> Optional[List[FlightBase]]:
    """
    Вьюха для получения всех перелётов

    :param page: Номер страницы
    :param db: Сессия для работы с бд
    :return: Сформированый ответ в формате JSON
    """
    res = await FlightController(db).get_all_flights(page=page)
    if len(res) == 0:
        raise HTTPException(status_code=404, detail="Flight not found")
    return res


@router.get("/table/{departure_airport}")
async def table_get(departure_airport: str,
                    departure_date: datetime = datetime.now(),
                    db: Session = Depends(get_db)
                    ) -> Optional[List[FlightBase]]:
    """
    Вьюха для получения табло рейсов

    :param departure_airport: Аэропорт вылета
    :param departure_date: Дата вылета
    :param db: Сессия для работы с бд
    :return: Сформированый ответ в формате JSON
    """
    if not valid_airport_code(departure_airport):
        raise HTTPException(status_code=422, detail='departure_airport code must be 3 characters')
    res = await FlightController(db).get_all_for_a_day(departure_date=departure_date,
                                                       departure_airport=departure_airport)
    if len(res) == 0:
        raise HTTPException(status_code=404, detail="Flights not found")
    return res


@router.get("/best_price/")
async def get_best_price(departure_airport: Optional[str] = 'VKO',
                         arrival_airport: Optional[str] = 'VVO',
                         max_transits: Optional[int] = 2,
                         departure_date: Optional[datetime] = datetime.now(),
                         fare_condition: Optional[str] = 'Economy',
                         num_of_passengers: Optional[int] = 1,
                         db: Session = Depends(get_db)
                         ) -> List[Optional[float]]:
    """
    Вьюха для лучших цен на неделю

    :param departure_airport: Аэропорт вылета
    :param arrival_airport: Аэропорт прилёта
    :param max_transits: Колличество пересадок (максимум)
    :param departure_date: Дата вылета
    :param fare_condition: Класс перелёта
    :param num_of_passengers: Колличество пассажиров 
    :param db: Сессия для работы с бд
    :return: Сформированый ответ в формате JSON
    """
    if not valid_fare_conditions(fare_condition):
        raise HTTPException(status_code=422, detail='must be Economy, Comfort or Business')
    if not valid_airport_code(departure_airport):
        raise HTTPException(status_code=422, detail='departure_airport code must be 3 characters')
    if not valid_airport_code(arrival_airport):
        raise HTTPException(status_code=422, detail='arrival_airport code must be 3 characters')
    res = await FlightController(db).get_best_price_for_a_week(
        departure_date=departure_date,
        departure_airport=departure_airport,
        arrival_airport=arrival_airport,
        max_transits=max_transits,
        fare_condition=fare_condition,
        num_of_passengers=num_of_passengers
    )
    if len(res) == 0:
        raise HTTPException(status_code=404, detail="Prices flights not found")
    return res


@router.get("/")
async def filter_get(
        departure_airport: Optional[str] = 'VKO',
        arrival_airport: Optional[str] = 'VVO',
        max_transits: Optional[int] = 2,
        departure_date: Optional[datetime] = datetime.now(),
        fare_condition: Optional[str] = 'Economy',
        num_of_passengers: Optional[int] = 1,
        db: Session = Depends(get_db),
) -> List[Optional[FlightPath]]:
    """
    Вьюха для получения рейсов по фильтрам

    :param departure_airport: Аэропорт вылета
    :param arrival_airport: Аэропорт прилёта
    :param max_transits: Колличество пересадок (максимум)
    :param departure_date: Дата вылета
    :param fare_condition: Класс перелёта
    :param num_of_passengers: Колличество пассажиров
    :param db: Сессия для работы с бд
    :return: Сформированый ответ в формате JSON
    """
    if not valid_fare_conditions(fare_condition):
        raise HTTPException(status_code=422, detail='must be Economy, Comfort or Business')
    if not valid_airport_code(departure_airport):
        raise HTTPException(status_code=422, detail='departure_airport code must be 3 characters')
    if not valid_airport_code(arrival_airport):
        raise HTTPException(status_code=422, detail='arrival_airport code must be 3 characters')
    if departure_airport == arrival_airport:
        raise HTTPException(status_code=422, detail='departure airport cant be arrival airport')
    res = await FlightController(db).get_flights_from_to_(
        departure_date=departure_date,
        departure_airport=departure_airport,
        arrival_airport=arrival_airport,
        max_transits=max_transits,
        fare_condition=fare_condition,
        num_of_passengers=num_of_passengers
    )
    if len(res) == 0:
        raise HTTPException(status_code=404, detail="Flight not found")
    return res


@router.get("/no/{flight_no}")
async def single_get(flight_no: str,
                     date: Optional[datetime] = datetime.now(),
                     db: Session = Depends(get_db)) -> FlightBase:
    """
    Вьюха для получения одного рейса по номеру рейса и даты

    :param flight_no: Номер рейса
    :param date: Дата вылета
    :param db: Сессия для работы с бд
    :return: Сформированый ответ в формате JSON
    """
    if not valid_flight_no(flight_no):
        raise HTTPException(status_code=422, detail="flight_no must be 6 characters")
    res = await FlightController(db).get_single_flight_by_no_and_date(flight_no, date)
    if res is None:
        raise HTTPException(status_code=404, detail="Flight not found")
    return res


@router.get("/id/{flight_id}")
async def single_get(flight_id: int, db: Session = Depends(get_db)) -> FlightBase:
    """
    Вьюха для получения одного рейса по ID в бд

    :param flight_id: Номер рейса
    :param db: Сессия для работы с бд
    :return: Сформированый ответ в формате JSON
    """
    res = await FlightController(db).get_single_flight_by_id(flight_id)
    if res is None:
        raise HTTPException(status_code=404, detail="Flight not found")
    return res


@router.get("/path/{departure_airport}/{arrival_airport}")
async def single_get(departure_airport: str,
                     arrival_airport: str,
                     departure_date: Optional[datetime] = datetime.now(),
                     db: Session = Depends(get_db)) -> FlightBase:
    """
    Вьюха для рейса по аэропорту вылета и прилёта

    :param departure_airport: Аэропорт вылета
    :param arrival_airport: Аэропорт прилёта
    :param departure_date: Дата вылета
    :param db: Сессия для работы с бд
    :return: Сформированый ответ в формате JSON
    """
    res = await FlightController(db).get_single_flight_from_to(
        departure_airport, arrival_airport, departure_date)
    if res is None:
        raise HTTPException(status_code=404, detail="Flight not found")
    return res


@router.post("/")
async def post(data: FlightBase, db: Session = Depends(get_db)) -> FlightBase:
    """
    Вьюха для создания рейса

    :param data: Данные требуемые для работы контроллера
    :param db: Сессия для работы с бд
    :return: Сформированый ответ в формате JSON
    """
    return await FlightController(db).post_flight(data)


@router.delete("/{flight_id}")
async def delete(flight_id: int, db: Session = Depends(get_db)):
    """
    Вьюха для удаления рейса

    :param flight_id: Номер рейса
    :param db: Сессия для работы с бд
    :return: Сформированый ответ в формате JSON
    """
    if not await FlightController(db).delete_flight(flight_id):
        raise HTTPException(status_code=404, detail="Flight not found")


@router.put("/{flight_id}")
async def put(data: FlightUpdate, flight_id: int, db: Session = Depends(get_db)):
    """
    Вьюха для обновления рейса

    :param data: Данные требуемые для работы контроллера
    :param flight_id: Номер рейса
    :param db: Сессия для работы с бд
    :return: Сформированый ответ в формате JSON
    """
    if not await FlightController(db).put_flight(flight_id, data):
        raise HTTPException(status_code=404, detail="Flight not found")
