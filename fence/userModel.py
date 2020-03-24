from fence import db, login_manager
from flask_login import UserMixin


# the flask_login extension requires this function so that it knows how to load a user by user_id
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


#extend UserMixin so that flask_login will know how to check if a user is authenticated, if its active, etc.
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    # this defines how to print a user. Useful for interacting with DB from command line
    def __repr__(self):
        return f"User('{self.id}' ,'{self.username}')"

