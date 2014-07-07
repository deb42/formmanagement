import os

# dialect+driver://username:password@host:port/database
SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % os.path.abspath("formmanagement.db")
SQLALCHEMY_ECHO = False
# Evil as errors during .commit() don't get caught.
# SQLALCHEMY_COMMIT_ON_TEARDOWN = True

# Used for secure sessions. Must be kept secret in production.
SECRET_KEY = "OMGORLYDEADBEEF"
SIGNATURE_MAX_AGE = 60*60*24*7  # 7 days

# Flask Debug Mode
DEBUG = True

BASIC_AUTH_FORCE = False
BASIC_AUTH_REALM = "Formmanagement"
BASIC_AUTH_USERNAME = "formmanagement"
BASIC_AUTH_PASSWORD = "1234"

# Facebook App Data
FB_APP_ID = 169367286558343
FB_APP_SECRET = "fe69090bf1319fb701c6bf846aa445f4"

# Mail Data
MAIL_SENDER = None
MAIL_SMTP_SERVER = None