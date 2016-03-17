import os

if os.getenv('FLASK_ENV', 'prod') != 'prod':
    config_name = 'dev'
else:
    config_name = 'prod'


settings = {}
with open('instance/{0}.cfg'.format(config_name)) as f:
    for line in f:
        if line == '\n':
            continue
        (key, val) = line.split('=')
        settings[key.strip()] = val.strip()


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
            'lang': 'eng'},
           {'name': 'droni.ge',
            'url': 'http://droni.ge/rss2.xml',
            'lang': 'geo'}]
