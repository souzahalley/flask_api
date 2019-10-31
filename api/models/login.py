from api import app, db, guard
from flask_praetorian import Praetorian
from datetime import datetime

# CREATE SCHEMA IF NOT EXISTS login;

class Users(db.Model):
    __tablename__ = "users"
    __table_args__ = {'schema' : 'login'}
    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.Text)
    password = db.Column(db.Text)
    roles = db.Column(db.Text)
    creation = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=False, server_default='false')

    @classmethod
    def lookup(cls, username):
        return cls.query.filter_by(username=username).one_or_none()
    
    @classmethod
    def identify(cls, id):
        return cls.query.get(id)

    @property
    def rolenames(self):
        try:
            return self.roles.split(' ')
        except Exception:
            return []

    @property
    def identity(self):
        return self.id
    
    def is_valid(self):
        return self.is_active

    def serialize(self):
        return {
            "username" : self.username,
            "roles" : self.roles.split(" "),
            "active" : self.is_active,
            "creation" : self.creation,
            "last_login" : self.last_login
        }


guard.init_app(app, Users)

# TODO: This will stay here for the future

# class Profile(db.Model):
#     __tablename__ = "profile"
#     __table_args__ = {'schema' : 'login'}
#     id = db.Column(db.Integer, primary_key=True, unique=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('login.users.id'))
#     first_name = db.Column(db.String(30))
#     last_name = db.Column(db.String(30))
#     birthday = db.Column(db.DateTime, default=datetime.utcnow)
#     location = db.Column(db.String(30))
#     summary = db.Column(db.Text)
#     user = db.relationship('Users', back_populates="profile")
