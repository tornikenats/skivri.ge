from peewee import *
from datetime import datetime
from playhouse.pool import PooledMySQLDatabase

mydb = PooledMySQLDatabase(None)

class BaseModel(Model):
    class Meta:
        database = mydb

class Articles(BaseModel):
    author = CharField(null=True)
    category = CharField(null=True)
    date_add = DateTimeField(default=datetime.utcnow())
    date_pub = DateTimeField()
    description = TextField(null=True)
    link = TextField(null=True)
    source = CharField()
    title = CharField(primary_key=True)
    lang = CharField(max_length=3)
    score = IntegerField(default=0)
