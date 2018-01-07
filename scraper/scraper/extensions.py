from pymongo import MongoClient

class Mongo():
    def init_app(self, app):
        uri = 'mongodb://{}/{}'.format(app.config['MONGO_HOST'], app.config['MONGO_DBNAME'])
        client = MongoClient(uri)
        self.db = client.get_database()

mongo = Mongo()