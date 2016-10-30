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
