from tests.base_test_class import BaseTest


class TestSeats(BaseTest):
    def test_base_func(self):
        data = {
            "aircraft_code": "Tes",
            "seat_no": "2A",
            "fare_conditions": "Business"
        }
        self.test_delete("Tes/2A", code=404)
        self.test_put(
            "Tes/2A",
            data_input=data,
            code=404
        )
        self.test_post(
            data_input=data
        )
        self.test_get_by_key(
            "Tes/2A",
            data=data
        )
        self.test_post(
            data_input=data,
            code=404
        )
        self.test_get_all()
        data_new = {
            "aircraft_code": "Tes",
            "seat_no": "2A",
            "fare_conditions": "Economy"
        }
        self.test_put(
            "Tes/2A",
            data_new
        )
        self.test_get_by_key(
            "Tes/2A",
            data=data_new
        )
        wrong_new = {
            "aircraft_code": "Tes",
            "seat_no": "2A",
            "fare_conditions": "Fconomy"
        }
        self.test_put(
            "Tes/2A",
            wrong_new,
            code=422
        )
        self.test_delete("Tes/2A")
        self.test_get_by_key("Tes/2A", code=404)
