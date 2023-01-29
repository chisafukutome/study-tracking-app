from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from os import path


STUDY_DB = "study-tracking.db"
USER_DB = "user.db"
MARKERS_DB = "user_markers.db"
db = SQLAlchemy(session_options={"autoflush": False})
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'helloworld'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{STUDY_DB}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_BINDS'] = {
        'user': f'sqlite:///{USER_DB}',
        'markers': f'sqlite:///{MARKERS_DB}'
    }
    db.init_app(app)
    bcrypt.init_app(app)

    # Create tables
    from .models import Study, User, SavedMarker
    create_db(app)
    # End Create tables

    # Register files
    from .views import views
    app.register_blueprint(views, url_prefix="/")
    # End Register files
    return app


# Create a database
def create_db(app):
    databases = [STUDY_DB, USER_DB, MARKERS_DB]
    if not all(path.exists("instance/" + p) for p in databases):
        with app.app_context():
            db.create_all()
        print("db created.")
