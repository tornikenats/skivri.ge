import data_fetcher
import time
import config
from logger import logging
from datetime import datetime

while True:
    logging.info("Start fetching at {0}".format(datetime.utcnow()))
    data_fetcher.update_all_sources()
    time.sleep(config.fetch_wait_secs)
