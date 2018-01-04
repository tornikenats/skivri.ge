import urllib.request as request
from urllib.error import URLError
from datetime import datetime, timezone, timedelta
import dateutil.parser
import dateutil.tz
import feedparser
from .base_scraper import Scraper

sources = [{'name': 'civil.ge',
            'url': 'http://civil.ge/eng/rss.php',
            'lang': 'eng'},
           {'name': 'agenda.ge',
            'url': 'http://agenda.ge/includes/rss.xml',
            'lang': 'eng'},
           {'name': 'ambebi.ge',
            'url': 'http://feeds.feedburner.com/ambebige?format=xml',
            'lang': 'geo'},
           {'name': 'dfwatch.net',
            'url': 'http://dfwatch.net/feed',
            'lang': 'eng'}]


class AllRSS(Scraper):
    def __init__(self):
        super().__init__(__name__)

    def _fetch(self):
        for source in sources:
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

                        super().insert_article(row)
            except URLError as e:
                self.logger.error('URLError for {0}'.format(source['url']))