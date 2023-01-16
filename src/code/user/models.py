from uuid import uuid4
from code.utils.base import BaseMixin
from ..extensions import db
from flask_security import UserMixin, RoleMixin
import datetime

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin,BaseMixin):
    __tablename__ = 'role'
    
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    
    def __repr__(self):
            return '<Role> {}'.format(self.name)


class User( UserMixin,db.Model,BaseMixin):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    fs_uniquifier = db.Column(db.String(255), unique=False, nullable=False, default=uuid4().hex)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),  nullable=True)
    confirmed_at = db.Column(db.DateTime())
    #email confirmation
   
    #tracking
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(255))
    current_login_ip = db.Column(db.String(255))
    login_count = db.Column(db.Integer())
    profile_information = db.Column(db.String(100000))
    event = db.Column(db.String(100000))
    location = db.Column(db.String(1000))
    eventtime = db.Column(db.String(1000))
    
    roles = db.relationship(
        'Role',
        secondary=roles_users,
        backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return '<User> {} {}'.format(self.id, self.email, self.profile_information,self.location,self.eventtime)
    def return_prof(self):
        return '{}'.format(self.profile_information)

    



