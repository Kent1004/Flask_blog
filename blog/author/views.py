from flask import Blueprint, render_template

author = Blueprint('author', __name__, url_prefix='/author', static_folder='../static')


@author.route('/')
def author_list():
    from blog.models import Author
    authors = Author.query.all()
    for author in authors:
        print(author.id)
    return render_template(
        'authors/list.html',
        authors=authors,
    )
