# -*- coding:utf-8 -*-

import os

# 返回py文件的绝对路径
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # SECRET_KEY必须设置，先判断系统变量中有没有SECRET_KEY
    SECRET_KEY = os.environ.get('SECRET_KEY') or '\x03d\xf4\x95J\x15\xa4B\xfb\xc0\xaf \xd1A[j$}\x18\x16a\xe7\xd0\xec'
    # 每次请求结束后都会自动提交数据库中的变动
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    BABEL_DEFAULT_LOCALE = 'zh'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SERVER_NAME = 'localhost:5000'
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
    WTF_CSRF_ENABLED = False


class Production(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'postgresql://vincent:?@localhost/blog-db'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': Production,
    'default': DevelopmentConfig
}
