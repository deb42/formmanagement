# encoding: utf-8
from __future__ import absolute_import, print_function, division, unicode_literals
import os
import binascii

from . import db


"""
We use SQLAlchemy and Flask-SQLAlchemy to map SQL tables to Python classes.
http://pythonhosted.org/Flask-SQLAlchemy/ <- excellent simple examples
http://de.slideshare.net/jbellis/pycon-2010-sqlalchemy-tutorial <- intro to sqlalchemy presentation
http://www.sqlalchemy.org/ <- api reference
TL;DR: It's awesome.
"""


# User <-> Conversation Table
# Many-to-Many: see http://docs.sqlalchemy.org/en/rel_0_9/orm/relationships.html#many-to-many
conversation_participants = db.Table(
    'conversation_members',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('conversation_id', db.Integer, db.ForeignKey('conversation.id'))
)

TYPE_PATIENT = 0b001
TYPE_PHYSICIAN = 0b010
TYPE_ADMINISTRATOR = 0b100 | TYPE_PHYSICIAN


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    profile_picture_id = db.Column(db.Integer, db.ForeignKey('file.access_token'))
    # Contains Type of current object, needed for inheritance
    type = db.Column(db.Integer)

    profile_picture = db.relationship("File", uselist=False)

    conversations = db.relationship("Conversation",
                                    secondary=conversation_participants,
                                    backref="users")
    messages = db.relationship("Message", backref="author")

    __mapper_args__ = {
        'polymorphic_on': type
    }

    def __repr__(self):
        return self.name


class Patient(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': TYPE_PATIENT
    }
    email = db.Column(db.String(120))
    diagnosiss = db.relationship("Diagnosis", backref="patient", foreign_keys="Diagnosis.patient_id")

    physician_id = db.Column(db.Integer, db.ForeignKey('physician.id'))



class Physician(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': TYPE_PHYSICIAN
    }
    diagnosiss = db.relationship("Diagnosis", backref="physician", foreign_keys="Diagnosis.physician_id")
    patients = db.relationship("Patient", foreign_keys="Patient.physician_id", backref="physician")



class Administrator(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': TYPE_ADMINISTRATOR
    }


class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))

    messages = db.relationship("Message", backref="conversation")

    def __repr__(self):
        return "%s (%s)" % (self.title, ", ".join(unicode(u) for u in self.users))


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey("conversation.id"))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    content = db.Column(db.String(1000))

    def __repr__(self):
        return "%s: %s" % (self.author, self.content)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    details = db.Column(db.String(1000))
    startTime = db.Column(db.DateTime())
    endTime = db.Column(db.DateTime())

    def __repr__(self):
        return "%s: %s" % (self.title, self.details)


class Diagnosis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    physician_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(140))
    details = db.Column(db.String(1000))
    startTime = db.Column(db.DateTime())
    endTime = db.Column(db.DateTime())

    def __repr__(self):
        return "%s: %s" % (self.title, self.details)

# FIXME: Remove, integrate into messages
class DiagnosisProposal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    physician_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(140))
    details = db.Column(db.String(1000))
    accepted = db.Column(db.Boolean)
    # Proposals are saved as a JSON-Array of start and end times
    proposal = db.Column(db.String)

    def __repr__(self):
        return "%s: %s" % (self.title, self.details)


class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    url = db.Column(db.String(1000))
    poster_id = db.Column(db.Integer, db.ForeignKey('file.access_token'))
    poster = db.relationship("File", uselist=False)

    def __repr__(self):
        return "%s: %s" % (self.title, self.url)


def _random_string():
    return binascii.b2a_hex(os.urandom(15))


class File(db.Model):
    access_token = db.Column(db.String(16), primary_key=True, default=_random_string)
    data = db.Column(db.Binary)

    def __repr__(self):
        return self.access_token