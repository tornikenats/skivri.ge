from flask import Flask, jsonify
from peewee import MySQLDatabase
from skivrige import commands
from skivrige.settings import ProdConfig
from skivrige.main.views import main
from skivrige.helpers.template_filters import timedelta, removetags
from skivrige_model import mydb

def create_app(config_object=ProdConfig):
    app = Flask(__name__, static_url_path='')
    app.config.from_object(config_object)
    initialize_db(app)
    register_extensions(app)
    register_blueprints(app)
    register_filters(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    return app


def initialize_db(app):
    db_name = app.config['MYSQL_DB']
    db_user = app.config['MYSQL_USER']
    db_password = app.config['MYSQL_PASS']
    mydb.initialize(MySQLDatabase(db_name, user=db_user, passwd=db_password))

    @app.before_request
    def before_request(): 
        mydb.connect()
        
    @app.teardown_request
    def after_request(exec): 
        mydb.close()

    return None


def register_blueprints(app):
    app.register_blueprint(main)
    return None

def register_filters(app):
    app.jinja_env.filters['timedelta'] = timedelta
    app.jinja_env.filters['removetags'] = removetags
    return None

def register_extensions(app):
    return None


def register_errorhandlers(app):
    """Register error handlers."""
    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return jsonify({'error': error_code}), error_code
    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None


def register_shellcontext(app):
    """Register shell context objects."""
    def shell_context():
        """Shell context objects."""
        return {
            'db': db,
            'User': user.models.User}

    app.shell_context_processor(shell_context)


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)
    app.cli.add_command(commands.clean)
    app.cli.add_command(commands.urls)