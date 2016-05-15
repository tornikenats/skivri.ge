from flask import Blueprint
from flask import request, abort, jsonify
from model.base_model import mydb
from model.trends import WordOccurences
from playhouse.shortcuts import model_to_dict
from datetime import datetime, timedelta
import config

trends_api = Blueprint('trends_api', __name__)
mydb.init(config.settings['MYSQL_DB'], max_connections=5, stale_timeout=600, **{'user': config.settings['MYSQL_USER'], 'password': config.settings['MYSQL_PASS'] })
mydb.create_tables([WordOccurences], safe=True)

@trends_api.before_request
def _db_connect():
    mydb.connect()

@trends_api.teardown_request
def _db_close(exc):
    if not mydb.is_closed():
        mydb.close()

@trends_api.route('/stats')
def stats():
    if 'start-date' not in request.args or 'end-date' not in request.args:
        return jsonify(exception="must specify the start-date and end-date")

    start_date = request.args['start-date']
    end_date = request.args['end-date']
    try:
        limit = min(int(request.args.get('limit', 20)), 100)
    except ValueError:
        limit = 20

    start_date = datetime.strptime(start_date, '%Y-%m-%d-%H-%M')
    end_date = datetime.strptime(end_date, '%Y-%m-%d-%H-%M')

    if end_date - start_date > timedelta(days=14):
        return jsonify(exception="periods larger than 2 weeks are not supported")

    # call db and get word, count pairs
    trends = []
    for word_occurence in WordOccurences.select(WordOccurences.word, WordOccurences.count)\
            .where(WordOccurences.date.between(start_date,end_date)).limit(limit):
        trends.append((word_occurence.word, word_occurence.count))

    return jsonify({'trends': trends})
