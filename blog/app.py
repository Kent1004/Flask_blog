from flask import Flask

from index.views import index
from user.views import user
from report.views import report
from article.views import article

def create_app() -> Flask:
    app = Flask(__name__)
    register_blueprints(app)
    return app


def register_blueprints(app: Flask):
    app.register_blueprint(user)
    app.register_blueprint(report)
    app.register_blueprint(index)
    app.register_blueprint(article)
