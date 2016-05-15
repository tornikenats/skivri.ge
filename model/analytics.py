from peewee import *
from .base_model import BaseModel

class Users(BaseModel):
    ip = CharField(max_length=45, primary_key=True)

class PageViews(BaseModel):
    title = TextField(default='')
    url = TextField()
    date = DateTimeField(index=True)
    user = ForeignKeyField(Users)
    referrer = TextField(default='')
    headers = TextField(default='')
    params = TextField(default='')