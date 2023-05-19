from fastapi.testclient import TestClient

from MyAviasales.main import app
from MyAviasales.DataBase.database import get_db
from tests.database import get_db_test, SessionLocal

from tests.test_aircraft import TestAircraft
from tests.test_airport import TestAirport
from tests.test_seats import TestSeats
from tests.test_flights import TestFlights

app.dependency_overrides[get_db] = get_db_test
client = TestClient(app)
class_inst = {
    "aircraft": TestAircraft(client, "/aircraft/"),
    "airport": TestAirport(client, "/airports/"),
    "seats": TestSeats(client, "/seats/"),
    "flights": TestFlights(client, "/flights/")
}
tables_to_clear = [
    "bookings.boarding_passes",
    "bookings.ticket_flights",
    "bookings.tickets",
    "bookings.bookings",
    "bookings.flights",
    "bookings.airports_data",
    "bookings.aircrafts_data",
    "bookings.seats"
]


def clear_all_tables():
    db = SessionLocal()
    try:
        db.execute("""TRUNCATE TABLE """ + ", ".join(tables_to_clear))
        db.commit()
    finally:
        db.close()


def test_base_func(need_clear: bool = True):
    """
    Тест базового функционала

    :param need_clear: Требуется ли очистка бд
    :return: Ничего
    """
    if need_clear:
        clear_all_tables()
    for inst in class_inst.values():
        inst.test_base_func()


def test_base_user_story(need_clear: bool = True):
    """
    Тест базового функционала

    :param need_clear: Требуется ли очистка бд
    :return: Ничего
    """
    if need_clear:
        clear_all_tables()
    aircraft_1 = {
        "aircraft_code": "Te1",
        "model": {"en": "Test", "ru": "Test"},
        "range": 12000
    }
    aircraft_2 = {
        "aircraft_code": "Te2",
        "model": {"en": "Test", "ru": "Test"},
        "range": 10000
    }
    airport_1 = {
        "airport_code": "YKS",
        "airport_name": {
            "ru": "Якутск",
            "en": "Yakutsk Airport"
        },
        "city": {
            "ru": "Якутск",
            "en": "Yakutsk"
        },
        "coordinates": "(129.77099609375,62.093299865722656)",
        "timezone": "Asia/Yakutsk"
    }
    airport_2 = {
        "airport_code": "MJZ",
        "airport_name": {
            "ru": "Мирный",
            "en": "Mirny Airport"
        },
        "city": {
            "ru": "Мирный",
            "en": "Mirnyj"
        },
        "coordinates": "(114.03900146484375,62.534698486328125)",
        "timezone": "Asia/Yakutsk"
    }
    airport_3 = {
        "airport_code": "SVO",
        "airport_name": {
            "ru": "Шереметьево",
            "en": "Sheremetyevo International Airport"
        },
        "city": {
            "ru": "Москва",
            "en": "Moscow"
        },
        "coordinates": "(37.4146,55.972599)",
        "timezone": "Europe/Moscow"
    }
    class_inst["aircraft"].test_post(aircraft_1)
    class_inst["aircraft"].test_post(aircraft_2)
    class_inst["airport"].test_post(airport_1)
    class_inst["airport"].test_post(airport_2)
    class_inst["airport"].test_post(airport_3)
    for i in range(1, 5):
        for letter in "ABCD":
            class_inst["seats"].test_post(
                data_input={
                    "aircraft_code": aircraft_1["aircraft_code"],
                    "seat_no": str(i) + letter,
                    "fare_conditions": "Business"
                }
            )
            class_inst["seats"].test_post(
                data_input={
                    "aircraft_code": aircraft_2["aircraft_code"],
                    "seat_no": str(i) + letter,
                    "fare_conditions": "Business"
                }
            )
    for i in range(5, 25):
        for letter in "ABCDEF":
            class_inst["seats"].test_post(
                data_input={
                    "aircraft_code": aircraft_1["aircraft_code"],
                    "seat_no": str(i) + letter,
                    "fare_conditions": "Economy"
                }
            )
            class_inst["seats"].test_post(
                data_input={
                    "aircraft_code": aircraft_2["aircraft_code"],
                    "seat_no": str(i) + letter,
                    "fare_conditions": "Economy"
                }
            )
    flight_1 = {
            "flight_no": "TEST01",
            "scheduled_departure": "2023-04-29T19:05:00+03:00",
            "scheduled_arrival": "2023-04-29T20:00:00+03:00",
            "departure_airport": airport_1["airport_code"],
            "arrival_airport": airport_2["airport_code"],
            "status": "Scheduled",
            "aircraft_code": aircraft_1["aircraft_code"],
            "actual_departure": None,
            "actual_arrival": None
        }
    flight_2 = {
        "flight_no": "TEST02",
        "scheduled_departure": "2023-04-29T20:00:00+03:00",
        "scheduled_arrival": "2023-04-29T23:00:00+03:00",
        "departure_airport": airport_2["airport_code"],
        "arrival_airport": airport_3["airport_code"],
        "status": "Scheduled",
        "aircraft_code": aircraft_2["aircraft_code"],
        "actual_departure": None,
        "actual_arrival": None
    }
    class_inst["flights"].test_post(flight_1)


if __name__ == "__main__":
    test_base_func()
    test_base_user_story()
