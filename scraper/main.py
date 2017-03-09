import time
from datetime import datetime
from playhouse.pool import PooledMySQLDatabase
from model.base_model import mydb
from model.articles import Articles
import config
from article_sources import *
from logger import logging

db = PooledMySQLDatabase(config.settings['MYSQL_DB'], max_connections=20, stale_timeout=600,
                    **{'user': config.settings['MYSQL_USER'], 'password': config.settings['MYSQL_PASS']})
mydb.initialize(db)
mydb.create_tables([Articles], safe=True)

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
