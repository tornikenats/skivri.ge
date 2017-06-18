import time
from scraper.validate import validate_article_row
from scraper.logger import logging
from skivrige_model import Articles
from peewee import IntegrityError
from scraper.monitor import SCRAPER_SCRAPE_COUNT, SCRAPER_SCRAPE_DURATION

class Scraper:
    def __init__(self, name):
        self.name = name

    def _fetch(self):
        raise NotImplemented

    def fetch(self):
        self.start_scrape_time = time.time()
        self._fetch()
        scrape_latency = time.time() - self.start_scrape_time
        SCRAPER_SCRAPE_DURATION.labels(self.name).observe(scrape_latency)
        SCRAPER_SCRAPE_COUNT.labels(self.name).inc()

    @staticmethod
    def insert_article(article_row):
        validate_article_row(article_row)

        q = Articles.insert(**article_row)
        try:
            q.execute()
        except IntegrityError:
            logging.debug('Skipping duplicate entry: {0}, {1}'.format(article_row['source'], article_row['date_pub']))