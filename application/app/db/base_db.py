from app import settings
from model.base_model import mydb
from peewee import *
from playhouse.pool import PooledMySQLDatabase


class Database:
    def __init__(self):
        if settings.settings['NODB']:
            db = SqliteDatabase(':memory:')
        else:
            db = PooledMySQLDatabase(settings.settings['MYSQL_DB'], max_connections=20, stale_timeout=600,
                    **{'user': settings.settings['MYSQL_USER'], 'password': settings.settings['MYSQL_PASS']})
        mydb.initialize(db)

    def connect(self):
        mydb.connect()

    def close(self):
        mydb.close()
    
    def is_closed(self):
        return mydb.is_closed()