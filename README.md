# Fit and Strong
#### Video Demo:  <URL HERE>
#### Description:

## Introduction

For my final project in CS50x, I decided to create a Flask application using Python, SQLite and Jinja. I wanted to create a web-based fitness application 
which combines several features of already-existing software, such as the ability to track your diet (including your daily intake of calories and 
macronutrients), the ability to record all of your workouts, and also the ability to keep track of your daily weight, steps taken and hours of sleep.

I wanted users to be able to create an account and then log in and out. To achieve this, I used some of the helper functions provided by the CS50 staff
in Problem Set 9, including the apology function (renamed to error) and the login_required function.

A database called fitness.db was created to store information about users, individual exercises, foods, workouts, stats and more. To keep a record of the 
queries and create statements which are used to initialise and populate the tables in this database, I created schema.sql. This file contains all of the
necessary code to get the database up and running before any users can interact with it.

My website has the following sections: 

### Home

Self-explanatory, the homepage of the website which contains a welcome message and brief descriptions of the other sections of the site.

### Exercise List

A table of strength training exercises, linked to the 'exercises' table in fitness.db. Each exercise has a name, a description and a field naming the muscles used in the exercise. A user can filter the list by muscles used, add a new exercise (description optional) or simply browse the list. 

### Workout Log

A list of workouts listed by date, each one with its own table. A user can delete an already-existed workout, or add a new one for the current date. For each workout, 
a user can add exercises, including the name of the exercise, the weight used, and the number of sets and reps performed.

### Food List

A table of foods, linked to the 'foods' table in fitness.db. Each food has a name, and the amount of calories, protein, fat and carbs per 100g of the food. A user can add a new food or filter by...

### Food Diary



### My Stats

Information on the current users health stats, including recent entries for weight, number of steps and hours of sleep. A user can add a new entry for the current date or remove an entry entirely. 

### Tips

A selection of tips regarding diet and training for users trying to get in shape.

### Contact

Details on how to get in touch with me via email, GitHub and LinkedIn.

