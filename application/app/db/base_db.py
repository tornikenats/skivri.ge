from app import settings
from model.base_model import mydb

class Database:
    def __init__(self):
        mydb.init(settings.settings['MYSQL_DB'], max_connections=20, stale_timeout=600,
                **{'user': settings.settings['MYSQL_USER'], 'password': settings.settings['MYSQL_PASS']})

    def connect(self):
        mydb.connect()

    def close(self):
        mydb.close()
    
    def is_closed(self):
        return mydb.is_closed()