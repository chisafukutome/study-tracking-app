from website import db
from sqlalchemy.sql import func


class Study(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    task = db.Column(db.String(150), nullable=False)
    amount = db.Column(db.Integer, default=0)
    unit = db.Column(db.String(150))
    duration_h = db.Column(db.Integer, default=0)
    duration_m = db.Column(db.Integer, default=0)

    # TODO: unique with id
    location = db.Column(db.String(150))

    # def __init__(self, id, date, task, amount, unit, duration_h, duration_m, loc):
    #     self.id = id
    #     self.date = date
    #     self.task = task
    #     self.amount = amount
    #     self.unit = unit
    #     self.duration_h = duration_h
    #     self.duration_m = duration_m
    #     self.location = loc


class User(db.Model):
    __bind_key__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    uname = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    passw = db.Column(db.Integer, nullable=False)


class SavedMarker(db.Model):
    __bind_key__ = 'markers'
    marker_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    long = db.Column(db.Integer)
    lat = db.Column(db.Integer)
