# -*- coding: utf-8 -*-

from flask import Flask, request
from os import path
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_pagedown import PageDown
from flask_gravatar import Gravatar
from flask_babel import Babel, gettext as _
from config import config

basedir = path.abspath(path.dirname(__file__))

babel = Babel()

# 这么做是为了解决app.py和models.py关于db的循环引用，将db独立出来之后分别被引用
db = SQLAlchemy()
pagedown = PageDown()
bootstrap = Bootstrap()
login_manager = LoginManager()

# one,'basic','strong'以提供不同的安全等级,一般设置strong,如果发现异常会登出用户
login_manager.session_protection = 'strong'

# 未登录访问鉴权页面时，重新定向到登录页面
login_manager.login_view = 'auth.login'


def create_app(config_name='default'):

    # app是Flask的实例，它接收包或者模块的名字作为参数
    app = Flask(__name__)

    # 默认的模式是development，除此之外还有testing & production
    app.config.from_object(config[config_name])

    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)

    babel.init_app(app)
    Gravatar(app, size=64)

    from .auth import auth as auth_blueprint
    from .main import main as main_blueprint

    app.register_blueprint(auth_blueprint, url_perfix='/auth')
    app.register_blueprint(main_blueprint, static_folder='static')

    @app.template_test('current_link')
    def is_current_link(link):
        return link == request.path

    @babel.localeselector
    def get_locale():
        return current_user.locale

    return app
