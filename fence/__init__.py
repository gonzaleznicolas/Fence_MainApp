from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

# make the application its own package
app = Flask(__name__)

# used to generate signatures and protect the web forms against cross-site request forgery
app.config['SECRET_KEY'] = 'a8d5u2grr7lo2cp'

print("HELOOOOOOOO")
# app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///site.{'db'}"
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://nico:.Seng401@aa1jkdj3cz1d2sd.cq1jyeha7bzs.us-west-2.rds.amazonaws.com/ebdb"

db = SQLAlchemy(app)

# used to hash passwords before they are stored in the DB
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from fence import routes