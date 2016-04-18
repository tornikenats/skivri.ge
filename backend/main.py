import importlib
import time
from datetime import datetime

import config
from article_sources import *
from logger import logging

while True:
    # execute all scrapers
    for subclass in scraper.Scraper.__subclasses__():
        try:
            scraperClass = subclass()
            logging.info("Start fetching {0} at {1}".format(scraperClass.name, datetime.utcnow()))
            scraperClass.fetch()
        except Exception as e:
            logging.error("Error in {0} scraper: {1}".format(scraperClass.name, e))

    time.sleep(config.fetch_wait_secs)
