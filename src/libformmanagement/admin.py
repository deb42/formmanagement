# encoding: utf-8
from __future__ import absolute_import, print_function, division, unicode_literals

from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView
from .models import *

"""
We use Flask-Admin to get a simple admin interface directly from our models.
https://flask-admin.readthedocs.org/en/latest/
"""

admin = Admin(name="Formmanagement Administration")

# To add a model to the admin interface, simply add it below.
admin.add_view(ModelView(Patient, db.session))
admin.add_view(ModelView(Physician, db.session))
admin.add_view(ModelView(Nurse, db.session))
admin.add_view(ModelView(File, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Hads, db.session))