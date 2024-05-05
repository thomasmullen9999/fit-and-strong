-- Create tables

-- Represent a list of exercises
CREATE TABLE "exercises" (
  "id" INTEGER,
  "name" TEXT NOT NULL,
  "description" TEXT NOT NULL,
  "muscles_used" TEXT NOT NULL,
  PRIMARY KEY("id")
);

-- Represent a list of users' workouts
CREATE TABLE "workouts" (
  "id" INTEGER,
  "date" TEXT NOT NULL,
  "user_id" TEXT NOT NULL,
  PRIMARY KEY("id")
);

-- Represent a list of exercise instances, each with a workout id
CREATE TABLE "exercise_instances" (
  "id" INTEGER,
  "workout_id" TEXT NOT NULL,
  "exercise_name" TEXT NOT NULL,
  "sets" INTEGER,
  "reps" INTEGER,
  PRIMARY KEY("id"),
  FOREIGN KEY("workout_id") REFERENCES "workouts"("id")
);

-- Represent users' food instances
CREATE TABLE "food_instances" (
  "id" INTEGER,
  "food_id" INTEGER,
  "food_name" TEXT NOT NULL,
  "amount_grams" INTEGER,
  "protein_grams" INTEGER,
  "carbs_grams" INTEGER,
  "fat_grams" INTEGER,
  "calories" INTEGER,
  PRIMARY KEY("id"),
  FOREIGN KEY("food_id") REFERENCES "foods"("id")
);

-- Represent a list of foods
CREATE TABLE "foods" (
  "id" INTEGER,
  "name" TEXT NOT NULL,
  "protein_per_hundred_grams" INTEGER,
  "carbs_per_hundred_grams" INTEGER,
  "fat_per_hundred_grams" INTEGER,
  "calories_per_hundred_grams" INTEGER,
  PRIMARY KEY("id")
);

-- Represents a list of users' stats for each date
CREATE TABLE "stats" (
  "id" INTEGER,
  "date" TEXT NOT NULL,
  "weight_kg" REAL,
  "steps" INTEGER,
  PRIMARY KEY("id")
);

-- Populate the exercises table with a default list of exercises
INSERT INTO "exercises" ("name", "description", "muscles_used")
VALUES
("Barbell Bench Press", "Lie on a flat bench with your feet flat on the floor. Grasp the bar a little wider than shoulder width apart. Start by raising the barbell above your body and move it over the middle of your chest. Lower the bar down so it touches your chest. Raise the bar till your arms are fully extended and your elbows are locked.", "Chest, Shoulders, Triceps"),
("Dumbbell Hammer Curls", "Stand with your feet shoulder width apart, your knees slightly bent and your abs drawn in. Grasp a dumbbell in each hand so your palms are facing each other. Extend your arms so they are at the sides of your body. Keeping your elbows locked lift your arms in an arc towards your shoulders. Lower your arms in a steady controlled motion and repeat.", "Biceps");

-- Populate the exercises table with a default list of foods
INSERT INTO "foods" ("name", "protein_per_hundred_grams", "carbs_per_hundred_grams", "fat_per_hundred_grams", "calories_per_hundred_grams")
VALUES
("John West Tuna", 30, 200, 15, 254);