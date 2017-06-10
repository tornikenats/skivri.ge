from scraper.validate import validate_article_row
from scraper.logger import logging
from skivrige_model import Articles
from peewee import IntegrityError


class Scraper:
    def __init__(self, name):
        self.name = name

    def fetch(self):
        raise NotImplemented

    @staticmethod
    def insert_article(article_row):
        validate_article_row(article_row)

        q = Articles.insert(**article_row)
        try:
            q.execute()
        except IntegrityError:
            logging.debug('Skipping duplicate entry: {0}, {1}'.format(article_row['source'], article_row['date_pub']))