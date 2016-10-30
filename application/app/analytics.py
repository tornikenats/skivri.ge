from datetime import datetime, timedelta

from flask import Blueprint
from flask import request, abort, jsonify
from model.analytics import Users, PageViews, ArticleViews
from model.articles import Articles
from model.base_model import mydb
from peewee import fn

from app import settings

analytic_api = Blueprint('analytic_api', __name__)
mydb.init(settings.settings['MYSQL_DB'], max_connections=5, stale_timeout=600,
          **{'user': settings.settings['MYSQL_USER'], 'password': settings.settings['MYSQL_PASS']})
mydb.create_tables([Users, PageViews, ArticleViews], safe=True)


@analytic_api.before_request
def _db_connect():
    mydb.connect()


@analytic_api.teardown_request
def _db_close(exc):
    if not mydb.is_closed():
        mydb.close()


@analytic_api.route('/a.gif', methods=["GET"])
def report_pageview():
    if not request.args.get('url'):
        abort(404)

    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    url = request.args['url']
    title = request.args.get('t', 'unknown')
    referrer = request.args.get('ref', 'unknown')

    user, created = Users.get_or_create(ip=ip)
    kwargs = {
        "title": title,
        "url": url,
        "user": user.id,
        "referrer": referrer,
        "date": datetime.utcnow()
    }
    PageViews.create(**kwargs)
    return '', 204


@analytic_api.route('/b.gif', methods=["GET"])
def report_articleview():
    if not request.args.get('id'):
        abort(404)

    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    id = request.args['id']

    user, created = Users.get_or_create(ip=ip)
    try:
        article = Articles.get(id=id)
    except Articles.DoesNotExist:
        return '', 204

    kwargs = {
        "user": user.id,
        "article": article.id,
        "date": datetime.utcnow()
    }

    ArticleViews.create(**kwargs)
    return '', 204


@analytic_api.route('/pageviewshourly', methods=["GET"])
def page_views_hourly():
    if 'start-date' not in request.args or 'end-date' not in request.args:
        return jsonify(exception="must specify the start-date and end-date")

    start_date = request.args['start-date']
    end_date = request.args['end-date']

    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    if end_date == 'newest':
        end_date = datetime.utcnow()
    else:
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

    if end_date - start_date > timedelta(days=31):
        return jsonify(exception="time range is too large")

    hourly = {}
    for view in PageViews.select(PageViews.date, PageViews.user) \
            .where(PageViews.date.between(start_date, end_date)):
        group = view.date.strftime('%B %d, %Y %H:00:00')
        if not group in hourly:
            hourly[group] = 0

        hourly[group] += 1

    return jsonify({"hourly_groups": hourly})


@analytic_api.route('/pageviews', methods=["GET"])
def page_views():
    start_date, end_date = validate_date(request)

    anonymized = {}
    anon_count = 0
    daily = {}
    for view in PageViews.select(PageViews.date, PageViews.user) \
            .where(PageViews.date.between(start_date, end_date)):
        # anonymize
        if not view.user_id in anonymized:
            anonymized_user_id = anon_count
            anonymized[view.user_id] = anonymized_user_id
            anon_count += 1
        else:
            anonymized_user_id = anonymized[view.user_id]

        group = view.date.strftime('%B %d, %Y')
        if not group in daily:
            daily[group] = {}

        if not anonymized_user_id in daily[group]:
            daily[group][anonymized_user_id] = 0

        daily[group][anonymized_user_id] += 1

    return jsonify({"daily_groups": daily, "user_count": anon_count - 1})


@analytic_api.route('/articleviews', methods=["GET"])
def article_views():
    start_date, end_date = validate_date(request)

    article_views = ArticleViews.select(ArticleViews.title, fn.Count(ArticleViews.title).alias("num_views"))
    for views in article_views:
        print("{}{}".format(article_views.title, article_views.num_views))
    # count distinct article titles
    # return (title, #views)

    article_views = ArticleViews.select(ArticleViews.title, ArticleViews.date) \
        .where(ArticleViews.date.between(start_date, end_date))
    return jsonify({"article_views": article_views})


def validate_date(request):
    if 'start-date' not in request.args or 'end-date' not in request.args:
        return jsonify(exception="must specify the start-date and end-date")

    start_date = request.args['start-date']
    end_date = request.args['end-date']

    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    if end_date == 'newest':
        end_date = datetime.utcnow()
    else:
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

    if end_date - start_date > timedelta(days=31):
        return jsonify(exception="time range is too large")

    return (start_date, end_date)
