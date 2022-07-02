import datetime
from flask import redirect, render_template, url_for, request
from flask_login import current_user, login_user, logout_user
from testy import app
from testy.dashboard import Dashboard
from testy.forms import LoginForm, RegisterForm, ProfileForm
from testy.models import Avatar, DBConnection, Hr_data, Measurement, Sp_data, User, UserProfile, Device
from testy.models import Dashboard as DashboardModel
import json
import time
import cloudinary
import cloudinary.uploader
from cloudinary import CloudinaryImage, api

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
        if user:
            if (user.VerifyPassword(attemptedPassword = form.password.data)):
                login_user(user)
                return redirect(url_for('dashboard_page'))
            form.password.errors.append('The password is incorrect.')
        else:
            user = User.query.filter_by(email=form.username.data).first()
            if not user:
                form.username.errors.append('The username or email address is incorrect.')           
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
        newDashboard = DashboardModel()
        db.AddDashboard(newDashboard)
        db.Flush()
        newUser = User(username=form.username.data,
                       email=form.emailAddress.data,
                       password=form.password1.data,
                       roleId=1, profileId = newProfile.id,
                       deviceId = newDevice.id,
                       dashboard_id = newDashboard.id)
        db.AddUser(newUser)  
        db.Flush()
        login_user(newUser)
        return redirect(url_for('dashboard_page'))
    return render_template("register.html", form=form)

@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard_page():
    if not current_user.is_authenticated:
        return redirect(url_for('home_page'))
    range = request.form.get('range')
    dashboard = Dashboard(current_user, range)
    return render_template("dashboard.html", cards=dashboard.cards)

@app.route("/logout")
def logout_page():
    logout_user()
    return redirect(url_for("home_page"))

@app.route("/profile", methods=['GET', 'POST'])
def profile_page():
    if current_user.is_authenticated:
        form = ProfileForm()
        if form.validate_on_submit():
            profile = UserProfile.query.filter_by(id=current_user.profileId).first()
            profile.first_name = form.first_name.data
            profile.last_name = form.last_name.data
            profile.dob = form.date_of_birth.data
            profile.gender_id = form.gender.data
            profile.nationality_id = form.nationality.data
            profile.height = form.height.data
            profile.weight = form.weight.data
            db.session.commit()
            return redirect(url_for('profile_page'))
        currentProfile = UserProfile.query.filter_by(id=current_user.profileId).first()
        form.gender.default = currentProfile.gender_id
        form.nationality.default = currentProfile.nationality_id
        form.process()
        form.first_name.data = currentProfile.first_name
        form.last_name.data = currentProfile.last_name
        form.date_of_birth.data = currentProfile.date_of_birth
        form.height.data = currentProfile.height
        form.weight.data = currentProfile.weight
        if request.args.get('remove') == 'True':
            if current_user.profiles.avatars.name != Avatar.DEFAULT:
                cloudinary.api.delete_resources(current_user.profiles.avatars.name)
                db.session.delete(current_user.profiles.avatars)
                current_user.profiles.avatar_id = Avatar.query.filter_by(name=Avatar.DEFAULT).first().id
                db.Flush()
        if request.method == 'POST':
            if 'file' in request.files:
                file_to_upload = request.files['file']
                app.logger.info('%s file_to_upload', file_to_upload)
                if file_to_upload:
                    upload_result = cloudinary.uploader.upload(file_to_upload, folder="media")
                    app.logger.info(upload_result)
                    if 'public_id' in upload_result:
                        avatar = Avatar(name=upload_result['public_id'])
                        if current_user.profiles.avatars.name != Avatar.DEFAULT:
                            cloudinary.api.delete_resources(current_user.profiles.avatars.name)
                            db.session.delete(current_user.profiles.avatars)
                            db.Flush()
                        db.session.add(avatar)
                        db.Flush()
                        current_user.profiles.avatar_id = avatar.id
                        db.Flush()
                        return render_template("profile.html", form=form, modal=upload_result['url'])
            if 'width' in request.form:
                options ={}
                options['height'] = request.form['height']
                options['width'] = request.form['width']
                options['x'] = request.form['x']
                options['y'] = request.form['y']
                current_user.profiles.avatars.options = json.dumps(options)
                db.Flush()
                return render_template("profile.html", form=form)
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
        settings = request.form.get('settings')
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
        if settings == 'delete_account':
            profile_id = current_user.profileId
            device_id = current_user.deviceId
            logout_user()
            db.session.delete(UserProfile.query.filter_by(id=profile_id).first())
            db.session.delete(Device.query.filter_by(id=device_id).first())
            db.session.commit()
            return redirect(url_for('home_page'))
        return render_template("settings.html", device=device)
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
        return (json.dumps({'action':'reset'}), 205, {'ContentType':'application/json'})
    return (json.dumps({'config_state':device.config_state}), 200, {'ContentType':'application/json'})
    