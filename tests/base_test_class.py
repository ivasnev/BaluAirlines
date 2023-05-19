class BaseTest:
    def __init__(self, client, base_url):
        self.client = client
        self.base_url = base_url

    def test_get_all(self, code: int = 200, data: dict = None):
        response = self.client.get(self.base_url)
        assert response.status_code == code
        if data:
            assert response.json() == data

    def test_get_by_key(self, key, code: int = 200, data: dict = None):
        response = self.client.get(self.base_url + key)
        assert response.status_code == code
        if data:
            assert response.json() == data

    def test_post(self, data_input: dict, code: int = 200, data_output: dict = None):
        response = self.client.post(
            self.base_url,
            json=data_input,
        )
        assert response.status_code == code
        if data_output:
            assert response.json() == data_output
        return response.json()

    def test_put(self, key, data_input: dict, code: int = 200, data_output: dict = None):
        response = self.client.put(
            self.base_url + key,
            json=data_input,
        )
        assert response.status_code == code
        if data_output:
            assert response.json() == data_output

    def test_delete(self, key, code: int = 200, data_output: dict = None):
        response = self.client.delete(
            self.base_url + key,
        )
        assert response.status_code == code
        if data_output:
            assert response.json() == data_output
