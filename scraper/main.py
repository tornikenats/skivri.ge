import time
import signal, os, sys
import datetime
from peewee import MySQLDatabase
from skivrige_model import mydb, Articles
from scraper.scrapers import *
from scraper.settings import ProdConfig, DevConfig
from scraper.util import get_debug_flag
from scraper.logger import logging

CONFIG = DevConfig if get_debug_flag() else ProdConfig

db = MySQLDatabase(CONFIG.MYSQL_DB, host=CONFIG.MYSQL_HOST, port=int(CONFIG.MYSQL_PORT), user=CONFIG.MYSQL_USER, passwd=CONFIG.MYSQL_PASS)
mydb.initialize(db)
mydb.create_tables([Articles], safe=True)


def handler(signum, frame):
    if signum == signal.SIGINT:
        logging.info('Recieved interrupt. Stopping...')
        sys.exit()

signal.signal(signal.SIGINT, handler)

while True:
    # execute all scrapers
    for subclass in base_scraper.Scraper.__subclasses__():
        try:
            scraperClass = subclass()
            logging.info("Start fetching {0} at {1}".format(scraperClass.name, datetime.datetime.utcnow()))
            scraperClass.fetch()
        except Exception as e:
            logging.error("Error in {0} scraper: {1}".format(scraperClass.name, e))
    
    time.sleep(CONFIG.FETCH_WAIT_SECONDS)