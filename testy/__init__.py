import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DataBase.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://cgzzaksjhzmdzs:55db17b483e0d434cf3e39c3ef264e5346f3b13b2c69a69683beb08bf615cf25@ec2-52-73-184-24.compute-1.amazonaws.com:5432/d748chi53pe91i'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager(app)
app.config['SECRET_KEY'] = os.urandom(32)

bcrypt = Bcrypt(app)

from testy import routes