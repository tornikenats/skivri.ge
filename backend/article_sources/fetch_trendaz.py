import urllib.request as request
from urllib.error import URLError
from datetime import datetime, timezone, timedelta
from peewee import IntegrityError
import dateutil.parser
import dateutil.tz
from bs4 import BeautifulSoup

from model.articles import Articles
from logger import logging
from article_sources.scraper import Scraper
from validate import validate_article_row

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
                articles = soup.find('div', class_='hot-topics-list').find_all('div', class_='media')

                for article in articles:
                    body = article.contents[3]
                    body_info = body.contents[3]
                    # ignore if paid article
                    if body_info.find(class_='fa-lock'):
                        continue

                    body_heading = body.contents[1]
                    body_description = body.contents[5]
                    href = body_heading.a['href']
                    title = body_heading.a.text
                    date_str = body_info.find(class_='date-created').text
                    description = body_description.text

                    date_pub = dateutil.parser.parse(date_str, fuzzy=True)
                    date_pub = date_pub.replace(tzinfo=timezone(timedelta(hours=+4), 'AZT'))
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
                    q = Articles.insert(**validate_article_row(row))
                    try:
                        q.execute()
                    except IntegrityError:
                        logging.debug('Skipping duplicate entry: {0}, {1}'.format(row['source'], row['date_pub']))
                        continue
        except URLError as e:
            logging.error('URLError for {0}'.format(self.source))
