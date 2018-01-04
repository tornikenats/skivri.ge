from flask import render_template, request, current_app, jsonify
from flask.views import MethodView
from skivrige.helpers.pagination import Pagination
from skivrige.helpers.filters import timedelta
from skivrige.extensions import mongo

class News(MethodView):
    def get(self):
        language = request.args.get('lang', 'eng')
        try:
            current_page = int(request.args.get('page', 1))
            if current_page < 1:
                raise ValueError()
        except ValueError as e:
            current_page = 1

        all_articles = list(mongo.db.articles.find({'lang': language}, {'_id': 0}))
        articles = []
        offset = current_app.config['ARTICLES_PER_PAGE'] * (current_page - 1) + 1
        start = (current_page - 1) * current_app.config['ARTICLES_PER_PAGE']
        end = current_page * current_app.config['ARTICLES_PER_PAGE']

        for i, article in enumerate(all_articles[start:end]):
            article['num'] = offset + i
            article['time_since'] = timedelta(article['date_pub'])
            articles.append(article)

        pagination = Pagination(current_page, current_app.config['ARTICLES_PER_PAGE'], len(all_articles))

        return jsonify(articles)
