import data_fetcher
import time
import config

while True:
    data_fetcher.update_all_sources()
    time.sleep(config.fetch_wait_secs)