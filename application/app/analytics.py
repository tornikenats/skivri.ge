from datetime import datetime, timedelta

from flask import Blueprint
from flask import request, abort, jsonify
from playhouse.shortcuts import model_to_dict
from app.db.analytics_db import AnalyticsDatabase
from app import settings

analytic_api = Blueprint('analytic_api', __name__)
analytics_db = AnalyticsDatabase()

@analytic_api.before_request
def _db_connect():
    analytics_db.connect()


@analytic_api.teardown_request
def _db_close(exc):
    if not analytics_db.is_closed():
        analytics_db.close()


@analytic_api.route('/a.gif', methods=["GET"])
def report_pageview():
    if not request.args.get('url'):
        abort(404)

    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    url = request.args['url']
    title = request.args.get('t', 'unknown')
    referrer = request.args.get('ref', 'unknown')
    date = datetime.utcnow()
    
    analytics_db.report_pageview(ip, referrer, url, title, date)
    return '', 204


@analytic_api.route('/b.gif', methods=["GET"])
def report_articleview():
    if not request.args.get('id'):
        abort(404)

    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    article_id = request.args['id']
    date = datetime.utcnow()

    analytics_db.report_articleview(ip, article_id, date)
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
    for view in analytics_db.get_pageviews(start_date, end_date):
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
    for view in analytics_db.get_pageviews(start_date, end_date):
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

    article_views = analytics_db.get_articleviews(start_date, end_date)
    article_views = list(map(model_to_dict, article_views))
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
