from flask import Blueprint, render_template

article = Blueprint('article', __name__, url_prefix='/article', static_folder='../static')

Articles = ['Mars','Earth','Venera']

@article.route('/')
def article_list():
    return render_template('article/list.html',articles= Articles)

@article.route('/<article_name>')
def article_details(article_name: str):
    return render_template(
        'article/details.html',
        article_name = article_name,
    )
