# encoding: utf-8
from __future__ import absolute_import, print_function, division, unicode_literals
from . import db
from datetime import date as _date

from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

import os, binascii

"""
We use SQLAlchemy and Flask-SQLAlchemy to map SQL tables to Python classes.
http://pythonhosted.org/Flask-SQLAlchemy/ <- excellent simple examples
http://de.slideshare.net/jbellis/pycon-2010-sqlalchemy-tutorial <- intro to sqlalchemy presentation
http://www.sqlalchemy.org/ <- api reference
TL;DR: It's awesome.
"""

TYPE_PATIENT =          0b0001
TYPE_PHYSICIAN =        0b0010
TYPE_NURSE =            0b0100
TYPE_ADMINISTRATOR =    0b1000

# User <-> Conversation Table
# Many-to-Many: see http://docs.sqlalchemy.org/en/rel_0_9/orm/relationships.html#many-to-many
"""
conversation_participants = db.Table(
    'conversation_members',
    db.Column('user_id', db.Integer, db.ForeignKey('user.user_id')),
    db.Column('conversation_id', db.Integer, db.ForeignKey('conversation.conversation_id'))
)
"""

class Hads(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    code = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=_date.today())

    def __repr__(self):
        return self.code

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login_id = db.Column(db.String(8), unique=True)
    forename = db.Column(db.String(40))
    surname = db.Column(db.String(80))
    # Contains Type of current object, needed for inheritance
    type = db.Column(db.Integer)

    __mapper_args__ = {
        'polymorphic_on': type
    }

    def __repr__(self):
        return self.surname

class Patient(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': TYPE_PATIENT
    }
    hads_questionairs = db.relationship("Hads", foreign_keys="Hads.patient_id", backref="user")
    treatments = db.Column(db.Integer)

class Physician(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': TYPE_PHYSICIAN
    }

class Nurse(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': TYPE_NURSE
    }

class Administrator(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': TYPE_ADMINISTRATOR
    }







def _random_string():
    return binascii.b2a_hex(os.urandom(15))

class File(db.Model):
    access_token = db.Column(db.String(16), primary_key=True, default=_random_string)
    data = db.Column(db.Binary)

    def __repr__(self):
        return self.access_token