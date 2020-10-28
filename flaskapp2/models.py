from datetime import datetime
from flaskapp2 import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(userId):
    return User.query.get(int(userId))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(60), nullable=False)
    lastname = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(60), nullable = False)
    dob= db.Column(db.Date, nullable=False)
    password = db.Column(db.String(60), nullable = False)
    number = db.Column(db.String(12), nullable=False)
    confirmed = db.Column(db.Boolean, default = False, nullable = False)
    def __repr__(self):
        return f"User('{self.email}','{self.firstname}','{self.lastname}','{self.dob}','{self.number}','{self.confirmed}')"

