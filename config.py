from os import getenv, urandom


class Config:
    SECRET = urandom(32)
    SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
