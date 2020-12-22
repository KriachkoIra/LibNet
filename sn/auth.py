from flask_sqlalchemy import SQLAlchemy
from db import User
import functools
from datetime import datetime
from app import app, db
from werkzeug.security import check_password_hash, generate_password_hash
from validate_email import validate_email

from flask import (
	Blueprint, flash, g, redirect, render_template, request, session, url_for
)

@app.route('/register', methods=('GET', 'POST'))
def register():
	if request.method == 'POST':
		username = request.form['username']
		name = request.form['name']
		u_birth_date = request.form['birth_date']
		u_birth_date = u_birth_date[2:len(u_birth_date)]
		birth_date = datetime.strptime(u_birth_date, '%y-%m-%d')
		email = request.form['email']
		password = request.form['password']
		pass_copy = password
		password = generate_password_hash(password)
		error = None

		avatar = None
		if request.files:
			avatar = request.files['cropped_image']
			print(avatar)
		
		username_registered = User.query.filter_by(username=username)
		email_registered = User.query.filter_by(email=email)

		if not name or not username or not birth_date or not password:
			error = 'Порожня форма.'

		elif username_registered.first() is not None:
			error = 'Користувач {} вже зареєстрований.'.format(username)

		elif email_registered.first() is not None:
			error = 'Адреса {} вже зареєстрована.'.format(email)

		elif len(pass_copy) < 6:
			error = 'Пароль повинен мати щонайменше 6 символів.'

		
		if error is None:
			user = User(username = username, name = name, birth_date = birth_date, email = email, password = password)
			db.session.add(user)
			db.session.commit()
			if avatar:
				s = "avatars/" + str(user.id)
				storage.child(s).put(avatar)
				av_url = storage.child(s).get_url(1)
				user.avatar = av_url
				db.session.commit()
			return redirect(url_for('login'))
		
		flash(error)

	return render_template('register.html')


@app.route('/login', methods=('GET', 'POST'))
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']

		error = None

		user = User.query.filter_by(username=username).first()

		if user is None:
			error = 'Некоректний нікнейм.'
		elif not check_password_hash(user.password, password):
			error = 'Некоректний пароль.'

		if error is None:
			session.clear()
			session['user_id'] = user.id
			return redirect(url_for('index'))

		flash(error)

	return render_template('login.html')

@app.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('login'))