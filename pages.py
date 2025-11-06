from flask import Flask, render_template
from data import verify_user

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("index.html")
