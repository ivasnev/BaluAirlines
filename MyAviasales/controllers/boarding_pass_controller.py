from sqlalchemy import and_

from MyAviasales.controllers.base_controller import BaseController
from MyAviasales.models import TicketFlight, BoardingPass
from typing import List
from MyAviasales.views.boarding_passes.schema import *
from sqlalchemy import func


class BoardingPassController(BaseController):
    """
    Контроллер для работы с бд посадочных талонов
    """
    async def get_all_boarding_passes(self, page=0) -> Optional[List[BoardingPassBase]]:
        """
        Метод для получения всех посадочных талонов

        :param page: Номер страницы результатов
        :return: 50 посадочных талонов
        """
        page_size = 50
        boarding_passes = self.session.query(
            BoardingPass
        ).limit(page_size).offset(
            page * page_size)
        return [BoardingPassBase.from_orm(row) for row in boarding_passes]

    async def get_single_boarding_pass(self, ticket_no: str, flight_id: int) -> Optional[BoardingPassBase]:
        """
        Метод для получения посадочного талона по номеру билета и номеру рейса

        :param ticket_no: Номер билета
        :param flight_id: Номер рейса
        :return: Посадочный талон
        """
        boarding_pass = self.session.query(
            BoardingPass
        ).filter(and_(BoardingPass.ticket_no == ticket_no,
                      BoardingPass.flight_id == flight_id, )
                 ).one_or_none()
        if boarding_pass:
            return BoardingPassBase.from_orm(boarding_pass)
        return boarding_pass

    async def seat_no_available(self, flight_id: int, seat_no: str):
        """
        Метод для проверки доступности места на самолёте

        :param flight_id: Номер рейса
        :param seat_no: Номер места в самолёте
        :return: Доступно/не доступно
        """
        if self.session.query(BoardingPass).filter(
                and_(BoardingPass.seat_no == seat_no,
                     BoardingPass.flight_id == flight_id)).one_or_none():
            return False
        return True

    async def ticket_flight_exist(self, flight_id: int, ticket_no: str):
        """
        Метод для проверки существования связи между перелётом и билетом

        :param flight_id: Номер рейса
        :param ticket_no: Номер билета
        :return: Существует/не существует
        """
        if self.session.query(TicketFlight).filter(
                and_(TicketFlight.ticket_no == ticket_no,
                     TicketFlight.flight_id == flight_id)).one_or_none():
            return True
        return False

    async def post_boarding_pass(self, data: BoardingPassPost) -> bool:
        """
        Метод добавления посадочного талона на рейс

        :param data: Данные для создания посадочного
        :return: Статус создания(Создан/ не создан)
        """
        if self.session.query(BoardingPass.seat_no).filter(
                and_(BoardingPass.ticket_no == data.ticket_no,
                     BoardingPass.flight_id == data.flight_id)).one_or_none():
            return False

        last_id = self.session.query(
            func.max(BoardingPass.boarding_no)
        ).filter(BoardingPass.flight_id == data.flight_id
                 ).one_or_none()
        if last_id[0] is None:
            last_id = 1
        else:
            last_id = last_id[0]+1
        self.session.add(BoardingPass(
            ticket_no=data.ticket_no,
            flight_id=data.flight_id,
            boarding_no=last_id,
            seat_no=data.seat_no,
        ))
        self.session.commit()
        return True

    async def delete_boarding_pass(self, ticket_no: str, flight_id: int) -> bool:
        """
        Метод для удаления посадочного талона

        :param ticket_no: Номер билета
        :param flight_id: Номер рейса
        :return: Статус удаления(Удалён/ не удалён)
        """
        boarding_pass = self.session.query(
            BoardingPass
        ).filter(and_(BoardingPass.ticket_no == ticket_no,
                      BoardingPass.flight_id == flight_id)
                 ).one_or_none()
        if boarding_pass is None:
            return False
        self.session.delete(boarding_pass)
        self.session.commit()
        return True

    async def put_boarding_pass(self, ticket_no: str, flight_id: int, data: BoardingPassUpdate) -> bool:
        """
        Метод для обновления данных об посадочном талоне

        :param ticket_no: Номер билета
        :param flight_id: Номер рейса
        :param data: Данные для обновления
        :return: Статус обновления(Обновлён/ не обновлён)
        """
        return self.base_put(BoardingPass, {'ticket_no': ticket_no, 'flight_id': flight_id}, data)
