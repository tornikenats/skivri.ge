#!/usr/bin/env python

import sys, time
import data_fetcher
import config
from daemon import Daemon

class NewsAggregatorDaemon(Daemon):
    def run(self):
        while True:
            data_fetcher.update_all_sources()
            time.sleep(config.fetch_wait_secs)


if __name__ == "__main__":
    daemon = NewsAggregatorDaemon(config.path[config.env]['pid'])
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print
            "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)
