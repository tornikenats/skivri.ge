from peewee import *
from playhouse.pool import PooledMySQLDatabase

mydb = PooledMySQLDatabase(charset='utf8')

class BaseModel(Model):
    class Meta:
        database = mydb
