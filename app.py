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
    

@app.route("/foodlist", methods=["GET", "POST"])
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

@app.route("/register", methods=["GET", "POST"])
def register():
    # Forget current user_id
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not username or not password or not confirmation:
            return apology("all fields must be filled in", 400)
        # check if username already exists
        rows = db.execute("SELECT * FROM users WHERE username = ?;", username)
        if len(rows) != 0:
            return apology("username already exists", 400)

        # check that password and confirmation match
        print(password)
        print(confirmation)
        if password != confirmation:
            return apology("passwords must match", 400)

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
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

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
