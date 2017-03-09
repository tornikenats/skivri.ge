from peewee import fn, JOIN
from playhouse.shortcuts import model_to_dict
from playhouse.test_utils import test_database
from peewee import SqliteDatabase

from .base_db import Database
from model.articles import Articles
from model.analytics import ArticleViews, Users
from model.base_model import mydb
from app import settings
import json
from datetime import datetime

class NewsDatabase(Database):

    def __init__(self):
        super().__init__()
        mydb.create_tables([Articles], safe=True)

    def get_all_articles(self, language):
        all_articles = Articles\
            .select()\
            .join(ArticleViews, JOIN.LEFT_OUTER)\
            .where(Articles.lang == language)\
            .switch(Articles)\
            .select(
                Articles, fn.COUNT(ArticleViews.article).alias('count'))\
            .group_by(Articles)\
            .order_by(Articles.date_pub.desc())

        return all_articles

class NewsDatabaseMock(Database):
    def __init__(self):
        self.test_db = SqliteDatabase(':memory:')

    def create_test_data(self):
        user = Users.create(ip='random-ip')

        with open('eng_articles.json', 'r') as f:
            for article in json.loads(''.join(f.readlines())):
                article['date_add'] = datetime.strptime(article['date_add'], "%Y-%m-%dT%H:%M:%S")
                article['date_pub'] = datetime.strptime(article['date_pub'], "%Y-%m-%dT%H:%M:%S") 
                Articles.create(**article)

                ArticleViews.create(date=datetime.utcnow(),
                                    user=user.id,
                                    article=article['id'])

        with open('geo_articles.json', 'r') as f:
            for article in json.loads(''.join(f.readlines())):
                article['date_add'] = datetime.strptime(article['date_add'], "%Y-%m-%dT%H:%M:%S")
                article['date_pub'] = datetime.strptime(article['date_pub'], "%Y-%m-%dT%H:%M:%S") 
                Articles.create(**article)

                ArticleViews.create(date=datetime.utcnow(),
                                    user=user.id,
                                    article=article['id'])

        
    def get_all_articles(self, language):
        with test_database(self.test_db, [Articles, ArticleViews, Users]):
            self.create_test_data()
            all_articles = Articles\
                .select()\
                .join(ArticleViews, JOIN.LEFT_OUTER)\
                .where(Articles.lang == language)\
                .switch(Articles)\
                .select(
                    Articles, fn.COUNT(ArticleViews.article).alias('count'))\
                .group_by(Articles)\
                .order_by(Articles.date_pub.desc())
            
            return list(all_articles)