from MyAviasales.controllers.base_controller import BaseController
from MyAviasales.models import Flight, AirportsDatum
from collections import deque
from typing import Optional, List
from MyAviasales.views.flights.schema import FlightBase, FlightUpdate, FlightPath, FlightPathBase
from datetime import datetime, timedelta
from sqlalchemy import and_


class FlightController(BaseController):
    """
    Контроллер для работы с бд перелётов
    """

    async def get_single_flight_by_id(self, key: int) -> Optional[FlightBase]:
        """
        Метод для получения перелёта по id записи в бд

        :param key: Id записи бд
        :return: Перелёт
        """
        flight = self.session.query(Flight.flight_id,
                                    Flight.flight_no,
                                    Flight.scheduled_departure,
                                    Flight.scheduled_arrival,
                                    Flight.departure_airport,
                                    Flight.arrival_airport,
                                    Flight.status,
                                    Flight.aircraft_code,
                                    Flight.actual_departure,
                                    Flight.actual_arrival
                                    ).filter_by(
            flight_id=key).first()
        if flight:
            return FlightBase.from_orm(flight)
        else:
            return None

    async def get_single_flight_by_no_and_date(self, flight_no,
                                               departure_date) -> Optional[FlightBase]:
        """
        Метод для получения перелёта по номеру рейса и дате вылета

        :param flight_no: Номер рейса
        :param departure_date: Дата вылета
        :return: Перелёт
        """
        flight = self.session.query(Flight.flight_id,
                                    Flight.flight_no,
                                    Flight.scheduled_departure,
                                    Flight.scheduled_arrival,
                                    Flight.departure_airport,
                                    Flight.arrival_airport,
                                    Flight.status,
                                    Flight.aircraft_code,
                                    Flight.actual_departure,
                                    Flight.actual_arrival
                                    ).filter(and_(Flight.flight_no == flight_no,
                                                  Flight.scheduled_departure >= departure_date
                                                  )).first()
        if flight:
            return FlightBase.from_orm(flight)
        else:
            return None

    async def get_single_flight_from_to(self, departure_airport,
                                        arrival_airport, departure_date) -> Optional[FlightBase]:
        """
        Получение перелёта по аэропорту вылета и прилёта и дате вылета

        :param departure_airport: Аэропорт вылета
        :param arrival_airport: Аэропорт прилёта
        :param departure_date: Дата вылета
        :return: Перелёт
        """
        flight = self.session.query(Flight.flight_id,
                                    Flight.flight_no,
                                    Flight.scheduled_departure,
                                    Flight.scheduled_arrival,
                                    Flight.departure_airport,
                                    Flight.arrival_airport,
                                    Flight.status,
                                    Flight.aircraft_code,
                                    Flight.actual_departure,
                                    Flight.actual_arrival
                                    ).filter(and_(Flight.departure_airport == departure_airport,
                                                  Flight.arrival_airport == arrival_airport,
                                                  Flight.scheduled_departure >= departure_date
                                                  )).first()
        if flight:
            return FlightBase.from_orm(flight)
        else:
            return None

    async def get_all_for_a_day(self, departure_date: datetime, departure_airport: str) -> Optional[List[FlightBase]]:
        """
        Метод для получения всех вылетов из аэропорта на определённую дату

        :param departure_date: Дата вылета
        :param departure_airport: Аэропорт вылета
        :return: Список перелётов
        """
        flight_query = self.session.query(Flight.flight_id,
                                          Flight.scheduled_departure,
                                          Flight.scheduled_arrival,
                                          Flight.flight_no,
                                          Flight.status,
                                          Flight.departure_airport,
                                          Flight.arrival_airport,
                                          Flight.aircraft_code
                                          ).filter(
            Flight.scheduled_departure > departure_date,
            Flight.scheduled_departure < departure_date + timedelta(days=1),
            Flight.departure_airport == departure_airport
        ).order_by(Flight.scheduled_departure).all()
        return [FlightBase.from_orm(x) for x in flight_query if x is not None]

    @staticmethod
    def bfs_paths_with_city(graph: dict, start: str, goal: str, airport_to_city: dict, max_transits: int = 2):
        """
        Генератор для обхода графа методом BFS

        :param graph: Граф сохранённый в формате связанного списка
        :param start: Стартовая точка
        :param goal: Финальная точка
        :param airport_to_city: Словарь который мапит аэропорты с городами
        :param max_transits: Максимальное колличество пересадок
        :return: Генератор
        """
        queue = deque([(start, [start], [airport_to_city[start]])])
        while queue:
            (vertex, path, cites) = queue.pop()
            for _next in set(graph[vertex]) - set(path):
                if len(path) > max_transits:
                    continue
                if airport_to_city[_next] in cites:
                    continue
                if _next == goal:
                    yield path + [_next]
                else:
                    queue.appendleft((_next, path + [_next], cites + [airport_to_city[_next]]))

    async def get_all_flights(self, page: int) -> Optional[List[FlightBase]]:
        """
        Метод для получения страницы из 50 записей перелётов

        :param page: Номер страницы
        :return: 50 записей перелётов
        """
        page_size = 50
        flight_query = self.session.query(Flight.flight_id,
                                          Flight.flight_no,
                                          Flight.scheduled_departure,
                                          Flight.scheduled_arrival,
                                          Flight.departure_airport,
                                          Flight.arrival_airport,
                                          Flight.status,
                                          Flight.aircraft_code,
                                          Flight.actual_departure,
                                          Flight.actual_arrival
                                          ).limit(page_size).offset(page * page_size)
        flights = [FlightBase.from_orm(x) for x in flight_query if x is not None]
        return flights

    async def get_routes_from_to(self, departure_airport: str,
                                 arrival_airport: str,
                                 max_transits: int) -> list:
        """
        Метод для получения всех перелётов из точки А в точку Б

        :param departure_airport: Аэропорт вылета
        :param arrival_airport: Аэропорт прилёта
        :param max_transits: Колличество пересадок
        :return: Список перелётов
        """
        airports = self.session.query(AirportsDatum.airport_code, AirportsDatum.city).all()
        edges = self.session.query(Flight.departure_airport, Flight.arrival_airport).distinct().all()
        nodes = [x[0] for x in airports]
        airports = {x[0]: x[1]['en'] for x in airports}
        listed_graph = {key: [] for key in nodes}
        for edge in edges:
            listed_graph[edge[0]].append(edge[1])
        return list(self.bfs_paths_with_city(listed_graph, departure_airport, arrival_airport, airports, max_transits))

    async def get_flights_from_to_(self, departure_date: datetime,
                                   departure_airport: str,
                                   arrival_airport: str,
                                   max_transits: int,
                                   fare_condition: str,
                                   num_of_passengers: int) -> List[Optional[FlightPath]]:
        """
        Метод для получения всех рейсов из точки А в точку Б

        :param departure_date: Дата вылета
        :param departure_airport: Аэропорт вылета
        :param arrival_airport: Аэропорт прилёта
        :param max_transits: Колличество пересадок
        :param fare_condition: Класс перелёта
        :param num_of_passengers: Колличество пассажиров
        :return: Список возможных перелётов с ценами за определённое колличество людей
        """
        routes = await self.get_routes_from_to(departure_airport, arrival_airport, max_transits)
        res = []

        for route in routes:
            flights = []
            dist = 0.0
            prev = route[0]
            st_date = None
            for key in route[1:]:
                flight = self.session.query(Flight.flight_id,
                                            Flight.scheduled_departure,
                                            Flight.scheduled_arrival,
                                            Flight.flight_no,
                                            Flight.status,
                                            Flight.departure_airport,
                                            Flight.arrival_airport,
                                            Flight.aircraft_code
                                            ).filter(
                    Flight.scheduled_departure > departure_date, Flight.departure_airport == prev,
                    Flight.arrival_airport == key,
                    Flight.status == "Scheduled"
                ).order_by(Flight.scheduled_departure).first()
                prev = key
                if flight is None:
                    break
                if st_date is None:
                    st_date = flight.scheduled_departure
                departure_airport = self.session.query(AirportsDatum.coordinates).filter(
                    AirportsDatum.airport_code == flight.departure_airport).first()[0]
                arrival_airport = self.session.query(AirportsDatum.coordinates).filter(
                    AirportsDatum.airport_code == flight.arrival_airport).first()[0]

                dist += self.get_dist(eval(departure_airport), eval(arrival_airport))
                departure_date = flight['scheduled_arrival']
                flights.append(FlightPathBase.from_orm(flight))
            else:
                res.append(FlightPath(cost=self.generate_cost(fare_condition, dist, st_date.date()) * num_of_passengers,
                                      fare_condition=fare_condition,
                                      num_of_passengers=num_of_passengers,
                                      time=str(departure_date - st_date),
                                      flights=flights))
        return res

    async def get_best_price_for_a_week(self, departure_date: datetime,
                                        departure_airport: str,
                                        arrival_airport: str,
                                        max_transits: int,
                                        fare_condition: str,
                                        num_of_passengers: int) -> Optional[List[float]]:
        """
        Метод для получения цен на неделю от даты для перелёта из точки А в точку Б

        :param departure_date: Дата вылета
        :param departure_airport: Аэропорт вылета
        :param arrival_airport: Аэропорт прилёта
        :param max_transits: Колличество пересадок
        :param fare_condition: Класс перелёта
        :param num_of_passengers: Колличество пассажиров
        :return: Список лучших цен на неделю
        """
        routes = await self.get_routes_from_to(departure_airport, arrival_airport, max_transits)
        cur_date = departure_date.date() - timedelta(days=3)
        costs_for_week = []
        for i in range(7):
            res = []
            for route in routes:
                flights = []
                dist = 0.0
                prev = route[0]
                departure_date = cur_date
                st_date = None
                for key in route[1:]:
                    flight = self.session.query(Flight.flight_id,
                                                Flight.scheduled_departure,
                                                Flight.scheduled_arrival,
                                                Flight.flight_no,
                                                Flight.status,
                                                Flight.departure_airport,
                                                Flight.arrival_airport,
                                                Flight.aircraft_code
                                                ).filter(
                        Flight.scheduled_departure >= departure_date,
                        Flight.departure_airport == prev,
                        Flight.arrival_airport == key,
                        Flight.status == "Scheduled"
                    ).order_by(Flight.scheduled_departure).first()
                    prev = key
                    if flight is None:
                        break
                    if st_date is None:
                        if flight.scheduled_departure.day != cur_date.day or flight.scheduled_departure.month != cur_date.month:
                            break
                        st_date = flight.scheduled_departure
                    departure_airport = self.session.query(AirportsDatum.coordinates).filter(
                        AirportsDatum.airport_code == flight.departure_airport).first()[0]
                    arrival_airport = self.session.query(AirportsDatum.coordinates).filter(
                        AirportsDatum.airport_code == flight.arrival_airport).first()[0]
                    dist += self.get_dist(eval(departure_airport), eval(arrival_airport))
                    departure_date = flight['scheduled_arrival']
                    flights.append(FlightBase.from_orm(flight))
                else:
                    res.append(self.generate_cost(fare_condition, dist, cur_date) * num_of_passengers)
            cur_date += timedelta(days=1)
            costs_for_week.append(min(res, default=None))
        return costs_for_week

    async def post_flight(self, data: FlightBase) -> FlightBase:
        """
        Метод для создания перелёта

        :param data: Данные для создания перелёта
        :return: Созданый перелёт
        """
        obj_to_add = Flight(flight_no=data.flight_no,
                            scheduled_departure=data.scheduled_departure,
                            scheduled_arrival=data.scheduled_arrival,
                            departure_airport=data.departure_airport,
                            arrival_airport=data.arrival_airport,
                            status=data.status,
                            aircraft_code=data.aircraft_code,
                            actual_departure=data.actual_departure,
                            actual_arrival=data.actual_arrival
                            )
        self.session.add(obj_to_add)
        self.session.flush()
        self.session.commit()
        return FlightBase.from_orm(obj_to_add)

    async def delete_flight(self, key: int) -> bool:
        """
        Метод удаления перелёта

        :param key: Номер перелёта
        :return: Статус удаления(Удалён/ не удалён)
        """
        if await self.get_single_flight_by_id(key) is None:
            return False
        self.session.delete(self.session.query(Flight).get(key))
        return True

    async def put_flight(self, flight_id: int, data: FlightUpdate) -> bool:
        """
        Метод обновления перелёта

        :param flight_id: Номер перелёта в бд
        :param data: Данные для обновления
        :return: Статус обновления(Обновлён/ не обновлён)
        """
        return self.base_put(Flight, flight_id, data)
