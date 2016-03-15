from flask import Blueprint
from flask import render_template, abort, jsonify, request, make_response, json
from model.articles import initialize, Articles

base_api = Blueprint('base_api', __name__)


@base_api.route('/')
@base_api.route('/index')
def root():
    articles = []
    i = 1
    for article in Articles.select().order_by(Articles.date_pub.desc()):
        article = article.to_dict()
        article['id'] = i
        articles.append(article)
        i += 1

    return render_template('index.html', articles=articles)
