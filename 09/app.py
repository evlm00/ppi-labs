from dataloader.coinbaseloader import CoinbaseLoader, Granularity

from models.pairs import Pairs

import asyncio
import os
import yaml
import json
import logging
import logging.config

DUMP_JSON=False

def setup_logging(path='logger.yml', level=logging.INFO, env_key='LOG_CONFIG'):
    path = os.getenv(env_key, path)
    if (os.path.exists(path)):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=level)

def dump_json(data: dict[str, any], fname: str):
    if DUMP_JSON:
        with open(fname, 'wt') as f:
            json.dump(data, f)

async def main(log):
    log.info("Begin")
    loader = CoinbaseLoader()

    pairs = await loader.get_pairs()
    log.debug("Pairs received")
    dump_json(pairs, "pairs.json")
    log.debug("Pairs stored")
    pairs = Pairs.model_validate(pairs)

    stats = await loader.get_stats("btc-usdt")
    log.debug("Stats for btc-usdt receievd")
    dump_json(pairs, "stats.json")
    log.debug("Stats for btc-usdt stored")

    data = await loader.get_historical_data("btc-usdt", "2023-0101", "2023-06-30", Granularity.ONE_DAY)
    log.debug("Data received")
    dump_json(data, "data.json")
    log.debug("Data stored")
    log.info("End")

if __name__ == "__main__":
    setup_logging()
    log = logging.getLogger("APPMAIN")
    asyncio.run(main(log))
