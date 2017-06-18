import urllib.request as request
from urllib.error import URLError
from datetime import datetime, timezone, timedelta, time
import dateutil.parser
import dateutil.tz
from bs4 import BeautifulSoup
from .base_scraper import Scraper
from scraper.util import month_geo_to_eng
from scraper.logger import logging

class VOA(Scraper):
    def __init__(self):
        super().__init__(__name__)
        self.url = 'http://www.amerikiskhma.com/z/1849.html'
        self.source = 'amerikiskhma.com'

    def _fetch(self):
        try:
            fixed_start_time = datetime.utcnow()

            with request.urlopen(self.url) as response:
                page = request.urlopen(self.url)
                soup = BeautifulSoup(page.read(), 'lxml')
                articles = soup.find_all(class_="content")

                for article in articles:
                    href = 'http://www.amerikiskhma.com' + article.a['href']
                    title = article.a.h4.text
                    date_str = article.span.text
                    geo_month = date_str.split()[0]
                    date_str = date_str.replace(geo_month, month_geo_to_eng[geo_month])
                    description = article.a.p.text

                    date_pub = dateutil.parser.parse(date_str, fuzzy=True)
                    date_pub = date_pub.replace(tzinfo=timezone(timedelta(hours=+4), 'GET'))
                    date_pub = date_pub.astimezone(timezone.utc)

                    # if no time present set fetch time
                    if date_pub.time() == time(hour=0,minute=0,second=0):
                        date_pub = date_pub.replace(hour=fixed_start_time.hour, minute=fixed_start_time.minute, second=fixed_start_time.second)
                        # move time back by a second as we go down in articles chronologically
                        fixed_start_time = fixed_start_time - timedelta(seconds=1)

                    row = {
                        'title': title,
                        'author': None,
                        'source': self.source,
                        'date_pub': date_pub,
                        'date_add': datetime.utcnow(),
                        'description': description,
                        'category': None,
                        'link': href,
                        'lang': 'geo'
                    }

                    super().insert_article(row)
        except URLError as e:
            logging.error('URLError for {0}'.format(self.source))