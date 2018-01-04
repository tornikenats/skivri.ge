import os

class Config(object):
    """Base configuration."""

    SECRET_KEY = os.environ.get('APP_SECRET', 'SET IN DOCKER ENV')
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'SET IN DOCKER ENV')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'SET IN DOCKER ENV')
    MYSQL_USER = os.environ.get('MYSQL_USER', 'SET IN DOCKER ENV')
    MYSQL_PASS = os.environ.get('MYSQL_PASS', 'SET IN DOCKER ENV')    
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    ARTICLES_PER_PAGE = 20

class ProdConfig(Config):
    """Production configuration."""

    ENV = 'prod'
    DEBUG = False


class DevConfig(Config):
    """Development configuration."""

    ENV = 'dev'
    DEBUG = True


class TestConfig(Config):
    """Test configuration."""

    TESTING = True
    DEBUG = True