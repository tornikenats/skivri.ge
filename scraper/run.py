import signal, os, sys
from scraper import app
from scraper.util import get_debug_flag
from scraper.settings import ProdConfig, DevConfig
from threading import Event


stop_event = Event()

def quit(signum, frame):
    stop_event.set()

# subscribe to events
for sig in ('TERM', 'HUP', 'INT'):
    signal.signal(getattr(signal, 'SIG'+sig), quit)

config = DevConfig if get_debug_flag() else ProdConfig

app = app.create_app(config)
app.run(stop_event)
