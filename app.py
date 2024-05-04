from flask import Flask, redirect, render_template, request, session
from flask_session import Session

# Configure application
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


