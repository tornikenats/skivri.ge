import urllib.request as request
from urllib.error import URLError
from datetime import datetime, timezone, timedelta
from peewee import IntegrityError
import dateutil.parser
import dateutil.tz
import feedparser

from logger import logging
import model.articles as articles
import config

ArticlesTable = articles.initialize(config.settings['MYSQL_DB'], config.settings['MYSQL_USER'], config.settings['MYSQL_PASS'])

def update_all_sources():
    for source in config.sources:
        try:
            with request.urlopen(source['url']) as response:
                root = feedparser.parse(response.read())
                for entry in root['entries']:

                    def ensure_correct_tz(date: datetime):
                        if date.tzinfo is not dateutil.tz.tzutc:
                            georgian_tz = timezone(timedelta(hours=+4),'GET')
                            return date.replace(tzinfo=georgian_tz).astimezone(timezone.utc)
                        return date

                    row = {
                        'title': entry.get('title', None),
                        'author': entry.get('author', None),
                        'source': source['name'],
                        'date_pub': ensure_correct_tz(dateutil.parser.parse(entry.get('published', None))),
                        'date_add': datetime.utcnow(),
                        'description': entry.get('summary', None),
                        'category': entry.get('category', None),
                        'link': entry.get('link', None),
                        'lang': source['lang']
                    }
                    q = ArticlesTable.insert(**row)
                    try:
                        q.execute()
                    except IntegrityError:
                        logging.info('Skipping duplicate entry: {0}, {1}'.format(row['source'], row['date_pub']))
                        continue
        except URLError as e:
            logging.error('URLError for {0}'.format(source['url']))


if __name__ == '__main__':
    update_all_sources()