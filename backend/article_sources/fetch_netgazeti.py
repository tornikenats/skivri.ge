import urllib.request as request
from urllib.error import URLError
from datetime import datetime, timezone, timedelta, time
from peewee import IntegrityError
import dateutil.parser
import dateutil.tz
from bs4 import BeautifulSoup

from logger import logging
from article_sources.scraper import Scraper
from validate import validate_article_row
import util

class TrendAz(Scraper):
    def __init__(self):
        super().__init__(__name__)
        self.url = 'http://netgazeti.ge/category/news/'
        self.source = 'netgazeti.ge'

    def fetch(self):
        try:
            fixed_start_time = datetime.utcnow()

            with request.urlopen(self.url) as response:
                page = request.urlopen(self.url)
                soup = BeautifulSoup(page.read(), 'lxml')
                articles = soup.find_all(class_="content-right")

                for article in articles:
                    href = article.h2.a['href']
                    title = article.h2.a.text
                    author = util.direct_translate(article.div.contents[1].text).title()
                    date_str = article.div.contents[3].text
                    description = article.div.contents[7].text.strip()

                    date_pub = dateutil.parser.parse(date_str, fuzzy=True)
                    date_pub = date_pub.replace(tzinfo=timezone.utc)

                    # if no time present set fetch time
                    if date_pub.time() == time(hour=0,minute=0,second=0):
                        date_pub = date_pub.replace(hour=fixed_start_time.hour, minute=fixed_start_time.minute, second=fixed_start_time.second)
                        # move time back by a second as we go down in articles chronologically
                        fixed_start_time = fixed_start_time - timedelta(seconds=1)

                    row = {
                        'title': title,
                        'author': author,
                        'source': self.source,
                        'date_pub': date_pub,
                        'description': description,
                        'link': href,
                        'lang': 'geo'
                    }
                    q = Scraper.ArticlesTable.insert(**validate_article_row(row))
                    try:
                        q.execute()
                    except IntegrityError:
                        logging.debug('Skipping duplicate entry: {0}, {1}'.format(row['source'], row['date_pub']))
                        continue
        except URLError as e:
            logging.error('URLError for {0}'.format(self.source))
