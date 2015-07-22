#-*-coding:utf-8-*-
#-------------------------------------
# Name: 认证表单模块
# Purpose: 
# Author:
# Date:
#-------------------------------------

from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User 


#登录表单
class LoginForm(Form):
	email = StringField('Email', validators=[Required(), Length(1,64), Email()])
	password = PasswordField('Password', validators=[Required()])
	remember_me = BooleanField('Keep me logged in')
	submit = SubmitField('Log In')

    
#注册表单
class RegistrationForm(Form):
	email = StringField('Email', validators=[Required(), Length(1,64), Email()])
	username = StringField('Username', validators=[Required(), Length(1,64), 
							Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Usernames must have only letters,''numbers, dots or underscores')])
	password = PasswordField('Password', validators=[Required(), EqualTo('password2',message='Passwords must match.')])
	password2 = PasswordField('Confirm password', validators=[Required()])
	submit = SubmitField('Register')
	
	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('Email already registered.')
			
	def validate_username(self, field):
		if User.query.filter_by(username=field.data).first():
			raise ValidationError('Username already in use.')


#更改密码表单
class ChangePasswordForm(Form):
	oldpassword = PasswordField('Old password', validators=[Required()])
	password = PasswordField('New Password', validators=[Required(), EqualTo('password2',message='Passwords must match.')])
	password2 = PasswordField('Confirm password', validators=[Required()])
	submit = SubmitField('Confirm change')


#重设密码表单
class ResetPasswordRequestForm(Form):
	email = StringField('Email', validators=[Required(), Length(1,64), Email()])
	submit = SubmitField('Confirm reset')


#重设密码
class ResetPasswordForm(Form):
	email = StringField('Email', validators=[Required(), Length(1,64), Email()])
	password = PasswordField('New Password', validators=[Required(), EqualTo('password2',message='Passwords must match.')])
	password2 = PasswordField('Confirm password', validators=[Required()])
	submit = SubmitField('Confirm reset')
	
	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first() is None:
			raise ValidationError('Unknown email address.')


#更改邮箱
class ChangeEmailForm(Form):
	email = StringField('New Email', validators=[Required(), Length(1,64), Email()])
	password = PasswordField('Password', validators=[Required()])
	submit = SubmitField('Update Email Address')

	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('Email already registered.')