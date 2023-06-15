from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime

from blog.extensions import db

article_tag_associations_table = Table(
    'article_tag_associations',
    db.metadata,
    db.Column('article_id', db.Integer, ForeignKey('articles.id'), nullable=False),
    db.Column('tag_id', db.Integer, ForeignKey('tags.id'), nullable=False),
)


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    admin = db.Column(db.Boolean, default=False)
    author = relationship('Author', uselist=False, back_populates='user')

    def __init__(self, email, first_name, last_name, password):
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name

    def __str__(self):
        return self.user.email


class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates='author')
    articles = relationship('Article', back_populates='author')

    def __str__(self):
        return self.user.name


class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, ForeignKey('authors.id'), nullable=False)
    title = db.Column(db.String(255))
    text = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    author = relationship('Author', back_populates='articles')
    tags = relationship('Tag', secondary=article_tag_associations_table, back_populates='articles')

    def __str__(self):
        return self.title


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    articles = relationship('Article', secondary=article_tag_associations_table, back_populates='tags')

    def __str__(self):
        return self.name
