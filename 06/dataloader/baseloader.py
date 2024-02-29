from datetime import datetime
import requests
import pandas as pd

class BaseDataLoader:

    def __init__(self, endpoint=None):
        self._base_url = endpoint

    def _get_req(self, resource, params=None):
        req_url = self._base_url + resource
        if params is not None:
            response = requests.get(req_url, params=params)
        else:
            response = requests.get(req_url)
        if response.status_code != 200:
            msg = f"Unable to request data from {req_url}, status: {req_url.status}"
            if response.text and response.text.message:
                msg += f", message: {response.text.message}"
            raise RuntimeError(msg)
        return response.text

if __name__ == "__main__":
    loader = BaseDataLoader()