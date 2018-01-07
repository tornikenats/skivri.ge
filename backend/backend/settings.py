import os

class Config(object):
    """Base configuration."""

    SECRET_KEY = os.environ.get('APP_SECRET', 'SET IN DOCKER ENV')
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    MONGO_DBNAME = 'news'
    ARTICLES_PER_PAGE = 20

class ProdConfig(Config):
    """Production configuration."""

    ENV = 'prod'
    DEBUG = False
    MONGO_HOST = 'mongodb'


class DevConfig(Config):
    """Development configuration."""

    ENV = 'dev'
    DEBUG = True
    MONGO_HOST = 'localhost'


class TestConfig(Config):
    """Test configuration."""

    TESTING = True
    DEBUG = True