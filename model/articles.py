from peewee import *

def initialize(db, user, passw):
    mydb = MySQLDatabase(db, **{'user': user, 'password': passw })
    mydb.connect()

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

        class Meta:
            db_table = 'Articles'
            indexes = (
                (('date_pub', 'source'), True),
            )
            primary_key = CompositeKey('date_pub', 'source')

    mydb.create_tables([Articles], safe=True)
    
    return Articles

