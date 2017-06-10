from peewee import *

mydb = Proxy()

class BaseModel(Model):
    class Meta:
        database = mydb