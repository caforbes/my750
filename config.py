import os

rootdir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "sample-secret-itsrelativelylong"
    TESTING = False
    if TESTING:
        PG_DATABASE_URI = os.getenv("TEST_DATABASE_URL")
    else:
        PG_DATABASE_URI = os.getenv("DATABASE_URL")
