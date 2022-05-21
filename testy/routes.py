from flask import redirect, render_template, url_for, flash, request
from flask_login import current_user, login_user, logout_user
from testy import app
from testy.forms import LoginForm, RegisterForm, ProfileForm
from testy.models import DBConnection, User, UserProfile
from pprint import pprint

db = DBConnection()

@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html")

@app.route("/login", methods=['GET', 'POST'])
def login_page():
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
        db.AddProfile(newProfile)
        db.Flush()
        newUser = User(username=form.username.data,
                       email=form.emailAddress.data,
                       password=form.password1.data,
                       roleId=1, profileId = newProfile.id)
        db.AddUser(newUser)  
        db.Flush()
        login_user(newUser)
        return redirect(url_for('dashboard_page'))
    return render_template("register.html", form=form)

@app.route("/dashboard")
def dashboard_page():
    return render_template("dashboard.html")

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
