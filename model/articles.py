from peewee import *

def initialize(db, user, passw):
    mydb = MySQLDatabase(db, **{'user': user, 'password': passw })

    class BaseModel(Model):
        class Meta:
            database = mydb


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
        
        @classmethod 
        def connect(cls):
            cls._meta.database.connect()

        @classmethod
        def disconnect(cls):
            cls._meta.database.close()

    mydb.create_tables([Articles], safe=True)
    
    return Articles


