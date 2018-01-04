import urllib.request as request
from urllib.error import URLError
from datetime import datetime, timezone, timedelta
import dateutil.parser
import dateutil.tz
from bs4 import BeautifulSoup
from .base_scraper import Scraper

class TrendAz(Scraper):
    def __init__(self):
        super().__init__(__name__)
        self.url = 'http://www.interpressnews.ge/en/all-the-news-of-the-day.html?view=allnews'
        self.source = 'interpressnews.ge'

    def _fetch(self):
        try:
            with request.urlopen(self.url) as response:
                page = request.urlopen(self.url)
                soup = BeautifulSoup(page.read(), 'lxml')
                articles = soup.find_all(class_="other_itemb")

                for article in articles:
                    href = 'http://www.interpressnews.ge' + article.contents[3].a['href']
                    title = article.img['title'].strip()
                    date_str = article.contents[5].text
                    description = article.contents[7].text.strip()

                    date_pub = dateutil.parser.parse(date_str, fuzzy=True)
                    date_pub = date_pub.replace(tzinfo=timezone(timedelta(hours=+4), 'GET'))
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

                    super().insert_article(row)
        except URLError as e:
            self.logger.error('URLError for {0}'.format(self.source))
