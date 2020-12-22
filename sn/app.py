import os
import pyrebase
from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy

config = {
    "apiKey": "AIzaSyDYa_v871QA83ZawAtDqBzAoPtNVN2gWHw",
    "authDomain": "libnet-91669.firebaseapp.com",
    "databaseURL": "https://libnet-91669.firebaseio.com",
    "projectId": "libnet-91669",
    "storageBucket": "libnet-91669.appspot.com",
    "messagingSenderId": "673223811419",
    "appId": "1:673223811419:web:5d9430cb7f4ebfb5493a7e",
    "measurementId": "G-E5X4YRC00K"
  };

app = Flask(__name__, instance_relative_config=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\projects\\book_prog\\mydb.db'
app.config['SECRET_KEY'] = 'dev'

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()

db = SQLAlchemy(app)

if __name__ == '__main__':
	from auth import *
	from index import *
	app.run(debug = True)