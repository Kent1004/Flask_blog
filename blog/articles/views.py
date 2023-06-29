import requests
from typing import Dict
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from sqlalchemy.orm import joinedload, lazyload
from werkzeug.exceptions import NotFound

from flask_login import login_required, current_user, login_user

from blog.forms.article import CreateArticleForm
from blog.models import Article, Author, Tag
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


@article.route('/', methods=['GET'])
@login_required
def article_list():
    articles: Article = Article.query.all()
    count_articles: Dict = requests.get('http://127.0.0.1:5000/api/articles/event_get_count/').json()
    print(count_articles)
    return render_template('articles/list.html', articles=articles, count_articles = count_articles['count'])


@article.route("/<int:article_id>/", methods=['GET'])
@login_required
def article_detail(article_id):
    _article: Article = Article.query.filter_by(id=article_id).options(joinedload(Article.tags)).one_or_none()
    if _article is None:
        raise NotFound
    return render_template(
        "articles/details.html",
        article=_article,
    )


@article.route('/create', methods=['GET'])
@login_required
def create_article_form():
    form = CreateArticleForm(request.form)
    form.tags.choices = [(tag.id, tag.name) for tag in Tag.query.order_by('name')]
    return render_template('articles/create.html', form=form)


@article.route('/', methods=['POST'])
@login_required
def create_article():
    form = CreateArticleForm(request.form)
    form.tags.choices = [(tag.id, tag.name) for tag in Tag.query.order_by('name')]
    if form.validate_on_submit():
        _article: Article = Article(title=form.title.data.strip(), text=form.text.data)
        if form.tags.data:
            selected_tags = Tag.query.filter(Tag.id.in_(form.tags.data))
            for tag in selected_tags:
                _article.tags.append(tag)

        if current_user.author:
            _article.author_id = current_user.author.id
        else:
            author = Author(user_id=current_user.id)
            db.session.add(author)
            db.session.flush()
            _article.author_id = author.id
        db.session.add(_article)
        db.session.commit()
        return redirect(url_for('article.article_detail', article_id=_article.id))
    return render_template('articles/create.html', form=form)


@article.route('/tag/<int:tag_id>/')
@login_required
def list_by_tags(tag_id):
    _tag: Tag = Tag.query.filter_by(id=tag_id).one_or_none()
    _articles: Article = Article.query.join(Article.tags).filter(Tag.id == tag_id)
    return render_template("articles/list_by_tag.html", tag=_tag, articles=_articles)
