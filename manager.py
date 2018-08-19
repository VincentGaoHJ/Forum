# -*- coding:utf-8 -*-

from flask_script import Manager, Shell
from app import create_app, db
from app.models import User, Role, Post, Comment
from flask_migrate import Migrate, MigrateCommand, upgrade

app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)


# 每次启动shell会话都要导入数据库实例和模型，为了避免这一个繁琐工作，可以为shell注册一个make_context回调函数
def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


# 只要我们的文件有所变化，服务器会刷新浏览器
@manager.command
def dev():
    from livereload import Server
    live_server = Server(app.wsgi_app)
    live_server.watch('**/*.*')
    live_server.serve(open_url_delay=True)


@manager.command
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


# To sync the database in another system just refresh the migrations
# folder from source control and run the upgrade command.
@manager.command
def deploy():
    upgrade()
    Role.seed()


# 生成大量虚拟实验数据
@manager.command
def forged():
    from forgery_py import basic, lorem_ipsum, internet, date
    from random import randint

    db.drop_all()
    db.create_all()

    Role.seed()

    guests = Role.query.first()

    def generate_comment(func_author, func_post):
        return Comment(body=lorem_ipsum.paragraphs(),
                       created=date.date(past=True),
                       author=func_author(),
                       post=func_post())

    def generate_post(func_author):
        return Post(title=lorem_ipsum.title(),
                    body=lorem_ipsum.paragraphs(),
                    created=date.date(),
                    author=func_author())

    def generate_user():
        return User(name=internet.domain_name(),
                    email=internet.email_address(),
                    password=basic.text(6, at_least=6, spaces=False),
                    role=guests)

    # 生成用户列表
    users = [generate_user() for i in range(0, 5)]
    db.session.add_all(users)

    # 随机选择用户
    def random_user():
        return users[randint(0, 4)]

    # 为随机选择的用户生成一篇文章
    posts = [generate_post(random_user) for i in range(0, randint(50, 200))]

    db.session.add_all(posts)

    # 随机选择文章
    def random_post():
        return posts[randint(0, len(posts) - 1)]

    # 选择随机的文章和用户生成评论
    comments = [generate_comment(random_user, random_post) for i in range(0, randint(2, 100))]

    db.session.add_all(comments)

    db.session.commit()


if __name__ == '__main__':
    manager.run()
#    app.run(DEBUG=True)
