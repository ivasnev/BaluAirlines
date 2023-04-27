from MyAviasales.controllers.base_controller import BaseController
from MyAviasales.views.ticket_flights.schema import *
from MyAviasales.models import TicketFlight
from typing import Optional, List


class TicketFlightController(BaseController):
    async def get_all_ticket_flights(self, page: int) -> Optional[List[TicketFlightBase]]:
        """
        Метод для получения связей между билетами и перелётами

        :param page: Номер страницы
        :return: Страница из 50 записей связей между билетами и перелётами
        """
        page_size = 50
        ticket_flight_query = self.session.query(TicketFlight
                                                 ).limit(page_size).offset(page * page_size)
        ticket_flights = [TicketFlightBase.from_orm(x) for x in ticket_flight_query if x is not None]
        return ticket_flights

    async def get_single_ticket_flight(self, ticket_no: str, flight_id: int) -> Optional[TicketFlightBase]:
        """
        Метод для получения связи между билетами и перелётами

        :param ticket_no: Номер билета
        :param flight_id: Номер перелёта
        :return: Связь между билетами и перелётами
        """
        ticket_flight = self.session.query(TicketFlight
                                           ).filter_by(ticket_no=ticket_no,
                                                       flight_id=flight_id
                                                       ).one_or_none()
        if ticket_flight:
            return TicketFlightBase.from_orm(ticket_flight)
        return ticket_flight

    async def post_ticket_flight(self, data: TicketFlightBase) -> bool:
        """
        Метод для создания связи между билетами и перелётами

        :param data: Данные для создания записи
        :return: Статус создания(Создан/ не создан)
        """
        ticket_flight = self.session.query(TicketFlight).filter(
            TicketFlight.ticket_no == data.ticket_no,
            TicketFlight.flight_id == data.flight_id
        ).one_or_none()
        if ticket_flight:
            return False
        self.session.add(TicketFlight(ticket_no=data.ticket_no,
                                      flight_id=data.flight_id,
                                      fare_conditions=data.fare_conditions,
                                      amount=data.amount
                                      ))
        self.session.flush()
        self.session.commit()
        return True

    async def delete_ticket_flight(self, ticket_no: str, flight_id: int) -> bool:
        """
        Метод для удаления связи между билетами и перелётами

        :param ticket_no: Номер билета
        :param flight_id: Номер перелёта
        :return: Статус удаления(Удалён/ не удалён)
        """
        ticket_flight = self.session.query(TicketFlight).filter(
            TicketFlight.ticket_no == ticket_no,
            TicketFlight.flight_id == flight_id
        ).one_or_none()
        if ticket_flight is None:
            return False
        self.session.delete(self.session.query(TicketFlight).get({'ticket_no': ticket_no, 'flight_id': flight_id}))
        self.session.commit()
        return True

    async def put_ticket_flight(self, ticket_no: str, flight_id: int, data: TicketFlightUpdate) -> bool:
        """
        Метод для обновления связи между билетами и перелётами

        :param ticket_no: Номер билета
        :param flight_id: Номер перелёта
        :param data: Данные для обновления записи
        :return: Статус обновления(Обновлён/ не обновлён)
        """
        return self.base_put(TicketFlight, {'ticket_no': ticket_no, 'flight_id': flight_id}, data)
