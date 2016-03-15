import urllib.request as request
from datetime import datetime, timezone, timedelta

import backend.config as config
import dateutil.parser
import dateutil.tz
import feedparser
from backend.logger import logging
from model.articles import initialize, Articles
from peewee import IntegrityError

initialize()


def update_all_sources():
    for source in config.sources:
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
                q = Articles.insert(**row)
                try:
                    q.execute()
                except IntegrityError:
                    logging.debug('Skipping duplicate entry: {0}, {1}'.format(row['source'], row['date_pub']))
                    continue
