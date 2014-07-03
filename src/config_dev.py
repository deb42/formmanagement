import os

# dialect+driver://username:password@host:port/database
SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % os.path.abspath("formmanagement.db")
SQLALCHEMY_ECHO = False
# Evil as errors during .commit() don't get caught.
# SQLALCHEMY_COMMIT_ON_TEARDOWN = True

# Used for secure sessions. Must be kept secret in production.
SECRET_KEY = "OMGORLYDEADBEEF"

# Flask Debug Mode
DEBUG = True