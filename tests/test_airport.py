from tests.base_test_class import BaseTest


class TestAirport(BaseTest):
    def test_base_func(self):
        data = {
            "airport_code": "TE1",
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
        self.test_delete("TE1", code=404)
        self.test_put(
            "TE1",
            data_input=data,
            code=404
        )
        self.test_post(
            data_input=data
        )
        self.test_get_by_key(
            "TE1",
            data=data
        )
        self.test_post(
            data_input=data,
            code=404
        )
        self.test_get_all()
        data_new = {
            "airport_code": "TE1",
            "airport_name": {
                "ru": "Якутск2",
                "en": "Yakutsk Airport2"
            },
            "city": {
                "ru": "Якутск2",
                "en": "Yakutsk2"
            },
            "coordinates": "(129.77099609375,62.093299865722656)",
            "timezone": "Asia/Yakutsk"
        }
        self.test_put(
            "TE1",
            data_new
        )
        self.test_get_by_key(
            "TE1",
            data=data_new
        )
        self.test_delete("TE1")
        self.test_get_by_key("TE1", code=200)
