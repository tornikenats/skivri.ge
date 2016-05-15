from flask import Flask
import logging

server = Flask(__name__, static_url_path='')
if not server.debug:
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    server.logger.addHandler(stream_handler)
    
from .blueprints.main import main_api
from .blueprints.analytics import analytic_api
from .blueprints.trends import trends_api
server.register_blueprint(main_api, url_prefix='')
server.register_blueprint(analytic_api, url_prefix='/analytics')
server.register_blueprint(trends_api, url_prefix='/trends')