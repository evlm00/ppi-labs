import httpx
import asyncio

import logging

class BaseDataLoader:

    def __init__(self, endpoint=None, logger=None):
        self._base_url = endpoint
        if logger is None:
            logger = logging.getLogger('BASELDR')
        self._logger = logger
        self._logger.info("created")

    async def _fetch(self, url, params=None):
        async with httpx.AsyncClient() as client:
            if params is None:
                response = await client.get(url)
            else:
                response = await client.get(url, params=params)
            return response

    async def _get_req(self, resource, params=None):
        req_url = self._base_url + resource
        self._logger.debug(f"GET: url={req_url}, pramas={params}")
        response = await self._fetch(req_url, params=params)
        self._logger.debug(f"RESPONSE: code={response.status_code}")
        if response.status_code != 200:
            msg = f"Unable to request data from {req_url}, status: {req_url.status}"
            if response.text and response.text.message:
                msg += f", message: {response.text.message}"
            raise RuntimeError(msg)
        return response.text

if __name__ == "__main__":
    loader = BaseDataLoader()
