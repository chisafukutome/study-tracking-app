""" Service related functions """
from flask import Blueprint, render_template, request, redirect, url_for, flash
from website import db, bcrypt
from website.models import Study, User, SavedMarker
from datetime import datetime, timedelta
import json
import sys
from website.user import UserData
from sqlalchemy import func

# EXAMPLE_USER_ID = 123456789
CURR_USER = UserData(None)


views = Blueprint("views", __name__)


def load_user_data(input):
    CURR_USER.login(User.query.filter_by(id=input).first())


def check_user_exists(input):
    user_entry = User.query.filter_by(uname=input).all()
    if len(user_entry) == 0:
        user_entry = User.query.filter_by(email=input).all()
        if len(user_entry) == 0:
            return None
    return user_entry


def saveMarkers(markers):
    for item in markers:
        marker = SavedMarker(user_id=CURR_USER.data.id, long=item[0], lat=item[1])
        db.session.add(marker)
        db.session.commit()


@views.route("/")
@views.route("/home")
def home():
    x_axis, y_axis = [], []
    day = datetime.today().date()
    for i in range(7):
        # Extract study log data that is on the specific date
        studies = Study.query.filter(func.DATE(Study.date) == day).all()

        total_h = 0
        if studies:

            for study in studies:

                # if there is no value, assign 0
                study.duration_h = 0 if type(study.duration_h) == str else study.duration_h
                study.duration_m = 0 if type(study.duration_m) == str else study.duration_m

                # add duration
                total_h += study.duration_h * 60 + study.duration_m

            # Convert into hour
            total_h = 0 if total_h == 0 else total_h / 60
        y_axis.append(total_h)
        x_axis.append(day.strftime('%m/%d'))
        # Subtract a day
        day -= timedelta(days=1)

        # Time Studied
        weekly_total = sum(y_axis)
        weekly_total = f"{int(weekly_total)}:{int((weekly_total % 1) * 60)}"
        # End Time Studied

        # Tasks Completed
        # tasks_completed = Study.query.filter(Study.)
        # End Tasks Completed

    return render_template("home.html", x_axis=json.dumps(x_axis[::-1]), y_axis=json.dumps(y_axis[::-1]), weekly_total=weekly_total)


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


@views.route("/create_account", methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        if check_user_exists(request.form['uname']) or check_user_exists(request.form['email']):
            flash("Username/email already in use!", "danger")
            return redirect(url_for('views.create'))

        passw_hash = bcrypt.generate_password_hash(request.form['passwd']).decode('utf-8')
        user = User(
            name=request.form['name'],
            uname=request.form['uname'],
            email=request.form['email'],
            passw=passw_hash
        )
        db.session.add(user)
        db.session.commit()

        return redirect('home')
    return render_template('create_account.html')


@views.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_entry = check_user_exists(request.form['user_input'])
        if user_entry is None or not bcrypt.check_password_hash(user_entry[0].passw, request.form['passwd']):
            flash("Invalid Username or password1", "danger")
            return redirect(url_for('login'))

        load_user_data(user_entry[0].id)
        return redirect('home')
    return render_template('login.html')


@views.route("/map", methods=['GET', 'POST'])
def map():
    if request.method == 'POST':
        saveMarkers(request.json['values'])

    if CURR_USER.id:
        coords = []
        markers = SavedMarker.query.filter_by(user_id=CURR_USER.id).all()
        for m in markers:
            coords.append([m.long, m.lat])
        print(coords, file=sys.stderr)
        return render_template('map.html', saved=coords)

    return render_template('map.html')

@views.route("/virtual study space", methods=['GET', 'POST'])
def virtual_study_space():
    # Get data from virtual_study_space.html
    if request.method == "POST":
        return redirect(url_for('views.home'))

    return render_template("virtual_study_space.html")