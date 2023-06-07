from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from werkzeug.exceptions import NotFound

from flask_login import login_required, current_user, login_user

from blog.forms.article import CreateArticleForm
from blog.models import Article, Author
from blog.user.views import get_user_name
from blog.extensions import db
from blog.forms.auth import UserAuthForm

article = Blueprint('article', __name__, url_prefix='/articles', static_folder='../static')

# Articles = ['Mars','Earth','Venera']

# ARTICLES = {
#     1: {
#         "title": "Time for time",
#         "text": "many texts",
#         "author": 2
#     },
#     2: {
#         "title": "Time for relax",
#         "text": "more texts",
#         "author": 2
#     },
#     3: {
#         "title": "Cry In floor",
#         "text": "not many texts",
#         "author": 1
#     },
#     4: {
#         "title": "Crying floor",
#         "text": "fantasy is end",
#         "author": 3
#     }
# }


@article.route('/',methods = ['GET'])
@login_required
def article_list():
    articles: Article = Article.query.all()
    return render_template('articles/list.html', articles=articles)


@article.route("/<int:article_id>/",methods=['GET'])
@login_required
def article_detail(article_id):
    _article: Article = Article.query.filter_by(id = article_id).one_or_none()
    if _article is None:
        raise NotFound
    return render_template(
        "articles/details.html",
        article = _article,
    )

@article.route('/create', methods = ['GET'])
@login_required
def create_article_form():
    form = CreateArticleForm(request.form)
    return render_template('articles/create.html', form=form)

@article.route('/', methods = ['POST'])
@login_required
def create_article():
    form = CreateArticleForm(request.form)
    if form.validate_on_submit():
        _article: Article = Article(title = form.title.data.strip(), text= form.text.data)

        if current_user.author:
            _article.author_id = current_user.author.id
        else:
            author = Author(user_id=current_user.id)
            db.session.add(author)
            db.session.flush()
            _article.author_id = author.id
        db.session.add(_article)
        db.session.commit()
        return redirect(url_for('article.article_detail',article_id= _article.id))
    return render_template('articles/create.html', form = form)