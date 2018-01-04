import os, sys
import datetime
from scraper.scrapers import *
import logging
import sys
import time
from scraper.extensions import db
from pymongo import DESCENDING


class App():
    def __init__(self, config):
        self.config = config
        self.init_logger()
    
    def init_logger(self):
        logging.basicConfig(
            format='%(asctime)s | %(levelname)s | %(message)s',
            datefmt='%m/%d/%Y %I:%M:%S %p',
            stream=sys.stdout, 
            level=self.config.LOG_LEVEL)
        self.logger = logging.getLogger(__name__)

    def run(self, stop_event):
        while not stop_event.is_set():
            for subclass in base_scraper.Scraper.__subclasses__():
                if stop_event.is_set():
                    continue

                scraperClass = subclass()
                logging.info("Start fetching {0} at {1}".format(scraperClass.name, datetime.datetime.utcnow()))
                scraperClass.fetch()
            
            stop_event.wait(self.config.FETCH_WAIT_SECONDS)


def create_app(config):    
    app = App(config)
    init_db()
    
    return app


def init_db():
    if 'articles' not in db.collection_names():
        articles = db.articles
        articles.create_index(
            [('title', DESCENDING)],
            unique=True
        )
    else:
        articles = db.articles