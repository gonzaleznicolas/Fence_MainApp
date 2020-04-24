from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

# make the application its own package
app = Flask(__name__)

# used to generate signatures and protect the web forms against cross-site request forgery
app.config['SECRET_KEY'] = os.environ['FENCE_MAIN_APP_SECRET_KEY']

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{os.environ['FENCE_MAIN_APP_DB_USER']}:{os.environ['FENCE_MAIN_APP_DB_PASSWORD']}@{os.environ['FENCE_MAIN_APP_DB_HOST']}/{os.environ['FENCE_MAIN_APP_DB_NAME']}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# used to hash passwords before they are stored in the DB
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from fence import routes