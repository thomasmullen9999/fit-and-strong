# StrengthSync

#### Video Demo: https://www.youtube.com/watch?v=eT_UZQMsg3o

## Introduction

For my final project in CS50x, I decided to create a Flask application using Python, SQLite and Jinja. I wanted to create a web-based fitness application
which combines several features of already-existing software, such as the ability to track your diet (including your daily intake of calories and
macronutrients), the ability to record all of your workouts, and also the ability to keep track of your daily weight, steps taken and hours of sleep.

I wanted users to be able to create an account and then log in and out, and for the page to render an error message when certain criteria were not met. To achieve this, I borrowed some of the helper functions provided by the CS50 staff in Problem Set 9, including the apology function (renamed to error) and the login_required function. The error function was used to produce a relevant error message whenever a user does something incorrectly (such as neglect one or more required input fields in a form), and the login_required function ensures that a user is logged in before trying to access particular sections of the site.

A database called fitness.db was created to store relevant information for the application: The following tables were created in the database:

- users - stores information on the various users of the site
- exercises - stores information on a list of strength training exercises with data on name, description and muscles used
- workouts - stores information about users' workouts, including date
- exercise_instances - stores information about individual instances of an exercise with a link to its respective workout
- foods - stores information on a list of foods with nutritional information about calories, protein, fat and carbs per one hundred grams
- food_logs - stores information on users' food intake on a particular date
- food_instances - stores information about how much of a food was eaten by a user on a particular date, with a link to its specific food log
- stats - stores information on users' weight, steps and sleep for a particular date

Both the exercises and foods tables were given some default items for the user to view from the start.
To keep a record of the queries and create/insert statements which are used to initialise and populate the tables in this database, I created schema.sql.
This file contains all of the necessary code to get the database up and running before any users can start to interact with it.

## Files

My application contains the following sections:

#### Home (index.html)

Self-explanatory, the homepage of the website which contains a welcome message and brief descriptions of the other sections of the site.

#### Exercise List (exerciselist.html)

A table of strength training exercises, linked to the 'exercises' table in fitness.db. Each exercise has a name, a description and a field naming the muscles used in the exercise. A user can filter the list by muscles used, add a new exercise (description optional) or simply browse the list.

#### Workout Log (workoutlog.html)

A list of workouts listed by date, each one with its own table. A user can delete an already-existing workout, or add a new one for the current date. For each workout,
a user can add exercises, including the name of the exercise, the weight used, and the number of sets and reps performed.

#### Food List (foodlist.html)

A table of foods, linked to the 'foods' table in fitness.db. Each food has a name, and the amount of calories, protein, fat and carbs per 100g of the food. A user can add a new food, or remove one already in the list.

#### Food Diary (fooddiary.html)

A series of entries which a user can use to record information on which foods they have eaten on a particular day. They can select a food from the list of foods already registered, and enter the amount eaten (in grams). The protein/fat/carbs/calories per 100g from the food list are used to calculate the amount of each in the diary, depending on the amount. A user can remove an individual food from an entry, or remove an entry entirely.

#### My Stats (mystats.html)

Information on the current users' health stats, including recent entries for weight, number of steps and hours of sleep. A user can add a new entry for the current date or remove an entry entirely.

#### Tips (tips.html)

A selection of tips regarding diet and training for users trying to get in shape.

#### Contact (contact.html)

Details on how to get in touch with me via email, GitHub and LinkedIn.

In addition to these main sections, several more files were created:

- layout.html, which contains the basic layout which all of the template pages inherit from. This includes a navigation bar with links to all of the different sections, and the footer.

- error.html, which responds with an appropriate error message when the user hasn't filled in a form as expected.

- register.html, which allows the user to create an account.

- login.html, which allows the the user to log in to their account.

- style.css, which contains all of the styling for the web pages.

- fitness.db, which contains the database that the application uses

- schema.sql, which contains some CREATE and INSERT statements for producing the necessary tables in fitness.db
