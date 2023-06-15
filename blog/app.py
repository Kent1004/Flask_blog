import os

from flask import Flask, redirect, url_for
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from . import author
from .models import User, db
from .extensions import db, login_manager, migrate, csrf,admin
from dotenv import load_dotenv
from .config import DevConfig, ProductConfig

load_dotenv()

login_manager = LoginManager()


def create_app() -> Flask:
    app = Flask(__name__)
    # app.config['SECRET_KEY'] = 'Qwerty_123'
    # app.config['SQlALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    cfg_name = os.getenv("CONFIG_NAME") or "ProductConfig"
    app.config.from_object(f"blog.config.{cfg_name}")
    db.init_app(app)
    migrate.init_app(app, db, compare_type=True)
    csrf.init_app(app)
    admin.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @login_manager.unauthorized_handler
    def unauthorized():
        return redirect(url_for('auth.login'))

    register_blueprints(app)
    return app


def register_blueprints(app: Flask):
    from blog.auth.views import auth
    from blog.index.views import index
    from blog.user.views import user
    from blog.report.views import report
    from blog.articles.views import article
    from blog.author.views import author
    from blog import admin

    app.register_blueprint(user)
    app.register_blueprint(report)
    app.register_blueprint(index)
    app.register_blueprint(article)
    app.register_blueprint(auth)
    app.register_blueprint(author)
    admin.register_views()


# def register_commands(app: Flask):
#     app.cli.add_command(commands.create_init_tags)
