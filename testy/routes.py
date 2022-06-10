from ast import match_case
from calendar import month
import datetime
from flask import redirect, render_template, url_for, flash, request
from flask_login import current_user, login_user, logout_user
from sqlalchemy import JSON
from testy import app
from testy.forms import LoginForm, RegisterForm, ProfileForm, DeviceForm
from testy.models import DBConnection, Hr_data, Measurement, Sp_data, User, UserProfile, Device
from pprint import pprint
import json
import time
import math
import jsonpickle
from json import JSONEncoder

db = DBConnection()

@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html")

@app.route("/contact")
def contact_page():
    return render_template("contact.html")

@app.route("/login", methods=['GET', 'POST'])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
             user = User.query.filter_by(email=form.username.data).first()
        if (user and user.VerifyPassword(attemptedPassword = form.password.data)):
            login_user(user)
            return redirect(url_for('dashboard_page'))
    return render_template("login.html", form=form)

@app.route("/register", methods=['GET', 'POST'])
def register_page():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    form = RegisterForm()
    if form.validate_on_submit():
        newProfile = UserProfile()
        newDevice = Device()
        db.AddProfile(newProfile)
        db.AddDevice(newDevice)
        db.Flush()
        newUser = User(username=form.username.data,
                       email=form.emailAddress.data,
                       password=form.password1.data,
                       roleId=1, profileId = newProfile.id,
                       deviceId = newDevice.id)
        db.AddUser(newUser)  
        db.Flush()
        login_user(newUser)
        return redirect(url_for('dashboard_page'))
    return render_template("register.html", form=form)

@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard_page():
    class Measure:
        def __init__(self, date, hr_val, sp_val):
            self.date = date
            self.hr_val = hr_val
            self.sp_val = sp_val
    if not current_user.is_authenticated:
        return redirect(url_for('home_page'))
    range = request.form.get('range')
    match range:
        case 'last_week':
            current_time = datetime.datetime.utcnow()
            day_ago = current_time - datetime.timedelta(weeks=1)
            measurements = UserProfile.query.filter_by(id=current_user.profileId).first().measurements.filter(Measurement.date > day_ago).all()
        case 'last_month':
            current_time = datetime.datetime.utcnow()
            day_ago = current_time - datetime.timedelta(weeks=4)
            measurements = UserProfile.query.filter_by(id=current_user.profileId).first().measurements.filter(Measurement.date > day_ago).all()
        case _:
            current_time = datetime.datetime.utcnow()
            day_ago = current_time - datetime.timedelta(weeks=1)
            measurements = UserProfile.query.filter_by(id=current_user.profileId).first().measurements.filter(Measurement.date > day_ago).all()
    dict={}
    dict['measurements']=[]
    for measure in measurements:
        m = Measure(measure.date, measure.hr_data_avg, measure.sp_data_avg)
        dict['measurements'].append(m)
    profile = current_user.profiles
    dict['bmi_value'] = profile.weight / (math.pow(profile.height/100,2))
    dict['bmi_message']="Your bmi is correct and bla bla"
    dict['pulse_value']="12"
    dict['pulse_message']="Brawo masz wysmienity puls."
    dict['chart_saturation_value']="ala"
    dict['pulse_chart_message']="Masz za krotka historie pomiarow aby ladnie pokazac"
    dictJSON = jsonpickle.encode(dict, unpicklable=False)
    return render_template("dashboard.html", dict=dict, jsondict=dictJSON)

@app.route("/logout")
def logout_page():
    logout_user()
    return redirect(url_for("home_page"))

