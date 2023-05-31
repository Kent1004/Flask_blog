import os


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "Qwerty_123"


class ProductConfig(BaseConfig):
    Debug = False
class DevConfig(BaseConfig):
    DEBUG = True



class TestingConfig(BaseConfig):
    TESTING = True


