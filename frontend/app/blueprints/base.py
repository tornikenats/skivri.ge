from flask import Blueprint
from flask import render_template, abort, jsonify, request, make_response, json
import model.articles as articles
import config
from playhouse.shortcuts import model_to_dict
import math

base_api = Blueprint('base_api', __name__)

ArticlesTable = articles.initialize(config.settings['MYSQL_DB'], config.settings['MYSQL_USER'], config.settings['MYSQL_PASS'])


@base_api.route('/')
@base_api.route('/index')
def root():
    current_page = int(request.args.get('page', 1))
    articles_per_page = 20
    all_articles = ArticlesTable.select()
    total_pages = math.ceil(all_articles.count() / articles_per_page)
    page_boundries = {}
    if current_page < 3:
        page_boundries['min'] = 1
        page_boundries['max'] = 6
    elif current_page > total_pages - 2:
        page_boundries['min'] = total_pages - 4
        page_boundries['max'] = total_pages + 1
    else:
        page_boundries['min'] = current_page - 2
        page_boundries['max'] = current_page + 3

    articles = []
    i = articles_per_page * (current_page-1) + 1
    for article in all_articles.order_by(ArticlesTable.date_pub.desc()).paginate(current_page, articles_per_page):
        article = model_to_dict(article)
        article['id'] = i
        articles.append(article)
        i += 1


    return render_template('index.html', articles=articles, current_page=current_page, total_pages=total_pages, page_boundries=page_boundries)
