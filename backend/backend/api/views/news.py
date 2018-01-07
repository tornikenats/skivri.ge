from flask import render_template, request, current_app, jsonify
from flask.views import MethodView
from skivrige.helpers.pagination import Pagination
from skivrige.helpers.filters import timedelta
from skivrige.extensions import mongo
from pymongo import DESCENDING

class News(MethodView):
    def get(self):
        language = request.args.get('lang', 'eng')
        try:
            current_page = int(request.args.get('page', 1))
            if current_page < 1:
                raise ValueError()
        except ValueError as e:
            current_page = 1

        all_articles = list(mongo.db.articles
            .find({'lang': language}, {'_id': 0})
            .sort([('date_pub', DESCENDING)])
            .limit(15)
        )
        articles =[]
        for article in all_articles:
            article['time_since'] = timedelta(article['date_pub'])
            articles.append(article)

        return jsonify(articles)
