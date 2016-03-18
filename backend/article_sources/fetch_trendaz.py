import urllib.request as request
from urllib.error import URLError
from datetime import datetime, timezone, timedelta
from peewee import IntegrityError
import dateutil.parser
import dateutil.tz
from bs4 import BeautifulSoup

from logger import logging
from article_sources.scraper import Scraper

class TrendAz(Scraper):
    def __init__(self):
        super().__init__(__name__)
        self.url = 'http://en.trend.az/scaucasus/georgia/'
        self.source = 'trend.az'

    def fetch(self):
        try:
            with request.urlopen(self.url) as response:
                page = request.urlopen(self.url)
                soup = BeautifulSoup(page.read(), 'lxml')
                articles = soup.find('ul', class_='news-history').find_all('div', class_='text')

                for article in articles:
                    # ignore if paid article
                    if 'class' in article.parent.attrs and 'has-castle' in article.parent['class']:
                        continue

                    href = article.h3.a['href']
                    title = article.h3.a.text
                    date_str = article.span.text
                    description = article.p.text

                    date_pub = dateutil.parser.parse(date_str, fuzzy=True)
                    date_pub = date_pub.astimezone(timezone.utc)

                    row = {
                        'title': title,
                        'author': None,
                        'source': self.source,
                        'date_pub': date_pub,
                        'date_add': datetime.utcnow(),
                        'description': description,
                        'category': None,
                        'link': href,
                        'lang': 'eng'
                    }
                    q = Scraper.ArticlesTable.insert(**row)
                    try:
                        q.execute()
                    except IntegrityError:
                        logging.info('Skipping duplicate entry: {0}, {1}'.format(row['source'], row['date_pub']))
                        continue
        except URLError as e:
            logging.error('URLError for {0}'.format(self.source))
