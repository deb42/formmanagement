# encoding: utf-8
from __future__ import absolute_import, print_function, division, unicode_literals
from .models import *
from . import app
import flask


# Flask's jsonify doesn't allow arrays to be returned by default,
# as this might be problematic for EcmaScript 4 Clients.
# We don't care about ES4 clients (IE <= 8).
# http://flask.pocoo.org/docs/security/#json-security
def jsonify(*args, **kwargs):
    if len(args) == 1 and not kwargs and type(args[0]) == list:
        return flask.Response(flask.json.dumps(args[0], indent=2),  mimetype='application/json')
    else:
        return flask.jsonify(*args, **kwargs)

def seed():
    """
    Seed function to populate the database with initial values.
    """
    try:
        if User.query.first() and not app.config["DEBUG"]:
            return  # dev mode: always seed db on restart
    except:
        pass

    print("Create Tables...")
    db.drop_all()
    db.create_all()

    print("Seeding...")



    patient1 = Patient(login_id="m_must01", forename="Max", surname="Muster", treatments=7,)
    patient2 = User(login_id="b_alte01", forename="Bar", surname="Alter",)
    physician = Physician(login_id="m_hein01", forename="Heiner", surname="Sommer",)
    nurse = Nurse(login_id="c_irde01", forename="Carla", surname="Irgendwas",)
    db.session.add(patient1)
    db.session.add(patient2)
    db.session.add(physician)
    db.session.add(nurse)

    hads = Hads(patient_id=1, code= 1234,)
    db.session.add(hads)


    db.session.commit()