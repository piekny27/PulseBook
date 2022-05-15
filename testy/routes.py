from flask import redirect, render_template, url_for, flash, request
from testy import app

@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html")

@app.route("/dashboard")
def dashboard_page():
    return render_template("dashboard.html")