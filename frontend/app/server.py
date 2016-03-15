from flask import Flask

server = Flask(__name__, static_url_path='')

from .blueprints.base import base_api
server.register_blueprint(base_api, url_prefix='')