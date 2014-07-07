# encoding: utf-8
from __future__ import absolute_import, print_function, division, unicode_literals
import datetime

import facebook
import requests
from flask import Blueprint, request, abort, session, redirect
from itsdangerous import URLSafeTimedSerializer, BadData
from sqlalchemy.orm import joinedload
import json

from .models import *
from .seed import jsonify
from . import app


api = Blueprint("api", __name__)

"""
Authentication API

The Authentication API implements the RESTful methods for login/logout an user
and also initiating/destroying sessions.
"""


@api.route("/session")
def get_session_obj():
    if not "user_id" in session:
        abort(403)

    user = User.query.with_polymorphic("*").filter_by(id=session["user_id"]).first_or_404()

    session_data = {
        "user": user
    }
    if type(user) == Patient:
        session_data["physician"] = user.physician
        del user.physician  # don't include the physician data twice.

    return jsonify(session_data)


@api.route("/session", methods=["POST"])
def check_auth():
    """
    Receives a JSON object that contains the login type
    Examples:
        {facebook: {... facebook auth data ...}}
        {username: "Max Muster"}
    """
    auth_request = request.get_json()

    if "username" in auth_request:  # and app.config["DEBUG"]:
        user = User.query.filter_by(name=auth_request["username"]).first_or_404()


    else:
        abort(403)

    session['user_id'] = user.id
    return get_session_obj()


@api.route("/session", methods=["DELETE"])
def logout():
    session.pop('user_id', None)  # Delete user cookie
    return ""



user_modifiable_attrs = ["name"]

"""
physician API
"""


@api.route("/physicians/")
def get_physicians():
    """
    GET to the list: return list of all physicians.
    """
    return jsonify(Physician.query.all())


@api.route("/physicians/<int:id>")
def get_physician(id):
    """
    GET to physician resource: return single physician.
    Use .first_or_404() to automatically raise a 404 error if the resource isn't found.
    """
    return jsonify(Physician.query.filter_by(id=id).first_or_404())


physician_modifiable_attrs = user_modifiable_attrs + ['email']


@api.route("/physicians/<int:id>", methods=["POST"])
def update_physician(id):
    """
    PUT to physician resource: update given physician.
    Notice how we call get_physician() in the end to return the updated physician.
    This way, we don't even need to check whether the user exists as
    get_physician does this for us.
    """
    physician = Physician.query.filter_by(id=id).first_or_404()  # Gibt ein patient/physician object zurück.
    for attr in physician_modifiable_attrs:
        # Check if Attribute was used in Request
        # Then update
        if attr in request.json:
            setattr(physician, attr, request.json[attr])

    db.session.commit()
    return get_physician(id)


"""
patient API
"""


@api.route("/patients/")
def get_patients():
    """
    GET to the list: return list of all patients belonging to physician.
    """
    return jsonify(Patient.query.all())


@api.route("/patients/<int:id>")
def get_patient(id):
    """
    GET to patient resource: return single patient.
    Use .first_or_404() to automatically raise a 404 error if the resource isn't found.
    """
    return jsonify(Patient.query.filter_by(id=id).first_or_404())


patient_modifiable_attrs = user_modifiable_attrs + ["physician_id"]


@api.route("/patients/<int:id>", methods=["POST"])
def update_patient(id):
    """
    PUT to patient resource: update given patient.
    Notice how we call get_patient() in the end to return the updated patient.
    This way, we don't even need to check whether the user exists as
    get_patient does this for us.
    """
    patient = Patient.query.filter_by(id=id).first_or_404()  # Gibt ein patient/physician object zurück.
    for attr in patient_modifiable_attrs:
        # Check if Attribute was used in Request
        # Then update
        if attr in request.json:
            setattr(patient, attr, request.json[attr])

    db.session.commit()
    return get_patient(id)


"""
Events API

The Events API implements all RESTful methods for demonstration purposes.
As you may note, access control is _not_ implemented yet.
For the moment, that's a feature, so just ignore it.
"""


