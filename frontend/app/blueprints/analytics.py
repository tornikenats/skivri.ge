from flask import Blueprint
from flask import request, abort, jsonify
from model.analytics import Users, PageViews, mydb
from playhouse.shortcuts import model_to_dict
from datetime import datetime
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


@analytic_api.route('/pageviews', methods=["GET"])
def page_views():
    pageviews = []
    for view in PageViews.select(PageViews.date):
        pageviews.append(view.date.strftime('%B %d, %Y %H:%M:%S'))
    return jsonify({'pageviews': pageviews})