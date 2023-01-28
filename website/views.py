""" Service related functions """
from flask import Blueprint, render_template

views = Blueprint("views", __name__)

@views.route("/")
@views.route("home")
def home():
    return render_template("home.html")


@views.route("/map")
def map():
    # Get saved locations from user
    saved = []
    return render_template("map.html", markers=saved)
