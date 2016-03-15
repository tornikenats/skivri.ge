from flask import Flask
import frontend.config as config

server = Flask(__name__, static_url_path='', instance_relative_config=True)
server.config.from_pyfile(config.config_name + '.cfg')

from .blueprints.base import base_api
server.register_blueprint(base_api, url_prefix='')