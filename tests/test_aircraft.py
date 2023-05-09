from tests.base_test_class import BaseTest


class TestAircraft(BaseTest):
    def test_base_func(self):
        data = {
            "aircraft_code": "Tes",
            "model": {"en": "Test", "ru": "Test"},
            "range": 12345
        }
        res = self.test_post(
            data_input=data
        )
        self.test_get_by_key(
            res.get('aircraft_code'),
            data=data
        )
        self.test_put(
            "Tes",
            {
                "range": 10
            }
        )
        data["range"] = 10
        self.test_get_by_key(
            "Tes",
            data=data
        )
        self.test_delete("Tes")
        self.test_get_by_key("Tes", code=200)
