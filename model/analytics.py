from peewee import *

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
        
        
    mydb.create_tables([PageViews, Users], safe=True)
    
    return [PageViews, Users]


