from datetime import datetime, timedelta

from flask import Blueprint
from flask import request, jsonify
from model.base_model import mydb
from model.trends import WordOccurences

from app import settings

trends_api = Blueprint('trends_api', __name__)

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
