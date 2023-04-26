from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime

# adding flask security for passwords
from werkzeug.security import generate_password_hash, check_password_hash

# import secrets module (from python) generate a token for each user
import secrets

# import flask login
from flask_login import UserMixin, LoginManager

from flask_marshmallow import Marshmallow

db = SQLAlchemy()  # instantiating our database
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = '')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default = '')
    username = db.Column(db.String(150), nullable = True)
    token = db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    hero = db.relationship('Hero', backref = 'owner', lazy = True)
    # come back and add backref drone relationship

    def __init__(self, email, username, first_name = '', last_name = '',password = ''):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.username = username
        self.token = self.set_token(24)

    def set_token(self, length):
        return secrets.token_hex(length)
    
    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        print(self.pw_hash)
        return self.pw_hash
    
    def __repr__(self):
        return f"User {self.email} has been added to the database! wooo"
    


class Hero(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(150), nullable = True)
    comic_in = db.Column(db.Integer)
    super_power = db.Column(db.String(150), nullable = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    random_marvel = db.Column(db.String, nullable = True)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable=False)

    def __init__(self, name, description, comic_in, super_power,random_marvel, user_token):
        self.id = self.set_id()
        self.name = name
        self.description = description
        self.comic_in = comic_in
        self.super_power = super_power
        self.random_marvel
        self.user_token = user_token

    def set_id(self):
        return str(uuid.uuid4())

    def __repr__(self):
        return f"Hero {self.name} has been added to the data base!!"

class HeroSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'description', 'comic_in', 'super_power', 'date_created', 'random_marvel']

hero_schema = HeroSchema()
heros_schema = HeroSchema(many = True)