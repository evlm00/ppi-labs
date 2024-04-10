import json
from datetime import datetime
from enum import Enum

from .baseloader import BaseDataLoader

import asyncio
import logging

class Granularity(Enum):
    ONE_MINUTE=60,
    FIVE_MINUTES=300,
    FIFTEEN_MINUTES=900,
    ONE_HOUR=3600,
    SIX_HOURS=21600,
    ONE_DAY=86400

class CoinbaseLoader(BaseDataLoader):

    def __init__(self, endpoint="https://api.exchange.coinbase.com"):
        super().__init__(endpoint)
        self._logger = logging.getLogger("COINBASE")
        self._logger.info("created")
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)

    async def get_pairs_async(self) -> dict[str, any]:
        self._logger.debug("get pairs")
        data = await self._get_req("/products")
        return json.loads(data)
    
    def get_pairs(self) -> dict[str, any]:
        self._logger.debug("get pairs")
        data = self._loop.run_until_complete(self._get_req("/products"))
        return json.loads(data)

    async def get_stats_async(self, pair: str) -> dict[str, any]:
        self._logger.debug(f"get pair {pair} stats")
        data = await self._get_req(f"/products/{pair}")
        return json.loads(data)
    
    def get_stats(self, pair: str) -> dict[str, any]:
        self._logger.debug(f"get pair {pair} stats")
        data = self._loop.run_until_complete(self._get_req(f"/products/{pair}"))
        return json.loads(data)

    async def get_historical_data_async(self, pair: str, begin: datetime, end: datetime, granularity: Granularity) -> dict[str, any]:
        self._logger.debug(f"get pair {pair} history")
        params = {
            "start": begin,
            "end": end,
            "granularity": granularity.value
        }
        # retrieve needed data from Coinbase
        data = await self._get_req("/products/" + pair + "/candles", params)
        # parse response and create DataFrame from it
        return json.loads(data)
    
    def get_historical_data(self, pair: str, begin: datetime, end: datetime, granularity: Granularity) -> dict[str, any]:
        self._logger.debug(f"get pair {pair} history")
        params = {
            "start": begin,
            "end": end,
            "granularity": granularity.value
        }
        # retrieve needed data from Coinbase
        data = self._loop.run_until_complete(self._get_req("/products/" + pair + "/candles", params))
        # parse response and create DataFrame from it
        return json.loads(data),


if __name__ == "__main__":
    loader = CoinbaseLoader()
    data = loader.get_pairs()
    print(data)
    data = loader.get_stats("btc-usdt")
    print(data)
    data = loader.get_historical_data("btc-usdt", "2023-01-01", "2023-06-30", granularity=Granularity.ONE_DAY)
    print(data.head(5))
