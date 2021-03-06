#-*-coding:utf-8-*-
#-------------------------------------
# Name: 认证路由模块
# Purpose: 
# Author:
# Date:
#-------------------------------------

from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, logout_user, login_required, current_user
from . import auth
from ..models import User
from .forms import LoginForm, RegistrationForm, ChangePasswordForm, ResetPasswordForm, ResetPasswordRequestForm, ChangeEmailForm
from .. import db
from ..email import send_email 


#针对全局请求的钩子
@auth.before_app_request
def before_request():
	if current_user.is_authenticated():
		current_user.ping()#更新已登录用户的访问时间
		if not current_user.confirmed and request.endpoint[:5] != 'auth.'and request.endpoint != 'static':
			return redirect(url_for('auth.unconfirmed'))


#登录
@auth.route('/login',methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user, form.remember_me.data)
			return redirect(request.args.get('next') or url_for('main.index'))
		flash('Invalid username or password.')
	return render_template('auth/login.html',form=form)

    
#登出
@auth.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You have been logged out.')
	return redirect(url_for('main.index'))


#注册
@auth.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(email=form.email.data, username=form.username.data, password=form.password.data)
		db.session.add(user)
		db.session.commit()
		token = user.generate_confirmation_token()
        
        #发送确认邮件
		send_email(user.email, 'Confirm Your Account','auth/email/confirm', user=user, token=token)
		flash('A confirmation email has been sent to you by email.')
		return redirect(url_for('main.index'))
	return render_template('auth/register.html', form=form)

    
#确认账户
@auth.route('/confirm/<token>')
@login_required
def confirm(token):
	if current_user.confirmed:
		return redirect(url_for('main.index'))
	if current_user.confirm(token):
		flash('You have confirmed your account.Thanks!')
	else:
		flash('The confirmation link is invalid or has expired.')
	return redirect(url_for('main.index'))


#未确认账户
@auth.route('/unconfirmed')
def unconfirmed():
	if current_user.is_anonymous() or current_user.confirmed:
		return redirect(url_for('main.index'))
	return render_template('auth/unconfirmed.html')


#重新发送确认邮件
@auth.route('/confirm')
@login_required
def resend_confirmation():
	token = current_user.generate_confirmation_token()
	send_email(current_user.email,'Confirm Your Account', 'auth/email/confirm', user=current_user, token=token)
	flash('A new confirmation email has been sent to you by email.')
	return redirect(url_for('main.index'))


#更改密码
@auth.route('/change-password',methods=['GET', 'POST'])
@login_required
def change_password():
	form = ChangePasswordForm()
	if form.validate_on_submit():
		if current_user.verify_password(form.oldpassword.data):
			current_user.password = form.password.data
			db.session.add(current_user)
			flash('Password have been changed successfully!')
			return redirect(url_for('main.index'))
		else:
			flash('Invalid password.')
	return render_template('auth/password_change.html', form=form)


#重设密码
@auth.route('/Reset', methods=['GET', 'POST'])
def reset_password_request():
	if not current_user.is_anonymous():
		return redirect(url_for('main.index'))
	form = ResetPasswordRequestForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user:
			token = user.generate_reset_token()
			send_email(user.email, 'Reset Your Password','auth/email/Reset_password', user=user, token=token, next=request.args.get('next'))
			flash('A reset-password-request email has been sent to you by email.')
			return redirect(url_for('auth.login'))
		else:
			flash('Invalid email.')
	return render_template('auth/reset_password.html',form=form)


#重设密码
@auth.route('/Reset/<token>',methods=['GET', 'POST'])
def Reset_password(token):
	if not current_user.is_anonymous():
		return redirect(url_for('main.index'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is None : 
			return redirect(url_for('main.index'))
		if user.reset_password(token, form.password.data):
			flash('Your password has been updated.')
			return redirect(url_for('auth.login'))
		else:
			return redirect(url_for('main.index'))
	return render_template('auth/reset_password.html',form=form)


#更改邮箱
@auth.route('/change-email', methods=['GET', 'POST'])
@login_required
def change_email_request():
	form = ChangeEmailForm()
	if form.validate_on_submit():
		if current_user.verify_password(form.password.data):
			new_email = form.email.data
			token = current_user.generate_email_change_token(new_email)
			send_email(new_email, 'Confirm your email address',
						'auth/email/change_email',
						user=current_user, token=token)
			flash('An email with instructions to confirm your new email '
					'address has been sent to you.')
			return redirect(url_for('main.index'))
		else:
			flash('Invalid email or password.')
	return render_template("auth/change_email.html", form=form)


#更改邮箱
@auth.route('/change-email/<token>')
@login_required
def change_email(token):
	if current_user.change_email(token):
		flash('Your email address has been updated.')
	else:
		flash('Invalid request.')
	return redirect(url_for('main.index'))
