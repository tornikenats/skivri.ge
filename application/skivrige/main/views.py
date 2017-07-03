from flask import Blueprint, render_template

main = Blueprint('main', __name__)


@main.route('/', defaults={'path': ''})
@main.route('/<path:path>')
def root(path):
    return render_template('index.html')