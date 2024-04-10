import httpx

class TestClass:

    @staticmethod
    def setup_class(cls):
        TestClass._baseurl = "http://127.0.0.1:8000/users/"
        TestClass._client = httpx.Client()

    def test_user_list(self):
        resp = self._client.get(self._baseurl)
        assert resp.status_code == 200, f"Invalid response: {resp.status_code}"
        resp = resp.json()
        assert resp[0]['email'] == 'mee@mail.com', f"Unexpected response:\n{resp}"
        assert resp[1]['email'] == 'you@mail.com', f"Unexpected response:\n{resp}"

    def test_user_add(self):
        headers = {'Content-Type': 'application/json'}
        data = {'email': "someone@mail.com"}
        resp = self._client.post(self._baseurl, headers=headers, json=data)
        assert resp.status_code == 201, f"Invalid response: {resp_status_code}"

        resp = self._client.get(self._baseurl)
        assert resp.status_code == 200, "Invalid response"
        resp = resp.json()
        assert resp[0]['email'] == 'mee@mail.com', f"Unexpected response:\n{resp}"
        assert resp[1]['email'] == 'you@mail.com', f"Unexpected response:\n{resp}"
        assert len(resp) > 2, f"Invalid number of users: {len(resp)}"

    def test_users_delete(self):
        resp = self._client.get(self._baseurl)
        assert resp.status_code == 200, f"Invalid response: {resp.status_code}"
        count = len(resp.json())
        assert count > 1, f"Number of users={count}, but should be greater than 1)"

        resp = self._client.delete(self._baseurl + str(count - 1))
        assert resp.status_code == 204, f"Unexpected response: {resp.status_code}"

        resp = self._client.get(self._baseurl)
        assert resp.status_code == 200, f"Invalid response: {resp.status_code}"
        count2 = len(resp.json())
        assert count == count2 + 1, f"Number of users={count2}, but should be {count - 1})"
