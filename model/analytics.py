from peewee import *
from .articles import Articles
from .base_model import BaseModel


class Users(BaseModel):
    ip = CharField(max_length=45, unique=True)


class PageViews(BaseModel):
    title = TextField(default='')
    url = TextField()
    date = DateTimeField(index=True)
    user = ForeignKeyField(Users)
    referrer = TextField(default='')
    headers = TextField(default='')
    params = TextField(default='')


class ArticleViews(BaseModel):
    date = DateTimeField(index=True)
    user = ForeignKeyField(Users)
    article = ForeignKeyField(Articles)
