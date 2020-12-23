from flask_sqlalchemy import SQLAlchemy
from app import db
from datetime import datetime

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), nullable=False, unique = True)
	name = db.Column(db.String(80), nullable=False)
	birth_date = db.Column(db.DateTime, nullable=False)
	email = db.Column(db.String(80), unique=True, nullable=False)
	password = db.Column(db.String(80), nullable=False)	
	avatar = db.Column(db.String(100))

class Book(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	owner = db.relationship('User',  foreign_keys = "Book.owner_id")
	name = db.Column(db.String(80), nullable=False)
	author = db.Column(db.String(80))
	genre = db.Column(db.String(80))
	status = db.Column(db.String(3), nullable=False)
	rating = db.Column(db.String(3))
	image = db.Column(db.String(100))
	is_favorite = db.Column(db.Boolean, default=False)

class Quote(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
	book = db.relationship('Book',  foreign_keys = "Quote.book_id")
	text = db.Column(db.String(1005)) 
	is_favorite = db.Column(db.Boolean, default=False)

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	author = db.relationship('User',  foreign_keys = "Post.author_id")
	title = db.Column(db.String(80), nullable=False)
	body = db.Column(db.Text, nullable=False)
	date = db.Column(db.String(80), nullable=False)
	likes = db.Column(db.String(100))
	is_favorite = db.Column(db.Boolean, default=False)

class Like(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	user = db.relationship('User',  foreign_keys = "Like.user_id")
	post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
	post = db.relationship('Post',  foreign_keys = "Like.post_id")

class Post_Image(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
	post = db.relationship('Post',  foreign_keys = "Post_Image.post_id")

class Favorite_Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	user = db.relationship('User',  foreign_keys = "Favorite_Post.user_id")
	post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
	post = db.relationship('Post',  foreign_keys = "Favorite_Post.post_id")
	
if __name__ == '__main__':
	db.create_all()
	print("database created")