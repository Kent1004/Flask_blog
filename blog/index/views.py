from flask import Blueprint, render_template

index = Blueprint('index', __name__, url_prefix='/index')

@index.route('/')
def index_page():
    return 'Hello'