# -*- coding: utf-8 -*-
"""User models."""
import datetime as dt

# from flask_security import UserMixin, RoleMixin, SQLAlchemyUserDatastore
from flask_login import UserMixin

from palette.database import Column, Model, SurrogatePK, db, reference_col, relationship
from palette.extensions import bcrypt


class Role(SurrogatePK, Model):  # RoleMixin
    """A role for a user."""

    __tablename__ = 'roles'
    name = Column(db.String(80), unique=True, nullable=False)
    description = Column(db.String(255))  #
    user_id = reference_col('users', nullable=True)
    user = relationship('User', backref='roles')

    def __init__(self, name, **kwargs):
        """Create instance."""
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Role({name})>'.format(name=self.name)


class User(UserMixin, SurrogatePK, Model):
    """A user of the app."""

    __tablename__ = 'users'
    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(80), unique=True, nullable=False)
    password = Column(db.Binary(128), nullable=True)  #: The hashed password
    # password = Column(db.String(255))  #
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    first_name = Column(db.String(30), nullable=True)
    last_name = Column(db.String(30), nullable=True)
    active = Column(db.Boolean(), default=False)
    is_admin = Column(db.Boolean(), default=False)
    confirmed_at = Column(db.DateTime)  #
    last_login_at = Column(db.DateTime)  #
    current_login_at = Column(db.DateTime)  #
    last_login_ip = Column(db.String(80))  #
    current_login_ip = Column(db.String(80))  #
    login_count = Column(db.Integer)  #


    def __init__(self, username, email, password=None, **kwargs):
        """Create instance."""
        db.Model.__init__(self, username=username, email=email, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    def set_password(self, password):
        """Set password."""
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self.password, value)

    @property
    def full_name(self):
        """Full user name."""
        return '{0} {1}'.format(self.first_name, self.last_name)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<User({username!r})>'.format(username=self.username)
