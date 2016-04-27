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
import util

class TrendAz(Scraper):
    def __init__(self):
        super().__init__(__name__)
        self.url = 'http://georgiatoday.ge/en/news'
        self.source = 'georgiatoday.ge'

    def fetch(self):
        try:
            with request.urlopen(self.url) as response:
                page = request.urlopen(self.url)
                soup = BeautifulSoup(page.read(), 'lxml')
                articles = soup.find(id="latestNews").find_all(class_="itm")

                # use date of fetch as date of publish since article has no date
                date_pub = datetime.utcnow()
                date_pub = date_pub.replace(tzinfo=timezone.utc)
                for article in articles:
                    article = article.div
                    href = 'http://www.georgiatoday.ge' + article.contents[1].a['href']
                    title = article.contents[1].a.text.strip()
                    category = article.contents[3].text.strip()
                    description = article.contents[7].text.strip()

                    # ensure order of articles are preserved
                    date_pub = date_pub - timedelta(seconds=1)

                    row = {
                        'title': title,
                        'author': None,
                        'source': self.source,
                        'date_pub': date_pub,
                        'date_add': datetime.utcnow(),
                        'description': description,
                        'category': category,
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
