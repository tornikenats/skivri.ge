import signal, os, sys, logging, datetime
from scraper.factory import create_app
from scraper.util import get_debug_flag
from scraper.settings import ProdConfig, DevConfig
from scraper.scrapers import *
from threading import Event


stop_event = Event()

def quit(signum, frame):
    stop_event.set()

# subscribe to events
for sig in ('TERM', 'HUP', 'INT'):
    signal.signal(getattr(signal, 'SIG'+sig), quit)

config = DevConfig if get_debug_flag() else ProdConfig

app = create_app(config)
logger = logging.getLogger('skivrige.app')

def runner(config):
    while not stop_event.is_set():
        for subclass in base_scraper.Scraper.__subclasses__():
            if stop_event.is_set():
                continue

            scraperClass = subclass()
            logging.info("Start fetching {0} at {1}".format(scraperClass.name, datetime.datetime.utcnow()))
            scraperClass.fetch()
        
        stop_event.wait(config['FETCH_WAIT_SECONDS'])

app.run(runner)
