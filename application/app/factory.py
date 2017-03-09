from flask import Flask
import logging

from app.news import news_api
from app.analytics import analytic_api
from app.settings import settings
from app.trends import trends_api


def create_app():
    app = Flask(__name__, static_url_path='')
    if not app.debug:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        app.logger.addHandler(stream_handler)

    app.register_blueprint(news_api, url_prefix='')
    if not settings['NOANALYTICS']:
        app.register_blueprint(analytic_api, url_prefix='/analytics')
        app.register_blueprint(trends_api, url_prefix='/trends')

    return app