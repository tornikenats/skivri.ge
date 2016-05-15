from peewee import *
from datetime import datetime
from .base_model import BaseModel

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
