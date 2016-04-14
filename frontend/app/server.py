from flask import Flask
import logging

server = Flask(__name__, static_url_path='')
if not server.debug:
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    server.logger.addHandler(stream_handler)
    
from .blueprints.base import base_api
from .blueprints.analytics import analytic_api
server.register_blueprint(base_api, url_prefix='')
server.register_blueprint(analytic_api, url_prefix='/analytics')