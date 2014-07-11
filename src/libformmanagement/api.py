# encoding: utf-8
from __future__ import absolute_import, print_function, division, unicode_literals

from flask import Blueprint, request, abort, session

from .questionnaire_api import init_reply
from .models import *
from .seed import jsonify


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
Questionnaires API
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

@api.route('/reply')
def hads_list():
    return jsonify(Reply.query.with_polymorphic("*").all())

@api.route("/reply/<int:type>/<int:id>")
def get_reply(type, id):
    """
    GET to hads resource: return single patient.
    Use .first_or_404() to automatically raise a 404 error if the resource isn't found.
    """
    return jsonify(Reply.query.with_polymorphic("*").filter_by(patient_id=id).filter_by(type=type).all())

@api.route("/reply/<int:type>/<int:id>", methods=["POST"])
def add_reply(type,id):
    """
    POST to the list: add a new reply.
    The right type will be defined in the function init_reply
    Don't forget to call db.session.commit()
    """
    type += TYPE_HADS
    patient = Patient.query.filter_by(id=id).first_or_404()
    questionnaire=Questionnaire.query.filter_by(type=type).first_or_404()
    reply = init_reply(request.json["data"],type,patient,questionnaire["value"])
    db.session.add(reply)
    db.session.commit()
    return jsonify(reply)

"""
hads_modifiable_attrs = ["data", "depression_scale", "anxiety_scale"]


@api.route("/hads/<int:id>", methods=["POST"])
def update_hads(id):

    PUT to patient resource: update given patient.
    Notice how we call get_patient() in the end to return the updated patient.
    This way, we don't even need to check whether the user exists as
    get_patient does this for us.

    hads = Hads.query.filter_by(id=id).first_or_404()  # Gibt ein patient/physician object zurück.
    for attr in hads_modifiable_attrs:
        # Check if Attribute was used in Request
        # Then update
        if attr in request.json:
            setattr(hads, attr, request.json[attr])

    db.session.commit()
    return get_hads(id)

"""



