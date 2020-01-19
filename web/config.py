import os

basedir = os.path.abspath(os.path.dirname(__file__))
UNBABEL_DB_HOST = os.getenv('UNBABEL_DB_HOST')
UNBABEL_DB_PORT = os.getenv('UNBABEL_DB_PORT')
UNBABEL_DB_NAME_PROD = os.getenv('UNBABEL_DB_NAME_PROD')
UNBABEL_DB_NAME_DEV = os.getenv('UNBABEL_DB_NAME_DEV')
UNBABEL_DB_NAME_TEST = os.getenv('UNBABEL_DB_NAME_TEST')
UNBABEL_DB_USR = os.getenv('UNBABEL_DB_USR')
UNBABEL_DB_PWD = os.getenv('UNBABEL_DB_PWD')


class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.urandom(32)  # TODO: Update with a proper key
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = \
        f'postgresql://{UNBABEL_DB_USR}:{UNBABEL_DB_PWD}@{UNBABEL_DB_HOST}:{UNBABEL_DB_PORT}/{UNBABEL_DB_NAME_PROD}'
                                              
                                              
class DevelopmentConfig(Config):              
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = \
        f'postgresql://{UNBABEL_DB_USR}:{UNBABEL_DB_PWD}@{UNBABEL_DB_HOST}:{UNBABEL_DB_PORT}/{UNBABEL_DB_NAME_DEV}'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = \
        f'postgresql://{UNBABEL_DB_USR}:{UNBABEL_DB_PWD}@{UNBABEL_DB_HOST}:{UNBABEL_DB_PORT}/{UNBABEL_DB_NAME_TEST}'
