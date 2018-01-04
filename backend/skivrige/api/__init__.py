from flask import Blueprint, render_template, request, current_app, jsonify
from .views.news import News

api = Blueprint('api', __name__, url_prefix='/api/v1')

api.add_url_rule('/news', view_func=News.as_view('news'))
