from flask import Flask
from os import path
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DB_NAME = "study-tracking.db"

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = "helloworld"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    # Register files
    from .views import views
    app.register_blueprint(views, url_prefix="/")
    # End Register files

    # Create tables
    from .models import Study
    create_db(app)
    # End Create tables

    return app

# Create a database
def create_db(app):
    if not path.exists("website/" + DB_NAME):
        db.create_all(app=app)
        print("db created.")

