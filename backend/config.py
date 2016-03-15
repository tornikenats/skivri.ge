import os

env = os.getenv('SKIVRI_ENV', 'prod')

path = {'prod': {'pid': '/var/skivri-ge/NewsAggregator-daemon.pid',
                 'log': '/var/skivri-ge/NewsAggregator.log'},
        'debug': {'pid': 'NewsAggregator-daemon.pid',
                  'log': 'NewsAggregator.log'}
        }

fetch_wait_secs = 60 * 15  # 15 minutes

sources = [{'name': 'civil.ge',
            'url': 'http://civil.ge/eng/rss.php',
            'lang': 'eng'},
           {'name': 'agenda.ge',
            'url': 'http://agenda.ge/includes/rss.xml',
            'lang': 'eng'},
           {'name': 'ambebi.ge',
            'url': 'http://feeds.feedburner.com/ambebige?format=xml',
            'lang': 'geo'},
           {'name': 'dfwatch.net',
            'url': 'http://dfwatch.net/feed',
            'lang': 'eng'}]
