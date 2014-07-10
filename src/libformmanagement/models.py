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
    # Contains Type of current object, needed for inheritance
    type = db.Column(db.Integer)

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
    #questionnaires = db.relationship("Hads", backref="hads", foreign_keys="Hads.patient_id")
    questionnaire_replies = db.relationship("Reply", backref="patient", foreign_keys="Reply.patient_id")

    physician_id = db.Column(db.Integer, db.ForeignKey('physician.id'))



class Physician(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': TYPE_PHYSICIAN
    }
    patients = db.relationship("Patient", foreign_keys="Patient.physician_id", backref="physician")



class Administrator(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': TYPE_ADMINISTRATOR
    }


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

class Dlqi(Reply):
    id = db.Column(db.Integer, db.ForeignKey('reply.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': TYPE_DLQI
    }

    score = db.Column(db.Integer)


class Pbi(Reply):
    id = db.Column(db.Integer, db.ForeignKey('reply.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': TYPE_PBI
    }