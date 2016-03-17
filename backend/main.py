import data_fetcher
import time
import config
import logger
from datetime import datetime

while True:
    logger.info("Start fetching at {0}".format(datetime.utcnow()))
    data_fetcher.update_all_sources()
    time.sleep(config.fetch_wait_secs)
