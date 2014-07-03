# encoding: utf-8
from __future__ import absolute_import, print_function, division, unicode_literals
from flask import Blueprint, request, abort, session
from sqlalchemy.orm import joinedload
from .models import *
from .utils import jsonify


api = Blueprint("api", __name__)

"""
Authentication API

The Authentication API implements the RESTful methods for login/logout an user
and also initiating/destroying session.
"""


@api.route("/session", methods=["POST"])
def check_auth():
    user = User.query.filter_by(name=request.json["username"]).first_or_404()
    # set session cookie
    session['user_id'] = user.user_id
    # return session object. this is cached on the client side to avoid unnecessary requests.
    return jsonify({
        "user":  user
    })


@api.route("/session", methods=["DELETE"])
def logout():
    session.pop('user_id', None)  # Delete user cookie
    return ""


"""
User API

The User API implements all RESTful methods for demonstration purposes.
As you may note, access control is _not_ implemented yet.
For the moment, that's a feature, so just ignore it.
"""

@api.route("/users/")
def get_users():
    """
    GET to the list: return list of all patients.
    jsonify only accepts objects, not list. use {objects: [actual list]} structure.
    """
    return jsonify(User.query.with_polymorphic("*").all())

@api.route("/patients/")
def get_patients():
    """
    GET to the list: return list of all patients.
    jsonify only accepts objects, not list. use {objects: [actual list]} structure.
    """
    return jsonify(Patient.query.all())



@api.route("/patient/<int:id>")
def get_patient(id):
    """
    GET to user resource: return single user.
    Use .first_or_404() to automatically raise a 404 error if the resource isn't found.
    """
    return jsonify(Patient.query.filter_by(id=id).first_or_404())

@api.route("/hadss/")
def get_hadss():
    """
    GET to the list: return list of all patients.
    jsonify only accepts objects, not list. use {objects: [actual list]} structure.
    """
    return jsonify(Hads.query
                   .options(joinedload("patient"))
                   .first_or_404())




