from tests.base_test_class import BaseTest
from tests.test_aircraft import TestAircraft
from tests.test_airport import TestAirport
from tests.test_seats import TestSeats


class TestFlights(BaseTest):
    def __init__(self, client, base_url):
        super().__init__(client, base_url)
        self.class_inst = {
            "aircraft": TestAircraft(self.client, "/aircraft/"),
            "airport": TestAirport(self.client, "/airports/"),
            "seats": TestSeats(self.client, "/seats/")
        }
        self.aircraft_1 = {
            "aircraft_code": "Te1",
            "model": {"en": "Test", "ru": "Test"},
            "range": 12000
        }
        self.aircraft_2 = {
            "aircraft_code": "Te2",
            "model": {"en": "Test", "ru": "Test"},
            "range": 10000
        }
        self.airport_1 = {
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
        self.airport_2 = {
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
        self.airport_3 = {
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

    def base_fill_for_flights(self):
        """
        Базовое заполнение
        
        :return: Ничего
        """
        self.class_inst["aircraft"].test_post(self.aircraft_1)
        self.class_inst["aircraft"].test_post(self.aircraft_2)
        self.class_inst["airport"].test_post(self.airport_1)
        self.class_inst["airport"].test_post(self.airport_2)
        self.class_inst["airport"].test_post(self.airport_3)
        for i in range(1, 5):
            for letter in "ABCD":
                self.class_inst["seats"].test_post(
                    data_input={
                        "aircraft_code": self.aircraft_1["aircraft_code"],
                        "seat_no": str(i) + letter,
                        "fare_conditions": "Business"
                    }
                )
                self.class_inst["seats"].test_post(
                    data_input={
                        "aircraft_code": self.aircraft_2["aircraft_code"],
                        "seat_no": str(i) + letter,
                        "fare_conditions": "Business"
                    }
                )
        for i in range(5, 25):
            for letter in "ABCDEF":
                self.class_inst["seats"].test_post(
                    data_input={
                        "aircraft_code": self.aircraft_1["aircraft_code"],
                        "seat_no": str(i) + letter,
                        "fare_conditions": "Economy"
                    }
                )
                self.class_inst["seats"].test_post(
                    data_input={
                        "aircraft_code": self.aircraft_2["aircraft_code"],
                        "seat_no": str(i) + letter,
                        "fare_conditions": "Economy"
                    }
                )

    def test_get_all(self, code: int = 200, data: dict = None):
        response = self.client.get(self.base_url + "all")
        assert response.status_code == code
        if data:
            assert response.json() == data

    def test_base_func(self):
        self.base_fill_for_flights()
        data = {
            "flight_no": "TEST01",
            "scheduled_departure": "2023-04-29T19:05:00+03:00",
            "scheduled_arrival": "2023-04-29T20:00:00+03:00",
            "departure_airport": self.airport_1["airport_code"],
            "arrival_airport": self.airport_2["airport_code"],
            "status": "Scheduled",
            "aircraft_code": self.aircraft_1["aircraft_code"],
            "actual_departure": None,
            "actual_arrival": None
        }
        self.test_delete('11111', code=404)
        self.test_put(
            '11111',
            data_input=data,
            code=404
        )
        res = self.test_post(
            data_input=data
        )
        self.test_get_by_key(
            "id/" + str(res["flight_id"]),
            data=data
        )
        self.test_get_by_key(
            "id/0",
            code=404
        )
        self.test_get_by_key(
            "no/TEST01?date=2023-04-28 12%3a25%3a00%2b03",
            data=data
        )
        self.test_get_by_key(
            "no/TEST02?date=2023-04-28 12%3a25%3a00%2b03",
            code=404
        )
        self.test_get_by_key(
            "?departure_date=2017-05-01 12%3a25%3a00%2b03&departure_airport={}&arrival_airport={}&max_transits=5".format(
                self.airport_1["airport_code"],
                self.airport_2["airport_code"])
        )
        self.test_get_by_key(
            "path/{}/{}?departure_date=2050-05-01 12%3a25%3a00%2b03".format(
                self.airport_1["airport_code"],
                self.airport_2["airport_code"]),
            code=404
        )
        self.test_get_by_key(
            "best_price/?departure_date=2017-05-01 12%3a25%3a00%2b03&" +
            "departure_airport={}&arrival_airport={}&max_transits=5".format(
                self.airport_1["airport_code"],
                self.airport_2["airport_code"]),
            code=200
        )
        self.test_get_by_key(
            "table/YKS?departure_date=2023-04-29 12%3a25%3a00%2b03&",
            code=200
        )

        self.test_get_all()
        data_new = {
            "flight_no": "TEST01",
            "scheduled_departure": "2023-04-29T19:05:00+03:00",
            "scheduled_arrival": "2023-04-29T20:00:00+03:00",
            "departure_airport": self.airport_1["airport_code"],
            "arrival_airport": self.airport_2["airport_code"],
            "status": "Scheduled",
            "aircraft_code": self.aircraft_1["aircraft_code"],
            "actual_departure": "2023-04-29T19:05:10+03:00",
            "actual_arrival": "2023-04-29T20:10:00+03:00"
        }
        self.test_put(
            str(res["flight_id"]),
            data_new
        )
        self.test_get_by_key(
            "id/" + str(res["flight_id"]),
            data=data_new
        )
        self.test_delete(str(res["flight_id"]))
        self.test_get_by_key("id/" + str(res["flight_id"]), code=404)
