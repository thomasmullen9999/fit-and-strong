from cs50 import SQL
from datetime import date

from flask import Flask, redirect, render_template, request, session
from flask_session import Session

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///fitness.db")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/exercise")
def exercise():
    return render_template("exercise.html")

@app.route("/exerciselist", methods=["GET", "POST"])
def exerciselist():
    if request.method == "POST":
      name = request.form.get("exercise-name")
      desc = request.form.get("exercise-desc")
      muscles = request.form.get("exercise-muscles")

      db.execute(
        """INSERT INTO "exercises" ("name", "description", "muscles_used")
        VALUES (?, ?, ?)""",
        name, desc, muscles
      )
      return redirect("/exerciselist")
    else:
      exercises = db.execute("SELECT * FROM exercises;")
      return render_template("exerciselist.html", exercises=exercises)

@app.route("/workoutlog", methods=["GET", "POST"])
def workoutlog():
  if request.method == "POST":
    db.execute(
      """INSERT INTO "workouts" ("date", "user_id")
      VALUES (?, ?)""",
      date.today(), "placeholder"
    )
    return redirect("/workoutlog")
  else:
    workouts = db.execute("SELECT * FROM workouts;")
    return render_template("workoutlog.html", workouts=workouts)

@app.route("/foodlog")
def foodlog():
    return render_template("foodlog.html")

@app.route("/mystats")
def mystats():
    return render_template("mystats.html")




