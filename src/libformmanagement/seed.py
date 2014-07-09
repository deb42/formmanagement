# encoding: utf-8
from __future__ import absolute_import, print_function, division, unicode_literals
from datetime import *
import random
import string

import flask
import json

from .models import *
from . import app


# Flask's jsonify doesn't allow arrays to be returned by default,
# as this might be problematic for EcmaScript 4 patients.
# We don't care about ES4 patients (IE <= 8).
# http://flask.pocoo.org/docs/security/#json-security
def jsonify(*args, **kwargs):
    if len(args) == 1 and not kwargs and type(args[0]) == list:
        return flask.Response(flask.json.dumps(args[0], indent=2), mimetype='application/json')
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

    # Kundenberater seeden
    physician_datasets = (
        {
            "name": "Verena Meier"
        },
        {
            "name": "Anna Gaul"
        },
        {
            "name": "Peter Hubner"
        },
        {
            "name": "Herbert Becker"
        },
        {
            "name": "Jörg Bayer"
        },
        {
            "name": "Oliver Meier"
        },
        {
            "name": "Yannic Wulf"
        }
    )



    physicians = [Physician(name=physician_datasets[i]["name"])
                for i in range(len(physician_datasets))]
    for i in range(len(physician_datasets)):
        db.session.add(physicians[i])

    # Kunden seeden
    patient_datasets = (
        {
            "name": "Siegrun Kreft"
        },
        {
            "name": "Lena Laengerich"
        },
        {
            "name": "Dr. Peter Becker"
        },
        {
            "name": "Lilo Meier"
        },
        {
            "name": "Hardmut Forster"
        },
        {
            "name": "Dieter Dormeier"
        },
        {
            "name": "Prof. Dr. Dr. Julian von Anhalt"
        }
    )

    patients = []
    for i in range(len(patient_datasets)):
        physician =  physicians[1]
        patients.append(
            Patient(
                name=patient_datasets[i]["name"],
                email="kunde" + str(i) + "@example.com",
                # Kundenberater zufällig zuweisen
                physician=physician
            )
        )

    for patient in patients:
        db.session.add(patient)

    callcenter = User(name="Call Center")

    db.session.add(callcenter)

    c1 = Conversation(title="Testgespräch")
    patients[0].conversations.append(c1)
    physicians[2].conversations.append(c1)
    c1.messages.append(Message(author=patients[0], content="Hallo, dies ist ein Test."))
    c1.messages.append(Message(author=physicians[2], content="Hören Sie auf, mich zu testen!"))

    c2 = Conversation(title="Frage zu Bankwechsel")
    c2.messages.append(Message(author=patients[1], content="Niemand antwortet mir :-("))
    c2.users.extend([patients[1], callcenter])

    c3 = Conversation(title="Flotte Dreierverkonversation")
    c3.users.extend([patients[2], physicians[1], callcenter])

    event1 = Event(title="Volksbank Marathon",
                   details="laberabarberabarber...",
                   startTime=datetime(2014, 6, 3, 13, 30),
                   endTime=datetime(2014, 6, 3, 13, 31))
    event2 = Event(title="Volksbank Spartag",
                   details="laberabarberabarber... (2)",
                   startTime=datetime(2014, 8, 3, 13, 30),
                   endTime=datetime(2014, 6, 3, 13, 31))
    db.session.add(event1)
    db.session.add(event2)

    # Diagnosis seeden
    diagnosis_datasets = (
        {
            "title": "Beratung Bausparvertrag",
            "details": "Bitte kommen Sie zu mir in die Filiale."
        },
        {
            "title": "Hauskauf",
            "details": "Ich komme bei Ihnen vorbei."
        }
    )
    for i in range(30):
        patient = random.choice(patients) if i < 15 else patients[0]  # Zufälligen Kundenberater auswählen
        starttime = (datetime.now()
                     + timedelta(days=random.randint(0, 14))
                     + timedelta(minutes=random.randint(-24 * 60, 24 * 60)))
        endtime = starttime + timedelta(days=random.randint(0, 1), minutes=random.randint(0, 600))

        diagnosis_data = random.choice(diagnosis_datasets)
        diagnosis = Diagnosis(title=diagnosis_data["title"],
                                  patient=patient,
                                  physician=patient.physician,
                                  details=diagnosis_data["details"],
                                  startTime=starttime,
                                  endTime=endtime)
        db.session.add(diagnosis)


    json_data = open("./libformmanagement/seed/questionnaires/hads.json")
    hads_data = json.load(json_data)

    hads = Questionnaire(
        title= "hads",
        content= hads_data["content"],
        type=TYPE_HADS,
        value=hads_data["value"]
    )

    db.session.add(hads)

    json_data = open("./libformmanagement/seed/questionnaires/dlqi.json")
    dlqi_data = json.load(json_data)

    dlqi = Questionnaire(
        title= "dlqi",
        content= dlqi_data["content"],
        type=10,
        value=dlqi_data["value"]
    )

    db.session.add(dlqi)

    hadsresult = Hads(
        patient = patients[1],
        date=date.today(),
        data=[0, 1, 1],
        anxiety_scale =1,
        depression_scale = 1
    )

    hadsresult1 = Hads(
        patient = patients[1],
        date=date.today(),
        data=[0, 1, 1],
        anxiety_scale =1,
        depression_scale = 1
    )
    hadsresult2 = Hads(
        patient = patients[1],
        date=date.today(),
        data=[0, 1, 1],
        anxiety_scale =1,
        depression_scale = 1
    )
    hadsresult3 = Hads(
        patient = patients[1],
        date=date.today(),
        data=[0, 1, 1],
        anxiety_scale =1,
        depression_scale = 1
    )

    db.session.add(hadsresult)
    db.session.add(hadsresult1)
    db.session.add(hadsresult2)
    db.session.add(hadsresult3)


    db.session.commit()