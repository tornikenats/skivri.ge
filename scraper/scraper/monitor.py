from prometheus_client import Counter, Summary
from prometheus_client import start_http_server

SCRAPER_SCRAPE_COUNT = Counter('skivrige_scraper_scraper_count', 'Scraper Scrape Count',
                               ['name'])
SCRAPER_SCRAPE_DURATION = Summary('skivrige_scraper_scrape_duration', 'Scraper Scrape Duration',
                                   ['name'])


def monitor(port=8000, addr=''):
    start_http_server(port, addr)
