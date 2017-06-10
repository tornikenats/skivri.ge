from flask import Blueprint, render_template, request, current_app
from playhouse.shortcuts import model_to_dict
from skivrige.helpers.pagination import Pagination
from skivrige.db.news import get_all_articles

main = Blueprint('base_api', __name__)


@main.route('/')
@main.route('/news')
def news():
    language = request.args.get('lang', 'eng')
    try:
        current_page = int(request.args.get('page', 1))
        if current_page < 1:
            raise ValueError()
    except ValueError as e:
        current_page = 1

    all_articles = get_all_articles(language)
    articles = []
    offset = current_app.config['ARTICLES_PER_PAGE'] * (current_page - 1) + 1
    start = (current_page - 1) * current_app.config['ARTICLES_PER_PAGE']
    end = current_page * current_app.config['ARTICLES_PER_PAGE']

    for i, article in enumerate(all_articles[start:end]):
        article_dict = model_to_dict(article)
        article_dict['num'] = offset + i
        articles.append(article_dict)

    pagination = Pagination(current_page, current_app.config['ARTICLES_PER_PAGE'], len(all_articles))

    return render_template('news.html',
                           articles=articles,
                           current_page=current_page,
                           pagination=pagination,
                           language=language
                           )


@main.route('/about')
def about():
    return render_template('about.html')


