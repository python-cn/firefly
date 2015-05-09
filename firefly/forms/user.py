# coding=utf-8
from __future__ import absolute_import
from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import ValidationError, Email, Required

from firefly.models.user import User


class RegisterForm(Form):
    username = StringField('Username', [Required()])
    email = StringField('Email', [Required(), Email()])
    password = PasswordField('Password', [Required()])

    def validate_username(self, field):
        if User.objects.filter(username=field.data):
            raise ValidationError('当前用户名已被注册')

    def validate_email(self, field):
        if User.objects.filter(email=field.data):
            raise ValidationError('当前邮箱已注册')

    def save(self):
        return User.create_user(
            username=self.username.data, email=self.email.data,
            password=self.password.data
        )


class LoginForm(Form):
    email = StringField('Email', [Required(), Email()])
    password = PasswordField('Password', [Required()])

    def validate_password(self, field):
        user = User.objects.filter(
            email=self.email.data, active=True
        ).first()
        if user is not None and user.check_password(field.data):
            self.user = user
        else:
            raise ValidationError('邮箱或密码错误')
