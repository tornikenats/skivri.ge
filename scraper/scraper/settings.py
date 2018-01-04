import os
import logging

class Config(object):
    """Base configuration."""

    SECRET_KEY = os.environ.get('APP_SECRET', 'CHANGE')
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    FETCH_WAIT_SECONDS = 60 * 15  # 15 minutes

class ProdConfig(Config):
    """Production configuration."""

    ENV = 'prod'
    DEBUG = False
    LOG_LEVEL = logging.WARNING


class DevConfig(Config):
    """Development configuration."""

    ENV = 'dev'
    DEBUG = True
    LOG_LEVEL = logging.DEBUG
