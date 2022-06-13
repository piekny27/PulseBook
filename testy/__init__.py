import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DataBase.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://wsmohbpxwpqpob:fad7202693beaffac649af452f9c7dda06a9326eaa359b37bb59b80f61f3af51@ec2-63-32-248-14.eu-west-1.compute.amazonaws.com:5432/d33ut4rls21iaj'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager(app)
app.config['SECRET_KEY'] = os.urandom(32)

bcrypt = Bcrypt(app)

from testy import routes