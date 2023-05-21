from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from index.views import index
from user.views import user
from report.views import report
from article.views import article

db = SQLAlchemy()

def create_app() -> Flask:
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Qwerty_123'
    app.config['SQlALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    db.init.app(app)

    register_blueprints(app)
    return app


def register_blueprints(app: Flask):
    app.register_blueprint(user)
    app.register_blueprint(report)
    app.register_blueprint(index)
    app.register_blueprint(article)


