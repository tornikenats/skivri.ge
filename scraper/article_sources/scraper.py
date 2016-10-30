from validate import validate_article_row
from model.articles import Articles
from peewee import IntegrityError
from logger import logging
from datetime import datetime


class Scraper:
    def __init__(self, name):
        self.name = name

    def fetch(self):
        raise NotImplemented

    @staticmethod
    def insert_article(article_row):
        validate_article_row(article_row)

        # insert into db
        q = Articles.insert(**article_row)
        try:
            q.execute()

            # analyze article only if this article is not a duplicate
            Scraper.analyze_trends(article_row['title'])
        except IntegrityError:
            logging.debug('Skipping duplicate entry: {0}, {1}'.format(article_row['source'], article_row['date_pub']))

trend_stop_words = []
