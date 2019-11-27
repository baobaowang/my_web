import os

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
class BaseConfig(object):
    SECRET_KEY = os.getenv('SECRET_KEY','secret string')
    SQLALCHEMY_TRACK_MODIFICATIONS   = False
    BLUELOG_POST_PER_PAGE = 15

class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:////'+os.path.join(basedir,'data-dev.db')

class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:////:memory:'

class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI','sqlite:////'+os.path.join(basedir,'data.db'))

config = {
    'development':DevelopmentConfig,
    'testing':TestingConfig,
    'production':ProductionConfig
}

