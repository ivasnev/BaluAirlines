from MyAviasales.models import *
from MyAviasales.controllers.base_controller import BaseController
from MyAviasales.views.seats.schema import *
from typing import List, Optional
from datetime import datetime, timedelta
import pytz


class AdminController(BaseController):
    """
    Контроллер для админ функций
    """

    async def update_date(self, new_date_time: datetime) -> str:
        """
        Обновление даты в бд на текущую

        :param new_date_time:
        :return:
        """
        base_flight_id = 29080
        cur_base_date = self.session.query(Flight.actual_departure).filter(Flight.flight_id == base_flight_id).one()[0]
        new_date_time = pytz.utc.localize(new_date_time)
        delta = new_date_time - cur_base_date - timedelta(hours=3)
        if abs(delta) < timedelta(days=1):
            return "Обновление даты чаще чем раз в день запрещено"
        all_records = self.session.query(Flight).all()
        for rec in all_records:
            rec.scheduled_arrival += delta
            rec.scheduled_departure += delta
            if rec.actual_arrival:
                rec.actual_arrival += delta
            if rec.actual_departure:
                rec.actual_departure += delta

        self.session.commit()
        return "Дело сделано"

    async def clear_all_tables(self, password) -> str:
        if password != "IAMLORDOFNOWHERE":
            return "Вы кто такие я вас не звал идите н***й"
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
        self.session.execute("""TRUNCATE TABLE """ + ", ".join(tables_to_clear))
        self.session.commit()
        return "Ну и зачем ты это сделал"
