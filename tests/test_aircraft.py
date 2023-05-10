from tests.base_test_class import BaseTest


class TestAircraft(BaseTest):
    def test_base_func(self):
        data = {
            "aircraft_code": "Tes",
            "model": {"en": "Test", "ru": "Test"},
            "range": 12345
        }
        self.test_delete("Tes", code=404)
        self.test_put(
            "Tes",
            data_input=data,
            code=404
        )
        res = self.test_post(
            data_input=data
        )
        self.test_get_by_key(
            res.get('aircraft_code'),
            data=data
        )
        self.test_post(
            data_input=data,
            code=404
        )
        self.test_get_all()
        data_new = {
            "aircraft_code": "Tes",
            "model": {"en": "Test2", "ru": "Test2"},
            "range": 10
        }
        self.test_put(
            "Tes",
            data_new
        )
        self.test_get_by_key(
            "Tes",
            data=data_new
        )
        self.test_delete("Tes")
        self.test_get_by_key("Tes", code=200)
