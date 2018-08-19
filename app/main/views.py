# -*- coding: utf-8 -*-

from flask import render_template, request, flash, redirect, url_for, current_app, abort
from . import main
from .. import db
from ..models import Post, Comment
from flask_login import login_required, current_user
from .forms import CommentForm, PostForm
from flask_babel import gettext as _


# 使用程序实例提供的app.route修饰器，把修饰的函数注册为路由
@main.route('/')
def index():
    # 从request的参数中获取参数page的值，如果参数不存在那么返回默认值1，type=int保证返回的默认值是整型数字
    page_index = request.args.get('page', 1, type=int)

    # 第一个参数表示我们要查询的页数，这里用了上面获取的url的参数；
    # 第二个参数是每页显示的数量，我们这里设置成了1，如果不设置默认显示20条；
    # 第三个参数如果设置成True，当请求的页数超过了总的页数范围，就会返回一个404错误，如果设为False，就会返回一个空列表
    pagination = Post.query.paginate(page_index, per_page=20, error_out=False)
    posts = pagination.items
    return render_template("index.html",
                           title=_(u'欢迎来到Vincent--Gao的博客'),
                           posts=posts,
                           pagination=pagination)


@main.route('/about')
def about():
    return render_template("about.html", title=u'关于')


@main.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    # 对于不存在的条目返回一个404错误
    post = Post.query.get_or_404(id)

    form = CommentForm()

    # 验证用户名和密码
    if form.validate_on_submit():
        comment = Comment(author=current_user,
                          body=form.body.data,
                          post=post)
        db.session.add(comment)
        db.session.commit()

    return render_template('posts/detail.html',
                           title=post.title,
                           form=form,
                           post=post)


@main.route('/edit', methods=['GET', 'POST'])
@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id=0):
    form = PostForm()

    if id == 0:
        post = Post(author=current_user)
    else:
        post = Post.query.get_or_404(id)

    if form.validate_on_submit():
        post.body = form.body.data
        post.title = form.title.data

        db.session.add(post)
        db.session.commit()

        return redirect(url_for('.post', id=post.id))

    form.title.data = post.title
    form.body.data = post.body

    title = _(u'添加新文章')
    if id > 0:
        title = _(u'编辑 - %(title)', title=post.title)

    return render_template('posts/edit.html',
                           title=title,
                           form=form,
                           post=post)


# To shutdown the server you simply make a HTTP request to shutdown.
@main.route('/shutdown')
def shutdown():
    if not current_app.testing:
        abort(404)

    shutdown = request.environ.get('werkzeug.server.shutdown')
    if not shutdown:
        abort(500)

    shutdown()
    return u'正在关闭服务端进程...'
