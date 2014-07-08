# encoding: utf-8
from __future__ import absolute_import, print_function, division, unicode_literals

from flask import request, abort
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView
from wtforms import FileField
from .models import *

"""
We use Flask-Admin to get a simple admin interface directly from our models.
https://flask-admin.readthedocs.org/en/latest/
"""

admin = Admin(name="Bankbook Administration")


class FlaskFileField(FileField):
    def populate_obj(self, obj, name):
        files = request.files.listvalues()
        if not files or not files[0][0].filename:
            abort(400)
        file_contents = files[0][0].read()
        setattr(obj, name, file_contents)


class FileView(ModelView):
    column_list = ('access_token', )
    form_overrides = dict(data=FlaskFileField)

# To add a model to the admin interface, simply add it below.
# admin.add_view(ModelView(User, db.session))
admin.add_view(FileView(File, db.session))
admin.add_view(ModelView(Patient, db.session))
admin.add_view(ModelView(Physician, db.session))
admin.add_view(ModelView(Administrator, db.session))
admin.add_view(ModelView(Reply, db.session))
admin.add_view(ModelView(Hads, db.session))
admin.add_view(ModelView(Event, db.session))
admin.add_view(ModelView(Diagnosis, db.session))
admin.add_view(ModelView(Questionnaire, db.session))
