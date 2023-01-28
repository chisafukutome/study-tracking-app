""" Service related functions """
from flask import Blueprint, render_template, request, redirect, url_for
from . import db
from .models import Study
from datetime import datetime

views = Blueprint("views", __name__)


def saveMarkers(markers):
    with open('markers.txt', 'w') as f:
        for m in markers:
            f.write(f'{m}\n')    


@views.route("/")
@views.route("home")
def home():
    return render_template("home.html")

@views.route("/log_study", methods=['GET', 'POST'])
def log_study():
    # Get data from study_log.html
    if request.method == "POST":
        date = datetime.strptime(request.form.get('date'), "%Y-%m-%d")
        task = request.form.get('task')
        amount = request.form.get('amount')
        unit = request.form.get('unit')
        duration_h = request.form.get('duration_h')
        duration_m = request.form.get('duration_m')
        location = request.form.get('location')

        # Add to db
        study = Study(date=date, task=task, amount=amount, unit=unit, duration_h=duration_h, duration_m=duration_m, location=location)
        db.session.add(study)
        db.session.commit()

        return redirect(url_for('views.home'))
        
    return render_template("study_log.html")




@views.route("/map", methods=['GET', 'POST'])
def map():
    if request.method == 'POST':
        saveMarkers(request.json['values'])
    return render_template('map.html')
