from flask import Blueprint
from flask import request, abort, jsonify
import model.analytics as analytics
from playhouse.shortcuts import model_to_dict
import config

analytic_api = Blueprint('analytic_api', __name__)

PageViewTable, UserTable = analytics.initialize(config.settings['MYSQL_DB'], config.settings['MYSQL_USER'], config.settings['MYSQL_PASS'])


@analytic_api.route('/a.gif', methods=["GET"])
def report_pageview():
    if not request.args.get('url'):
        abort(404)

    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    url = request.args['url']
    title = request.args.get('t', 'unknown')
    referrer = request.args.get('ref', 'unknown')

    PageViewTable.connect()
    UserTable.connect()
    user, created = UserTable.get_or_create(ip=ip)
    UserTable.disconnect()
    PageViewTable.create(url=url, title=title, user=user.ip, referrer=referrer)
    PageViewTable.disconnect()
    return '', 204


@analytic_api.route('/pageviews', methods=["GET"])
def page_views():
    pageviews = []
    PageViewTable.connect()
    for view in PageViewTable.select(PageViewTable.date):
        pageviews.append(view.date.strftime('%B %d, %Y %H:%M:%S'))
    return jsonify({'pageviews': pageviews})