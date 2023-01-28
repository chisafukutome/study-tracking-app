from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os

STUDY_DB = "study-tracking.db"
USER_DB = "user.db"
MARKERS_DB = "user_markers.db"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'helloworld'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{STUDY_DB}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_BINDS'] = {
    'user': f'sqlite:///{USER_DB}',
    'markers': f'sqlite:///{MARKERS_DB}'
}
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from website import views
