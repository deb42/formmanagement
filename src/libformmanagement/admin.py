# encoding: utf-8
from __future__ import absolute_import, print_function, division, unicode_literals
from flask import session

from flask.ext.admin import Admin, expose, AdminIndexView
from flask.ext.admin.base import MenuLink, render_template
from flask.ext.admin.contrib.fileadmin import FileAdmin
from flask.ext.admin.contrib.sqla import ModelView

from . import app
from .models import *

"""
We use Flask-Admin to get a simple admin interface directly from our models.
https://flask-admin.readthedocs.org/en/latest/
"""


class MyHomeView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin_index.html')

    def is_accessible(self):
        return is_admin()


admin = Admin(name="FIKtiv Administration", index_view=MyHomeView())


def is_admin():
    if app.config["DEBUG"]:  # pragma: nocover
        return True
    if not "user_id" in session:
        return False
    user = User.query.filter_by(id=session["user_id"]).first_or_404()
    return bool(user.type & TYPE_ADMINISTRATOR)


class FiktivModelView(ModelView):
    def is_accessible(self):
        return is_admin()


class FiktivFileAdmin(FileAdmin):
    def is_accessible(self):
        return is_admin()

# To add a model to the admin interface, simply add it below.
# admin.add_view(ModelView(User, db.session))
admin.add_view(FiktivModelView(DiagnosisParticipants, db.session))
admin.add_view(FiktivModelView(Patient, db.session, category="Users"))
admin.add_view(FiktivModelView(Physician, db.session, category="Users"))
admin.add_view(FiktivModelView(Administrator, db.session, category="Users"))
admin.add_view(FiktivModelView(Reply, db.session))
admin.add_view(FiktivModelView(Hads, db.session, category="Replies"))
admin.add_view(FiktivModelView(Dlqi, db.session, category="Replies"))
admin.add_view(FiktivModelView(Pbi, db.session, category="Replies"))
admin.add_view(FiktivModelView(Questionnaire, db.session))
admin.add_link(MenuLink(name='FIKtiv', url='/'))

