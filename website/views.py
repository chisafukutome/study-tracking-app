""" Service related functions """
from flask import Blueprint, render_template, request
# from flask_cors import CORS
# import json

views = Blueprint("views", __name__)
# CORS(views)


def saveMarkers(markers):
    with open('markers.txt', 'w') as f:
        for m in markers:
            f.write(f'{m}\n')    


@views.route("/")
@views.route("home")
def home():
    return render_template("home.html")


@views.route("/map", methods=['GET', 'POST'])
def map():
    if request.method == 'POST':
        saveMarkers(request.json['values'])
    return render_template('map.html')
