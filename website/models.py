from website import db
from sqlalchemy.sql import func


class Study(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=func.now())
    task = db.Column(db.String(150), nullable=False)
    amount = db.Column(db.Integer, default=0)
    unit = db.Column(db.String(150))
    duration_h = db.Column(db.Integer, default=0)
    duration_m = db.Column(db.Integer, default=0)

    # TODO: unique with id
    location = db.Column(db.String(150))


class User(db.Model):
    __bind_key__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    uname = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    passw = db.Column(db.String(50), nullable=False, unique=False)


class SavedMarker(db.Model):
    __bind_key__ = 'markers'
    marker_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    long = db.Column(db.Integer)
    lat = db.Column(db.Integer)
