from flask import Blueprint
from flask import render_template, abort, jsonify, request, make_response, json
import model.articles as articles
import config
from playhouse.shortcuts import model_to_dict
import math
from datetime import datetime
import re

base_api = Blueprint('base_api', __name__)

ArticlesTable = articles.initialize(config.settings['MYSQL_DB'], config.settings['MYSQL_USER'], config.settings['MYSQL_PASS'])


@base_api.route('/')
@base_api.route('/index')
def root():
    ArticlesTable.connect()
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


    ArticlesTable.disconnect()
    return render_template('index.html', articles=articles, current_page=current_page, total_pages=total_pages, page_boundries=page_boundries)

@base_api.app_template_filter()
def timedelta(pub_date):
    delta = datetime.utcnow() - pub_date
    secs = delta.seconds
    days = delta.days

    hours, remainder = divmod(secs, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    days_str = ''
    if days != 0:
        days_str = '{} day'.format(days)
        if days > 1: days_str += 's'
        days_str += ', '

    hours_str = ''
    if hours != 0:
        hours_str = '{} hour'.format(hours)
        if hours > 1: hours_str += 's'
        hours_str += ', '

    minutes_str = ''
    if minutes != 0:
        minutes_str = '{} minute'.format(minutes)
        if minutes > 1: minutes_str += 's'
        minutes_str += ', '

    delta_str = '{}{}{}'.format(days_str, hours_str, minutes_str)
    return delta_str.strip(', ') + ' ago'

@base_api.app_template_filter()
def removetags(text):
    TAG_RE = re.compile(r'<[^>]+>')
    return TAG_RE.sub('', text)