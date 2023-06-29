from flask import Blueprint, render_template

index = Blueprint('index', __name__, url_prefix='/')


@index.route('/')
def index_page():
    return render_template('base.html')
