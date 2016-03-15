from flask import Blueprint
from flask import render_template, abort, jsonify, request, make_response, json
import model.articles as articles
import config
from playhouse.shortcuts import model_to_dict

base_api = Blueprint('base_api', __name__)

ArticlesTable = articles.initialize(config.settings['MYSQL_DB'], config.settings['MYSQL_USER'], config.settings['MYSQL_PASS'])


@base_api.route('/')
@base_api.route('/index')
def root():
    articles = []
    i = 1
    for article in ArticlesTable.select().order_by(ArticlesTable.date_pub.desc()):
        article = model_to_dict(article)
        article['id'] = i
        articles.append(article)
        i += 1

    return render_template('index.html', articles=articles)
