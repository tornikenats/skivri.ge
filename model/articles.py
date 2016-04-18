from peewee import *
from datetime import datetime

def initialize(db, user, passw):
    mydb = MySQLDatabase(db, **{'user': user, 'password': passw })

    class BaseModel(Model):
        class Meta:
            database = mydb

        @classmethod 
        def connect(cls):
            cls._meta.database.connect()

        @classmethod
        def disconnect(cls):
            cls._meta.database.close()


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
        score = IntegerField()
        

    mydb.create_tables([Articles], safe=True)
    
    return Articles

