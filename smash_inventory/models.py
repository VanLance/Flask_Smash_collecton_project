from flask_login.login_manager import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime
import flask_sqlalchemy 

from werkzeug.security import generate_password_hash, check_password_hash

import secrets

from flask_login import UserMixin

from flask_login import LoginManager

from flask_marshmallow import Marshmallow

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String(150), primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = "")
    last_name = db.Column(db.String(150), nullable = True, default = "")
    email = db.Column(db.String(150), nullable= False)
    password = db.Column(db.String, nullable=True, default = "")
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = "", unique = True)
    date_created =  db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    character = db.relationship('Character', backref= 'owner', lazy = True)

    def __init__(self, email, first_name= "", last_name = "", id = '', password = "", token = '', g_auth_verify = False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name= last_name
        self.password = self.set_password(password)
        self.email= email
        self.token = self.set_token(24)
        self.g_auth_verify= g_auth_verify

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self,password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f'User {self.email} is ready to collect Smashies!'
        
class Character(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(200), nullable= True)
    games_appeared_in = db.Column(db.String(200), nullable = True)
    abilities = db.Column(db.String(200), nullable = True)
    weight = db.Column(db.String(50), nullable = True)
    date_created =  db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    jumps = db.Column(db.Numeric(precision=10))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)
    

    def __init__(self, name, description, games_appeared_in, abilities, weight, jumps, user_token):
        self.id = self.set_id()
        self.name = name
        self.description= description
        self.games_appeared_in = games_appeared_in
        self.abilities = abilities
        self.weight = weight
        self.jumps = jumps
        self.user_token = user_token

    def __repr__(self):
        return f'The following Smashie has been added: {self.name}'

    def set_id(self):
        return (secrets.token_urlsafe()) 

class CharacterSchema(ma.Schema):
    class Meta:
        fields = ["id", 'name', 'description', 'games_appeared_in', 'abilites', 'weight', 'date_created', 'jumps']

character_schema = CharacterSchema()

characters_schema = CharacterSchema(many = True)