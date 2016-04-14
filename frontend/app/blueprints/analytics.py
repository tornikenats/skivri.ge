from flask import Blueprint
from flask import request, abort
import model.analytics as analytics
import config

analytic_api = Blueprint('analytic_api', __name__)

PageViewTable, UserTable = analytics.initialize(config.settings['MYSQL_DB'], config.settings['MYSQL_USER'], config.settings['MYSQL_PASS'])

@analytic_api.route('/a.gif', methods=["GET"])
def pageview():
    if not request.args.get('url'):
        abort(404)

    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    url = request.args['url']
    title = request.args.get('t', 'unknown')
    referrer = request.args.get('ref', 'unknown')
    user, created = UserTable.get_or_create(ip=ip)
    PageViewTable.create(url=url, title=title, user=user.ip, referrer=referrer)
    return '', 204

