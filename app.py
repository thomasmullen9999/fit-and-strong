from cs50 import SQL
from datetime import date

from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///fitness.db")

def error(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("error.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/exercise")
@login_required
def exercise():
    return render_template("exercise.html")

@app.route("/tips")
@login_required
def tips():
    return render_template("tips.html")

@app.route("/exerciselist", methods=["GET", "POST"])
@login_required
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
    

@app.route("/foodlist", methods=["GET", "POST"])
@login_required
def foodlist():
    if request.method == "POST":
      name = request.form.get("food-name")
      protein = request.form.get("food-protein")
      carbs = request.form.get("food-carbs")
      fat = request.form.get("food-fat")
      calories = request.form.get("food-calories")

      db.execute(
        """INSERT INTO "foods" ("name", "protein_per_hundred_grams", "carbs_per_hundred_grams", "fat_per_hundred_grams", "calories_per_hundred_grams")
        VALUES (?, ?, ?, ?, ?)""",
        name, protein, carbs, fat, calories
      )
      return redirect("/foodlist")
    else:
      foods = db.execute("SELECT * FROM foods;")
      return render_template("foodlist.html", foods=foods)

@app.route("/workoutlog", methods=["GET", "POST"])
@login_required
def workoutlog():
  print(request.method)
  if request.method == "POST":
    username = db.execute(
        """SELECT username FROM users
        WHERE id = ?;""",
        session["user_id"]
    )
    
    try:
      db.execute(
        """INSERT INTO "workouts" ("date", "user_id")
        VALUES (?, ?);""",
        date.today(), session["user_id"]
      )
      return redirect("/workoutlog")
    except ValueError:
       return error("only one workout can be entered per day", 400)
  else:
    exercises = db.execute("SELECT * FROM exercises;")
    workouts = db.execute("SELECT * FROM workouts WHERE user_id = ?;", session["user_id"])
    exercise_instances = db.execute("SELECT * FROM exercise_instances;")
    return render_template("workoutlog.html", workouts=workouts, exercise_instances = exercise_instances, exercises=exercises)

@app.route("/fooddiary", methods=["GET", "POST"])
@login_required
def fooddiary():
  if request.method == "POST":
    username = db.execute(
        """SELECT username FROM users
        WHERE id = ?;""",
        session["user_id"]
    )
    db.execute(
      """INSERT INTO "food_logs" ("date", "user_id")
      VALUES (?, ?)""",
      date.today(), username[0]["username"]
    )
    return redirect("/fooddiary")
  else:
    foodlogs = db.execute("SELECT * FROM food_logs;")
    return render_template("fooddiary.html", foodlogs=foodlogs)

@app.route("/mystats", methods=["GET", "POST"])
@login_required
def mystats():
  if request.method == "POST":
    weight = request.form.get("weight")
    steps = request.form.get("steps")
    username = db.execute(
        """SELECT username FROM users
        WHERE id = ?;""",
        session["user_id"]
    )
    db.execute(
      """INSERT INTO "stats" ("weight_kg", "steps", "date")
      VALUES (?, ?, ?)""",
      weight, steps, date.today()
    )
    return redirect("/mystats")
  else:
    stats = db.execute("SELECT * FROM stats;")
    return render_template("mystats.html", stats=stats)

@app.route("/register", methods=["GET", "POST"])
def register():
    # Forget current user_id
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not username or not password or not confirmation:
            return error("all fields must be filled in", 400)
        # check if username already exists
        rows = db.execute("SELECT * FROM users WHERE username = ?;", username)
        if len(rows) != 0:
            return error("username already exists", 400)

        # check that password and confirmation match
        if password != confirmation:
            return error("passwords must match", 400)

        db.execute("INSERT INTO users (username, hash) VALUES (?, ?);",
                   username, generate_password_hash(password))
        return redirect("/login")

    else:
        return render_template("register.html")
    

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return error("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return error("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return error("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    # Forget current user_id
    session.clear()
    # Return user to login page
    return redirect("/")

@app.route('/deleteworkout/<int:id>', methods=['POST'])
@login_required
def delete_workout(id):
    db.execute(
      """DELETE FROM "workouts"
      WHERE id = ?;""",
      id
    )
    return redirect("/workoutlog")

@app.route('/addexercise/<int:workout_id>', methods=['POST'])
@login_required
def add_exercise(workout_id):
    weight = request.form.get("weight")
    sets = request.form.get("sets")
    reps = request.form.get("reps")
    name = request.form.get("exercise-name")
    if not weight or not name or not sets or not reps:
       return error("all form fields must be entered", 400)
    db.execute(
      """INSERT INTO "exercise_instances" ("workout_id", "exercise_name", "weight_kg", "sets", "reps")
      VALUES (?, ?, ?, ?, ?);""",
        workout_id, name, weight, sets, reps
    )
    return redirect("/workoutlog")

@app.route('/deleteexercise/<int:id>', methods=['POST'])
@login_required
def delete_exercise(id):
    db.execute(
      """DELETE FROM "exercises"
      WHERE id = ?;""",
      id
    )
    return redirect("/exerciselist")

@app.route('/filteredexerciselist', methods=['GET'])
@login_required
def filter_exercise_list():
    musclefilter = request.args.get("musclefilter")
    filteredExercises = db.execute(
      """SELECT * FROM "exercises" WHERE muscles_used LIKE ?;
      """, musclefilter
    )
    print(filteredExercises)
    return render_template("exerciselist.html", exercises=filteredExercises)