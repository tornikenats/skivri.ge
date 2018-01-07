import os, sys
import datetime
import logging 
import sys
import time
from scraper.extensions import mongo
from pymongo import DESCENDING
from scraper.app import App


def create_app(config_object):    
    app = App()
    app.config.from_object(config_object)
    
    init_logger(app)
    init_db(app)
    
    return app


def init_db(app):
    mongo.init_app(app)

    # initialize unique index
    if 'articles' not in mongo.db.collection_names():
        articles = mongo.db.articles
        articles.create_index(
            [('title', DESCENDING)],
            unique=True
        )


def init_logger(app):
    logging.basicConfig(
        format='%(asctime)s | %(levelname)s | %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p',
        stream=sys.stdout, 
        level=app.config['LOG_LEVEL'])