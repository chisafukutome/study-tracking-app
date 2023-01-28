from . import db
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
