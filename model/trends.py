from peewee import *
from .base_model import BaseModel

class WordOccurences(BaseModel):
    date = DateTimeField(index=True)
    word = CharField(index=True)
    count = IntegerField(default=0)