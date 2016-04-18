from flask import Blueprint
from flask import render_template, abort, jsonify, request, make_response, json
import model.articles as articles
import config
from playhouse.shortcuts import model_to_dict
from datetime import datetime
import re

from .helpers.pagination import Pagination

base_api = Blueprint('base_api', __name__)

ArticlesTable = articles.initialize(config.settings['MYSQL_DB'], config.settings['MYSQL_USER'], config.settings['MYSQL_PASS'])

ARTICLES_PER_PAGE = 20

@base_api.route('/')
@base_api.route('/news')
def news():
    language = request.args.get('lang', 'eng')
    current_page = int(request.args.get('page', 1))

    ArticlesTable.connect()
    all_articles = ArticlesTable.select().where(ArticlesTable.lang == language)

    articles = []
    i = ARTICLES_PER_PAGE * (current_page-1) + 1
    for article in all_articles.order_by(ArticlesTable.date_pub.desc()).paginate(current_page, ARTICLES_PER_PAGE):
        article = model_to_dict(article)
        article['id'] = i
        articles.append(article)
        i += 1

    pagination = Pagination(current_page, ARTICLES_PER_PAGE, all_articles.count())

    ArticlesTable.disconnect()
    return render_template('news.html',
       articles=articles,
       current_page=current_page,
       pagination=pagination,
       language=language
    )

@base_api.app_template_filter()
def timedelta(pub_date):
    delta = datetime.utcnow() - pub_date

    secs = delta.total_seconds()
    days, remainder = divmod(secs, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    days_str = ''
    if days != 0:
        days_str = '{:0.0f} day'.format(days)
        if days > 1: days_str += 's'
        days_str += ', '

    hours_str = ''
    if hours != 0:
        hours_str = '{:0.0f} hour'.format(hours)
        if hours > 1: hours_str += 's'
        hours_str += ', '

    minutes_str = ''
    if minutes != 0:
        minutes_str = '{:0.0f} minute'.format(minutes)
        if minutes > 1: minutes_str += 's'
        minutes_str += ', '

    delta_str = '{}{}{}'.format(days_str, hours_str, minutes_str)
    return delta_str.strip(', ') + ' ago'

@base_api.app_template_filter()
def removetags(text):
    TAG_RE = re.compile(r'<[^>]+>')
    return TAG_RE.sub('', text)