import os
import sys
import warnings

settings = {}

if '--nodb' in sys.argv:
    settings['NODB'] = True
else:
    settings['NODB'] = False

if '--noanalytics' in sys.argv:
    settings['NOANALYTICS'] = True
else:
    settings['NOANALYTICS'] = False

if os.getenv('FLASK_ENV', 'prod') != 'prod':
    config_name = 'dev'
else:
    config_name = 'prod'

if os.path.exists(f'instance/{config_name}.cfg'):
    with open(f'instance/{config_name}.cfg') as f:
        for line in f:
            if line == '\n':
                continue
            (key, val) = line.split('=')
            settings[key.strip()] = val.strip()
else:
    warnings.warn("Instance folder not found.")
