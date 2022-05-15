from flask import redirect, render_template, url_for, flash, request
from testy import app

@app.route("/")
@app.route("/index")
def home_page():
    return render_template("index.html")