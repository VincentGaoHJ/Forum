# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email, Regexp, Length


class LoginForm(Form):
    username = StringField(label=u"用户", validators=[DataRequired()])
    password = PasswordField(label=u"密码", validators=[DataRequired()])
    submit = SubmitField(label=u"提交")


class RegistrationForm(Form):
    # 验证函数 Required() 确保提交的字段不为空
    email = StringField(u'邮箱地址', validators=[DataRequired(),
                                             Length(1, 64),
                                             Email()])
    username = StringField(u'用户名', validators=[DataRequired(),
                                               Length(1, 64),
                                               Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                      u'用户名必须由字母，数字，下划线或者.组成')])
    password = PasswordField(u'密码', validators=[DataRequired(),
                                                EqualTo('password2', message="Passwords must match")])

    password2 = PasswordField(u'确认密码', validators=[DataRequired()])
    submit = SubmitField(u'马上注册')
