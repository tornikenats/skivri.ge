from playhouse.shortcuts import model_to_dict
from app.db.news_db import NewsDatabase
import json
from datetime import datetime

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError ("Type not serializable")


def dump():
    language = 'geo'

    news_db = NewsDatabase()
    all_articles = news_db.get_all_articles(language)

    all_articles_dict = []
    for article in all_articles:
        article_dict = model_to_dict(article)
        article_dict['views'] = article.count
        all_articles_dict.append(article_dict)

    with open(f'{datetime.utcnow()}', 'w') as f:
        f.writelines(json.dumps(all_articles_dict, default=json_serial))
