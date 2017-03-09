from .base_db import Database
from model.articles import Articles
from model.analytics import Users, PageViews, ArticleViews
from peewee import fn, JOIN
from model.base_model import mydb

class AnalyticsDatabase(Database):

    def __init__(self):
        super().__init__()
        mydb.create_tables([Users, PageViews, ArticleViews], safe=True)
    
    def report_pageview(self, **kwargs):
        user, created = Users.get_or_create(ip=kwargs['ip'])
        kwargs['user'] = user.id
        PageViews.create(**kwargs)

    def report_articleview(self, **kwargs):
        user, created = Users.get_or_create(ip=kwargs['ip'])
        article = Articles.get(id=kwargs['id'])

        kwargs['user'] = user.id
        kwargs['article'] = article.id

        ArticleViews.create(**kwargs)
    
    def get_pageviews(self, start_date, end_date):
        return PageViews \
            .select(PageViews.date, PageViews.user) \
            .where(PageViews.date.between(start_date, end_date))
    
    def get_articleviews(self, start_date, end_date):
        # will return (title, #views)
        # article_views = ArticleViews\
        #     .select(ArticleViews.title, fn.Count(ArticleViews.title).alias("num_views"))

        return ArticleViews \
            .select(ArticleViews.date, ArticleViews.user) \
            .where(ArticleViews.date.between(start_date, end_date))