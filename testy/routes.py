from flask import redirect, render_template, url_for, flash, request
from testy import app

@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def home_page():
    return render_template("home.html", is_authenticated=True)

@app.route("/dashboard")
def dashboard_page():
    return render_template("dashboard.html")