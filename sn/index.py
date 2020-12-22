from flask_sqlalchemy import SQLAlchemy
from db import *
import functools
from datetime import datetime, date
from app import app, db, storage
from sqlalchemy import func

from flask import (
	Blueprint, flash, g, redirect, render_template, request, session, url_for
)

def get_user():
	user_id = session.get('user_id')

	if user_id is None:
		g.user = None
	else:
		g.user = User.query.filter_by(id=user_id).first()
	return g.user


@app.route('/')
def index():
	get_user()
	return render_template('index.html')


@app.route('/books', methods=('GET', 'POST'))
def books():
	get_user()
	if g.user is not None:
		b = Book.query.filter_by(owner_id=g.user.id)
		print(b.all())
		read = b.filter_by(status="1")
		will_read = b.filter_by(status="2")
		reading = b.filter_by(status="3")
	return render_template('books.html', will_read = will_read, read=read, reading=reading)


@app.route('/add_book', methods=('GET', 'POST'))
def add_book():
	get_user()

	if request.method == 'POST':
		name = request.form['name']
		author = request.form['author']
		genre = request.form['genre']
		status = request.form['status']
		rating = request.form.get("star")

		image = None

		if request.files:
			image = request.files['image']
			print(image)

		error = None
		if(rating == None):
			rating = "0"

		book = Book.query.filter_by(owner_id=g.user.id).filter_by(name=name).first()

		if g.user is None:
			error = 'Зайдіть на свій аккаунт, щоб додати книгу.'

		elif not name or not status:
			error = 'Empty form.'

		elif book is not None:
			error = 'Книга "{}" вже зареєстрована.'.format(name)

		if error is None:
			cur_book = Book(name = name, owner_id=g.user.id, status=status, rating=rating, author=author, genre=genre)
			db.session.add(cur_book)
			db.session.commit()
			if image:
				s = "images/" + str(cur_book.id)
				storage.child(s).put(image)
				i_url = storage.child(s).get_url(1)
				cur_book.image = i_url
				db.session.commit()
			return redirect(url_for('books'))
		
		flash(error)	

	return render_template('add_book.html')


@app.route('/<int:id>/book', methods=('GET', 'POST'))
def book(id):
	get_user()
	book = Book.query.filter_by(id = id).first()
	quotes = Quote.query.filter_by(book_id=book.id)

	author = book.author

	if request.method == 'POST':
		quote_text = request.form['quote_text']
		quote = Quote(book_id=book.id, text=quote_text)
		db.session.add(quote)
		db.session.commit()
		return redirect(url_for('book', id=id))

	return render_template('book.html', quotes=quotes, author=book.author, name=book.name, genre=book.genre, rating=book.rating, image=book.image, book=book)

@app.route('/<int:id>/delete_quote', methods=('GET', 'POST'))
def delete_quote(id):
	get_user()

	if request.method == 'POST':
		q_id = request.form.get("q_id")
		cur_quote = Quote.query.filter_by(id=q_id).first()
		
		db.session.delete(cur_quote)
		db.session.commit()
		return redirect(url_for('book', id=id))

	return redirect(url_for('book', id=id))


@app.route('/add_post', methods=('GET', 'POST'))
def add_post():
	get_user()

	if request.method == 'POST':
		title = request.form['title']
		body = request.form['body']

		dn = datetime.now()
		dn = str(dn)
		date = dn[8:10] + '.' + dn[5:7] + '.' + dn[0:4] + ' ' + dn[11:13] + ':' + dn[14:16]

		post = Post(author_id=g.user.id, title=title, body=body, date=date)
		db.session.add(post)
		db.session.commit()

		return redirect(url_for('posts'))

	return render_template('add_post.html')


@app.route('/posts', methods=('GET', 'POST'))
def posts():
	get_user()
	p = None
	if g.user is not None:
		p = Post.query.filter_by(author_id=g.user.id)
		print(p.all())

	return render_template('posts.html', posts=p)


@app.route('/<int:id>/delete_post', methods=('GET', 'POST'))
def delete_post(id):
	get_user()

	if request.method == 'POST':
		p_id = request.form.get("p_id")
		cur_post = Post.query.filter_by(id=p_id).first()
		
		db.session.delete(cur_post)
		db.session.commit()
		return redirect(url_for('posts'))

	return redirect(url_for('posts'))

@app.route('/my_profile', methods=('GET', 'POST'))
def my_profile():
	get_user()
	n = Post.query.filter_by(author_id=g.user.id).count()
	f_books = Book.query.filter_by(owner_id=g.user.id).filter_by(is_favorite=True).all()

	return render_template('user_page.html', n_posts=n, books=f_books)

@app.route('/upload_image', methods=('GET', 'POST'))
def upload_image():
	get_user()

	if request.method == 'POST':
		avatar = None
		
		if request.files:
			avatar = request.files['cropped_image']
			print(avatar)

		if avatar:
				s = "avatars/" + str(g.user.id)
				storage.child(s).put(avatar)
				av_url = storage.child(s).get_url(1)
				g.user.avatar = av_url
				db.session.commit()

		return redirect(url_for('my_profile'))

	return redirect(url_for('my_profile'))


@app.route('/<int:id>/delete_book', methods=('GET', 'POST'))
def delete_book(id):
	get_user()

	if request.method == 'POST':
		b_id = request.form.get("b_id")
		print(b_id)

		cur_book = Book.query.filter_by(id=b_id).first()
		print(b_id, cur_book.name)
		db.session.delete(cur_book)
		db.session.commit()

	return redirect(url_for('books'))

@app.route('/<int:id>/add_book_to_favorites', methods=('GET', 'POST'))
def add_book_to_favorites(id):
	get_user()

	if request.method == 'POST':
		b_id = request.form.get("b_id")

		cur_book = Book.query.filter_by(id=b_id).first()
		if cur_book.is_favorite == True:
			cur_book.is_favorite = False
		else:
			cur_book.is_favorite = True
		db.session.commit()
		return redirect(url_for('book', id=cur_book.id))

	return redirect(url_for('book', id=cur_book.id))

@app.route('/<int:id>/add_quote_to_favorites', methods=('GET', 'POST'))
def add_quote_to_favorites(id):
	get_user()

	if request.method == 'POST':
		q_id = request.form.get("q_id")

		cur_quote = Quote.query.filter_by(id=q_id).first()
		if cur_quote.is_favorite == True:
			cur_quote.is_favorite = False
		else:
			cur_quote.is_favorite = True
		db.session.commit()
		return redirect(url_for('book', id=cur_quote.book_id))

	return redirect(url_for('book', id=cur_quote.book_id))