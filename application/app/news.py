from datetime import datetime
import re
from flask import Blueprint
from flask import render_template, request
from playhouse.shortcuts import model_to_dict
from app.helpers.pagination import Pagination
from app import settings

if settings.settings['NODB']:
    from app.db.news_db import NewsDatabaseMock as NewsDatabase
else:
    from app.db.news_db import NewsDatabase

ARTICLES_PER_PAGE = 20

news_api = Blueprint('base_api', __name__)
news_db = NewsDatabase()

@news_api.before_request
def _db_connect():
    news_db.connect()


@news_api.teardown_request
def _db_close(exc):
    if not news_db.is_closed():
        news_db.close()


@news_api.route('/')
@news_api.route('/news')
def news():
    language = request.args.get('lang', 'eng')
    try:
        current_page = int(request.args.get('page', 1))
        if current_page < 1:
            raise ValueError()
    except ValueError as e:
        current_page = 1

    all_articles = news_db.get_all_articles(language)
    articles = []
    offset = ARTICLES_PER_PAGE * (current_page - 1) + 1
    start = (current_page - 1) * ARTICLES_PER_PAGE
    end = current_page * ARTICLES_PER_PAGE

    for i, article in enumerate(all_articles[start:end]):
        article_dict = model_to_dict(article)
        article_dict['views'] = article.count
        article_dict['num'] = offset + i
        articles.append(article_dict)

    pagination = Pagination(current_page, ARTICLES_PER_PAGE, len(all_articles))

    return render_template('news.html',
                           articles=articles,
                           current_page=current_page,
                           pagination=pagination,
                           language=language
                           )


@news_api.route('/stats')
def stats():
    return render_template('stats.html')


@news_api.route('/trends')
def trends():
    return render_template('trends.html')


@news_api.route('/about')
def about():
    return render_template('about.html')


@news_api.app_template_filter()
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
    else:
        minutes_str = 'seconds'

    delta_str = '{}{}{}'.format(days_str, hours_str, minutes_str)
    return delta_str.strip(', ') + ' ago'


@news_api.app_template_filter()
def removetags(text):
    TAG_RE = re.compile(r'<[^>]+>')
    return TAG_RE.sub('', text)
