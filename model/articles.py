from peewee import *
import config

database = MySQLDatabase(config.items['MYSQL_DB'], **{'user': config.items['MYSQL_USER'], 'password': config.items['MYSQL_PASS'] })

class BaseModel(Model):
    class Meta:
        database = database


class Articles(BaseModel):
    author = CharField(null=True)
    category = CharField(null=True)
    date_add = DateTimeField()
    date_pub = DateTimeField()
    description = TextField(null=True)
    link = TextField(null=True)
    source = CharField()
    title = TextField(null=True)
    lang = CharField(max_length=3)

    class Meta:
        db_table = 'Articles'
        indexes = (
            (('date_pub', 'source'), True),
        )
        primary_key = CompositeKey('date_pub', 'source')


def initialize():
    database.connect()
    database.create_tables([Articles], safe=True)
