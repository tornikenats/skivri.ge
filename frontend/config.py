import os

if os.getenv('FLASK_ENV', 'prod') != 'prod':
    config_name = 'dev'
else:
    config_name = 'prod'