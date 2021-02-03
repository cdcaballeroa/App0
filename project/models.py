from flask_login import UserMixin
from . import usersDB


class User(UserMixin, usersDB.Model):
    id = usersDB.Column(usersDB.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    email = usersDB.Column(usersDB.String(100), unique=True)
    password = usersDB.Column(usersDB.String(100))
    name = usersDB.Column(usersDB.String(100))


class Event(UserMixin, usersDB.Model):
    __bind_key__ = "events"
    id = usersDB.Column(usersDB.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    email = usersDB.Column(usersDB.String(100), unique=False)
    name = usersDB.Column(usersDB.String(100))
    category = usersDB.Column(usersDB.String(12))
    place = usersDB.Column(usersDB.String(100))
    address = usersDB.Column(usersDB.String(100))
    startDate = usersDB.Column(usersDB.Date)
    endDate = usersDB.Column(usersDB.Date)
    isVirtual = usersDB.Column(usersDB.Boolean)