@api.route("/events/")
def get_events():
    """
    GET to the list: return list of all events.
    """
    return jsonify(Event.query
                   .order_by(Event.startTime.asc())
                   .filter(Event.endTime >= datetime.datetime.utcnow())
                   .all())


@api.route("/events/", methods=["POST"])
def add_event():
    """
    POST to the list: add a new event.
    Don't forget to call db.session.commit()
    """
    event = Event(**request.json)
    db.session.add(event)
    db.session.commit()
    return jsonify(event)


"""
Appointments API

The Appointments API implements all RESTful methods for demonstration purposes.
As you may note, access control is _not_ implemented yet.
For the moment, that's a feature, so just ignore it.
"""


@api.route("/appointments/")
def get_appointments():
    """
    GET to the list: return list of all appointments.
    """
    return jsonify(Appointment.query
                   .options(joinedload("physician"))
                   .options(joinedload("patient"))
                   .order_by(Appointment.startTime.asc())
                   .filter(Appointment.endTime >= datetime.datetime.utcnow())
                   .filter((Appointment.patient_id == session["user_id"])
                           | (Appointment.physician_id == session["user_id"]))
                   .all())


@api.route("/appointments/", methods=["POST"])
def add_appointment():
    """
    POST to the list: add a new appointment.
    Don't forget to call db.session.commit()
    """
    appointment = Appointment(**request.json)
    db.session.add(appointment)
    db.session.commit()
    return jsonify(appointment)


"""
Videos API
"""


@api.route('/questionnaires/')
def questionnaires_list():
    return jsonify(Questionnaire.query.all())

@api.route("/questionnaires/<int:id>")
def get_questionnaires(id):
    """
    GET to patient resource: return single patient.
    Use .first_or_404() to automatically raise a 404 error if the resource isn't found.
    """
    return jsonify(Questionnaire.query.filter_by(id=id).first_or_404())

"""
Videos Hads
"""

@api.route('/hads')
def hads_list():
    return jsonify(Hads.query.all())

@api.route("/hads/<int:id>")
def get_hads(id):
    """
    GET to hads resource: return single patient.
    Use .first_or_404() to automatically raise a 404 error if the resource isn't found.
    """
    return jsonify(Hads.query.filter_by(id=id).first_or_404())

@api.route("/hads", methods=["POST"])
def add_hads():
    """
    POST to the list: add a new event.
    Don't forget to call db.session.commit()
    """
    hads = Hads(**request.json)
    #dlqi_data = json.load(request.get_data())
    #print(dlqi_data)
    db.session.add(hads)
    db.session.commit()
    return jsonify(hads)


hads_modifiable_attrs = ["data", "depression_scale", "anxiety_scale"]

@api.route("/hads/<int:id>", methods=["POST"])
def update_hads(id):
    """
    PUT to patient resource: update given patient.
    Notice how we call get_patient() in the end to return the updated patient.
    This way, we don't even need to check whether the user exists as
    get_patient does this for us.
    """
    hads = Hads.query.filter_by(id=id).first_or_404()  # Gibt ein patient/physician object zurück.
    for attr in hads_modifiable_attrs:
        # Check if Attribute was used in Request
        # Then update
        if attr in request.json:
            setattr(hads, attr, request.json[attr])

    db.session.commit()
    return get_hads(id)



"""
File API

The File API implements all RESTful methods for demonstration purposes.
As you may note, access control is _not_ implemented yet.
For the moment, that's a feature, so just ignore it.
"""


@api.route("/files/<access_token>")
def get_file_blob(access_token):
    """
    return file if access token is correct
    """
    f = File.query.filter_by(access_token=access_token).first_or_404()
    return f.data


@api.route('/files', methods=['POST'])
def upload_file():
    # Flask's handling for file uploads is a little bit akward.
    # TL;DR: Get file as string from request.
    files = request.files.listvalues()
    if not files:
        abort(400)
    file_contents = files[0][0].read()

    db_file = File(data=file_contents)
    db.session.add(db_file)
    db.session.commit()
    return jsonify({
        "access_token": db_file.access_token
    })