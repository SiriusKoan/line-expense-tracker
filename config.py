from os import getenv, urandom


class Config:
    SECRET = urandom(32)
    SQLALCHEMY_DATABASE_URI = "sqlite:///data.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
