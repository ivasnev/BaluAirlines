from fastapi.testclient import TestClient

from MyAviasales.main import app
from tests.test_aircraft import TestAircraft
from MyAviasales.DataBase.database import get_db
from tests.database import get_db_test, SessionLocal
from MyAviasales.models import *

app.dependency_overrides[get_db] = get_db_test
client = TestClient(app)
class_inst = {
    "aircraft": TestAircraft(client)
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


def test_base_func():
    clear_all_tables()
    for inst in class_inst.values():
        inst.test_base_func()