@app.route("/profile", methods=['GET', 'POST'])
def profile_page():
    if current_user.is_authenticated:
        form = ProfileForm()
        if form.validate_on_submit():
            newProfile = UserProfile(first_name = form.first_name.data,
                            last_name = form.last_name.data,
                            dob = form.date_of_birth.data,
                            gender = form.gender.data,
                            nationality = form.nationality.data,
                            avatarName = "avatar12",
                            height = form.height.data,
                            weight = form.weight.data)
            current_profile_ID = current_user.profileId
            db.session.add(newProfile)
            db.session.commit()
            current_user.profileId = newProfile.id
            db.session.delete(UserProfile.query.filter_by(id=current_profile_ID).first())
            db.session.commit()
            return redirect(url_for('profile_page'))
        currentProfile = UserProfile.query.filter_by(id=current_user.profileId).first()
        form.first_name.data = currentProfile.first_name
        form.last_name.data = currentProfile.last_name
        form.date_of_birth.data = currentProfile.date_of_birth
        form.gender.data = currentProfile.gender
        form.nationality.data = currentProfile.nationality
        form.height.data = currentProfile.height
        form.weight.data = currentProfile.weight
        return render_template("profile.html", form=form)
    return redirect(url_for("home_page"))

@app.route("/settings", methods=['GET', 'POST'])
def settings_page():
    if current_user.is_authenticated:
        device = Device.query.filter_by(id=current_user.deviceId).first()
        if(not device):
            device = Device(config_state = 0)
            db.session.add(device)
            db.session.commit()
            current_user.deviceId = device.id
            db.session.commit()
        device_key = request.args.get('device_key')
        pin = request.args.get('pin')
        delete_device = request.args.get('delete_device')
        if device_key:
            sec = 0
            while True:
                if sec > 5:
                    return ('Request timeout', 408)
                device = Device.query.filter_by(id=current_user.deviceId).first()
                device.device_key = device_key
                db.session.commit()
                if device and device.config_state > 0:
                    return ('Ok jest', 200)
                time.sleep(1)
                sec += 1
        if pin:
            sec = 0
            while True:
                if sec > 5:
                    return ('Request timeout', 408)
                device = Device.query.filter_by(id=current_user.deviceId).first()
                device.pin = pin
                db.session.commit()
                if device and device.config_state > 1:
                    return ('Ok jest', 200)
                time.sleep(1)
                sec += 1
        if delete_device:
            devi = Device(config_state = 0)
            db.session.add(devi)
            db.session.commit()
            db.session.delete(device)
            current_user.deviceId = devi.id
            db.session.commit()
            return ('Ok jest', 200)
        return render_template("settings.html", config_state = device.config_state, serial_number=device.serial_number, version=device.version, device=device.device_key)
    return redirect(url_for("home_page"))

@app.route("/device", methods=['POST'])
def device_page():
    content = request.get_json()
    device = Device.query.filter_by(device_key=content['device_key']).first()
    #config block
    if device and device.config_state == 0:
        device.config_state = 1
        db.session.commit()
        return (json.dumps({'device_key':device.device_key}), 202, {'ContentType':'application/json'})
    elif device and device.config_state == 1:
        pin = content['pin']
        if(pin and int(pin) == device.pin):
            device.config_state = 2
            device.serial_number = content['serial_number']
            device.version = content['version']
            db.session.commit()
            return (json.dumps({'pin':device.pin}), 202, {'ContentType':'application/json'})
    #receive data block
    elif device and device.config_state == 2:  
        new_measurement = Measurement()
        for sp_item in content['sp_array[]']:
            new_measurement.sp_data.append(Sp_data(data=sp_item))
        for hr_item in content['hr_array[]']:
            new_measurement.hr_data.append(Hr_data(data=hr_item)) 
        new_measurement.hr_data_avg = sum(content['hr_array[]']) / len(content['hr_array[]'])
        new_measurement.sp_data_avg = sum(content['sp_array[]']) / len(content['sp_array[]'])
        device.user[0].profiles.measurements.append(new_measurement)
        db.session.commit()
        pass
    elif not device:
        return (json.dumps({'action':'reset'}), 200, {'ContentType':'application/json'})
    return (json.dumps({'config_state':device.config_state}), 200, {'ContentType':'application/json'})
    