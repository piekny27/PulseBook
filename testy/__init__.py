import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DataBase.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://uvvdtmrpliizua:ae4230cf848b72c0cf627c0745b27e18b92d9dbec4e138c82f75216d900734e5@ec2-54-228-32-29.eu-west-1.compute.amazonaws.com:5432/d5i2ue6f3o4r9j'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager(app)
app.config['SECRET_KEY'] = os.urandom(32)

bcrypt = Bcrypt(app)

from testy import routes