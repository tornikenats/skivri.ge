import time
from scraper.util import validate_article_row
from scraper.extensions import mongo
from pymongo.errors import DuplicateKeyError
import logging

class Scraper:
    def __init__(self, name):
        self.name = name
        self.logger = logging.getLogger('skivrige.app')

    def _fetch(self):
        raise NotImplemented

    def fetch(self):
        self._fetch()

    def insert_article(self, article):
        validate_article_row(article)

        try:
            mongo.db.articles.insert_one(article)
        except DuplicateKeyError as e:
            self.logger.debug('Skipping article: {}'.format(article['title']))