from flask import Blueprint, render_template

main = Blueprint('main', __name__)


@main.route('/')
def root():
    return render_template('index.html')

@main.route('/about')
def about():
    return render_template('about.html')


