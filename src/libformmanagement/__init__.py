# encoding: utf-8
from __future__ import absolute_import, print_function, division, unicode_literals

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.basicauth import BasicAuth
from flask.json import JSONEncoder
from flask_sslify import SSLify

app = Flask(__name__, static_folder="../web", static_url_path="")
sslify = SSLify(app)
db = SQLAlchemy(app)
basic_auth = BasicAuth(app)

# Allow jsonification of SQLAlchemy Records
#Monkey-Patch db.Model.__iter__...
def sqla_iterator(self):
    for c in filter(lambda x: not x.startswith("_"), self.__dict__):
        yield c, getattr(self, c)
db.Model.__iter__ = sqla_iterator
# We also need to provide a default encoder (for whatever reason)
class SQLAlchemyEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, db.Model):
            return dict(obj)
        return JSONEncoder.default(self, obj)
app.json_encoder = SQLAlchemyEncoder


##### Endpoints

@app.route('/')
def root():
    return app.send_static_file("index.html")

# Facebook sends POST requests...
@app.route('/facebook-tab', methods=["GET","POST"])
def facebook_tab():
    return app.send_static_file("facebook-tab.html")

# Initialize Flask-Admin for the Admin Interface
from .admin import admin
admin.init_app(app)
# Register API
from .api import api
app.register_blueprint(api, url_prefix="/api")
