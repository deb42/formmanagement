# encoding: utf-8
from __future__ import absolute_import, print_function, division, unicode_literals
import os
import binascii

from . import db, utils
from datetime import date as _date


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

TYPE_PATIENT        = 0b0001
TYPE_PHYSICIAN      = 0b0010
TYPE_ADMINISTRATOR  = 0b0100 | TYPE_PHYSICIAN

"""
the typs of questionnaires are defined here
remember: TYPE_HADS has to have the lowest number
          in case of change: api.py l. 272
          @api.route("/reply/<int:type>/<int:id>", methods=["POST"]) must be improved
"""

TYPE_HADS = 0b1001
TYPE_DLQI = 0b1010
TYPE_PBI  = 0b1011


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
    diagnoses = db.relationship("Diagnosis", backref="patient", foreign_keys="Diagnosis.patient_id")
    #questionnaires = db.relationship("Hads", backref="hads", foreign_keys="Hads.patient_id")
    questionnaire_replies = db.relationship("Reply", backref="patient", foreign_keys="Reply.patient_id")


    physician_id = db.Column(db.Integer, db.ForeignKey('physician.id'))



class Physician(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': TYPE_PHYSICIAN
    }
    diagnoses = db.relationship("Diagnosis", backref="physician", foreign_keys="Diagnosis.physician_id")
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


class Questionnaire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    type= type = db.Column(db.Integer, unique=True)
    content = db.Column(utils.JSONType(5000))
    value= db.Column(utils.JSONType(500))
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __repr__(self):
        return "%s: %s" % (self.title, self.value)
    def __getitem__(self, item):
        if item == "value": return self.value


class Reply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.String(12))
    data = db.Column(utils.JSONType(5000))

    type = db.Column(db.Integer)

    __mapper_args__ = {
        'polymorphic_on': type
    }

    def __repr__(self):
        return "%s: %s" % (self.patient_id, self.date)


class Hads(Reply):
    id = db.Column(db.Integer, db.ForeignKey('reply.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': TYPE_HADS
    }

    anxiety_scale = db.Column(db.Integer)
    depression_scale = db.Column(db.Integer)


class Test(db.Column):
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(10))


def _random_string():
    return binascii.b2a_hex(os.urandom(15))


class File(db.Model):
    access_token = db.Column(db.String(16), primary_key=True, default=_random_string)
    data = db.Column(db.Binary)

    def __repr__(self):
        return self.access_token