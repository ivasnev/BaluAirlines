from MyAviasales.controllers.base_controller import BaseController
from MyAviasales.models import Flight, AirportsDatum, TicketFlight
from collections import deque
from typing import Optional, List
from MyAviasales.views.flights.schema import FlightBase, FlightUpdate, FlightPath
from sqlalchemy import func
from datetime import datetime, timedelta
from sqlalchemy import and_


class FlightController(BaseController):
    async def get_single_flight_by_id(self, key: int) -> Optional[FlightBase]:
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
                                 max_transits: int):
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
                flights.append(FlightBase.from_orm(flight))
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
        if await self.get_single_flight_by_id(key) is None:
            return False
        self.session.delete(self.session.query(Flight).get(key))
        return True

    async def put_flight(self, flight_id: int, data: FlightUpdate) -> bool:
        return self.base_put(Flight, flight_id, data)
        # obj_to_update = self.session.query(Flight).get(flight_id).one_or_none()
        # if obj_to_update is None:
        #     return False
        # data = data.dict()
        # for key, value in data.items():
        #     if value:
        #         obj_to_update.__setattr__(key, value)
        # self.session.flush()
        # self.session.commit()
        # return True
