""" Service related functions """
from flask import Blueprint, render_template, request, redirect, url_for, flash
from website import db, bcrypt
from website.models import Study, User, SavedMarker
from datetime import datetime, timedelta
import json
from sqlalchemy import func

EXAMPLE_USER_ID = 123456789


views = Blueprint("views", __name__)


def saveMarkers(markers):
    with open('markers.txt', 'w') as f:
        for m in markers:
            f.write(f'{m}\n')

    for item in markers:
        marker = SavedMarker(user_id=EXAMPLE_USER_ID, long=item[0], lat=item[1])
        db.session.add(marker)
        db.session.commit()

def calc_xy(y, x):
    x_axis, y_axis = [], []
    tasks_completed, time_studied = 0, 0
    end_day = datetime.today().date() 

    x_dict = {'daily_ch': 1, 'weekly_ch': 6, 'monthly_ch': 30}
    
    if not x_dict[x] == 1:
        start_day = end_day - timedelta(days=x_dict[x])
    
    for i in range(7):
        if x_dict[x] == 1:
            studies = Study.query.filter(func.DATE(Study.date) == end_day).all()
        else:
            # Extract study log data that is on the specific date
            studies = Study.query.filter(func.DATE(Study.date) >= start_day, func.DATE(Study.date) <= end_day).all()
        
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

        if x_dict[x] == 1:
            x_axis.append(end_day.strftime('%m/%d'))
            # Subtract a day
            end_day -= timedelta(days=1)
        else:
            x_axis.append(f"{start_day.strftime('%m/%d')} - {end_day.strftime('%m/%d')}")
            # Subtract a day
            end_day = start_day - timedelta(days=1)
            start_day = end_day - timedelta(days=x_dict[x])

        if y == 'hours_ch':
            y_axis.append(total_h)
            # Tasks Completed
            if i == 0:
                tasks_completed = len(studies)
                # Time Studied
                time_studied = y_axis[0]
                time_studied = f"{int(time_studied)}:{int((time_studied % 1) * 60)}"
        # End Time Studied
        else:
            y_axis.append(len(studies))
            # Tasks Completed
            tasks_completed = y_axis[0]
            if i == 0:
                time_studied = total_h
                time_studied = f"{int(time_studied)}:{int((time_studied % 1) * 60)}"




    return {'x_axis':x_axis, 'y_axis':y_axis, 'tasks_completed':tasks_completed, 'time_studied': time_studied}


@views.route("/")
@views.route("/home")
def home():
    xy_data = calc_xy('hours_ch', 'daily_ch')

    return render_template("home.html", x_axis=json.dumps(xy_data['x_axis'][::-1]), y_axis=json.dumps(xy_data['y_axis'][::-1]), time_studied=xy_data['time_studied'], tasks_completed=xy_data['tasks_completed'])



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
        # Check if user exists
        # if not, hash password and create account
        passw_hash = bcrypt.generate_password_hash(request.form['passwd']).decode('utf-8')
        user = User(name=request.form['name'], uname=request.form['uname'], email=request.form['email'], passw=passw_hash)
        db.session.add(user)
        db.session.commit()
        # pass
        return render_template('home.html')
    return render_template('create_account.html')


@views.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Check if password is correct for user
        input = request.form['user_input']
        user_entry = User.query.filter_by(uname=input).first()
        if user_entry is None:
            flash("Invalid Username or password!", "danger")
            return redirect(url_for('views.login'))

        hash = user_entry.passw
        if hash != bcrypt.generate_password_hash(request.form['passwd']).decode('utf-8'):
            flash("Invalid Username or password!", "danger")
            return redirect(url_for('views.login'))
        # load user data
        # return render_template('home.html')
    return render_template('login.html')


@views.route("/map", methods=['GET', 'POST'])
def map():
    if request.method == 'POST':
        saveMarkers(request.json['values'])
    return render_template('map.html')


@views.route("/change_chart", methods=["GET", "POST"])
def change_chart():
    if request.method == "POST":
        x_axis_ch = request.form.get('x_axis_ch')
        y_axis_ch = request.form.get('y_axis_ch')

        xy_data = calc_xy(y_axis_ch, x_axis_ch)

        print("---------------------------------------------------------", xy_data['time_studied'], xy_data['tasks_completed'])

    # TODO: UPDATE the frontend

    return redirect(url_for('views.home', x_axis=json.dumps(xy_data['x_axis'][::-1]), y_axis=json.dumps(xy_data['y_axis'][::-1]), time_studied=xy_data['time_studied'], tasks_completed=xy_data['tasks_completed']))

