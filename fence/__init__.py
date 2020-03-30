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
print(f"RDS_USERNAME: {os.environ['RDS_USERNAME']}")
print(f"RDS_PASSWORD: {os.environ['RDS_PASSWORD']}")
print(f"RDS_HOSTNAME: {os.environ['RDS_HOSTNAME']}")
print(f"RDS_PORT: {os.environ['RDS_PORT']}")
print(f"RDS_DB_NAME: {os.environ['RDS_DB_NAME']}")
print(f"mysql://{os.environ['RDS_USERNAME']}:{os.environ['RDS_PASSWORD']}@{os.environ['RDS_HOSTNAME']}/{os.environ['RDS_DB_NAME']}")
# app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///site.{'db'}"
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{os.environ['RDS_USERNAME']}:{os.environ['RDS_PASSWORD']}@{os.environ['RDS_HOSTNAME']}/{os.environ['RDS_DB_NAME']}"

db = SQLAlchemy(app)

# used to hash passwords before they are stored in the DB
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from fence import routes