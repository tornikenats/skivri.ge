from peewee import *
from playhouse.pool import PooledMySQLDatabase

mydb = PooledMySQLDatabase(None)

class BaseModel(Model):
    class Meta:
        database = mydb
