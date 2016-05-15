import config
from validate import validate_article_row
from model.articles import Articles
from model.trends import WordOccurences
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
        validated_article_row = validate_article_row(article_row)

        # insert into db
        q = Articles.insert(**article_row)
        try:
            q.execute()

            # analyze article only if this article is not a duplicate
            Scraper.analyze_trends(article_row['title'])
        except IntegrityError:
            logging.debug('Skipping duplicate entry: {0}, {1}'.format(article_row['source'], article_row['date_pub']))

    @staticmethod
    def analyze_trends(article_title):
        tokens = article_title.split()
        valid_tokens = [token for token in tokens if token not in trend_stop_words]

        for token in valid_tokens:
            token = token.lower()
            word_occurence, created = WordOccurences.get_or_create(word=token, date=datetime.utcnow())
            query = word_occurence.update(count=WordOccurences.count + 1)
            query.execute()


trend_stop_words = []
