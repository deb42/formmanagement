# encoding: utf-8
from __future__ import absolute_import, print_function, division, unicode_literals

import json

from sqlalchemy import types
from sqlalchemy.ext.associationproxy import _AssociationList
import flask
from flask.ext.sqlalchemy import Model
from flask.json import JSONEncoder


# We also need to provide a default encoder (for whatever reason)
class SQLAlchemyEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, _AssociationList):
            return list(obj)
        if isinstance(obj, Model):
            return dict(obj)
        return JSONEncoder.default(self, obj)

# Flask's jsonify doesn't allow arrays to be returned by default,
# as this might be problematic for EcmaScript 4 Clients.
# We don't care about ES4 clients (IE <= 8).
# http://flask.pocoo.org/docs/security/#json-security
def jsonify_plain(*args, **kwargs):
    return flask.json.dumps(*args, indent=2, cls=SQLAlchemyEncoder, **kwargs)

def jsonify(*args, **kwargs):
    if len(args) == 1 and not kwargs and type(args[0]) == list:
        return flask.Response(jsonify_plain(args[0]), mimetype='application/json')
    else:
        return flask.jsonify(*args, **kwargs)


class JSONType(types.TypeDecorator):
    """
    SQLAlchemy JSON Type
    """

    impl = types.String

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)

        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value
