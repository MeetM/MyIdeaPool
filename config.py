import os
from datetime import timedelta


class BaseConfig(object):
    PROPAGATE_EXCEPTIONS = True
    JWT_PROPAGATE_EXCEPTIONS = True
    JWT_TOKEN_LOCATION = ['headers', 'json']  # json for delete access-token op
    JWT_HEADER_NAME = "X-Access-Token"
    JWT_HEADER_TYPE = ""  # Defaults to Bearer type ("Bearer <JWT>") if not marked empty
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=10)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    JWT_ALGORITHM = 'HS256'
    _MYSQL_DRIVER = "mysql+pymysql://"


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    SECRET_KEY = "super-secret"
    REDIS_URL = "localhost"
    MYSQL_USERNAME = "root"
    MYSQL_PASSWORD = "password"
    MYSQL_ENDPOINT = "localhost"
    MYSQL_DBNAME = "myideapooldev"
    SQLALCHEMY_DATABASE_URI = BaseConfig._MYSQL_DRIVER + MYSQL_USERNAME + ":" + MYSQL_PASSWORD + "@" + MYSQL_ENDPOINT + "/" + MYSQL_DBNAME


class ProdConfig(BaseConfig):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
    REDIS_URL = os.getenv('REDIS_URL')
    MYSQL_USERNAME = os.getenv('MYSQL_USERNAME', 'invalid')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'invalid')
    MYSQL_ENDPOINT = os.getenv('MYSQL_ENDPOINT', 'invalid')
    MYSQL_DBNAME = "myideapool"
    SQLALCHEMY_DATABASE_URI = BaseConfig._MYSQL_DRIVER + MYSQL_USERNAME + ":" + MYSQL_PASSWORD + "@" + MYSQL_ENDPOINT + "/" + MYSQL_DBNAME


def get_config():
    config_name = os.getenv('FLASK_CONFIGURATION', 'prod')
    print(config_name)
    if config_name == 'dev':
        return DevelopmentConfig
    else:
        return ProdConfig
