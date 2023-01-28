from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from os import path

STUDY_DB = "study-tracking.db"
USER_DB = "user.db"
MARKERS_DB = "user_markers.db"
db = SQLAlchemy(session_options={"autoflush": False})
# DB_NAME = "study-tracking.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'helloworld'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{STUDY_DB}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_BINDS'] = {
        'user': f'sqlite:///{USER_DB}',
        'markers': f'sqlite:///{MARKERS_DB}'
    }
    bcrypt = Bcrypt(app)

    db.init_app(app)



    # Create tables
    from .models import Study
    create_db(app)
    # End Create tables

    # Register files
    from .views import views
    app.register_blueprint(views, url_prefix="/")
    # End Register files
    return app

# Create a database
def create_db(app):
    if not path.exists("website/" + STUDY_DB):
        db.create_all(app=app)
        print("db created.")
