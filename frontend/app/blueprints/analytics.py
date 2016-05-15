from flask import Blueprint
from flask import request, abort, jsonify
from model.base_model import mydb
from model.analytics import Users, PageViews
from playhouse.shortcuts import model_to_dict
from datetime import datetime, timedelta
import config

analytic_api = Blueprint('analytic_api', __name__)
mydb.init(config.settings['MYSQL_DB'], max_connections=5, stale_timeout=600, **{'user': config.settings['MYSQL_USER'], 'password': config.settings['MYSQL_PASS'] })
mydb.create_tables([Users, PageViews], safe=True)

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
        "user": user.ip,
        "referrer": referrer,
        "date": datetime.utcnow()
    }
    PageViews.create(**kwargs)
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
    for view in PageViews.select(PageViews.date, PageViews.user)\
                        .where(PageViews.date.between(start_date, end_date)):
        group = view.date.strftime('%B %d, %Y %H:00:00')
        if not group in hourly:
            hourly[group] = 0

        hourly[group] += 1

    return jsonify({"hourly_groups": hourly})


@analytic_api.route('/pageviews', methods=["GET"])
def page_views():
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

    anonymized = {}
    anon_count = 0
    daily = {}
    for view in PageViews.select(PageViews.date, PageViews.user)\
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

    return jsonify({"daily_groups": daily, "user_count": anon_count - 1 })