import json
import datetime
from collections import defaultdict
import matplotlib.pyplot as plt

class User:
    def __init__(self, name, age, weight, height, goals=[], workout_logs=[]):
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height
        self.goals = goals
        self.workout_logs = workout_logs

class Exercise:
    def __init__(self, name, category, duration, calories_burned):
        self.name = name
        self.category = category
        self.duration = duration
        self.calories_burned = calories_burned

class WorkoutLog:
    def __init__(self, exercise, date, duration):
        self.exercise = exercise
        self.date = date
        self.duration = duration

def load_user_data(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            user = User(**data)
            user.workout_logs = [WorkoutLog(Exercise(**log['exercise']), log['date'], log['duration']) for log in data['workout_logs']]
            return user
    except FileNotFoundError:
        return None

def save_user_data(user, file_path):
    data = user.__dict__.copy()
    data['workout_logs'] = [log.__dict__.copy() for log in user.workout_logs]
    for log in data['workout_logs']:
        log['exercise'] = log['exercise'].__dict__.copy()
    with open(file_path, 'w') as file:
        json.dump(data, file)

def log_exercise(user, exercise, duration):
    log = WorkoutLog(exercise, datetime.datetime.now().isoformat(), duration)
    user.workout_logs.append(log)
    save_user_data(user, f'{user.name}_data.json')

def generate_workout_summary(user):
    workout_summary = []
    exercise_logs = defaultdict(list)
    total_calories = 0

    for log in user.workout_logs:
        date = datetime.datetime.fromisoformat(log.date).strftime('%m/%d/%Y')
        calories_burned = log.exercise.calories_burned * log.duration
        total_calories += calories_burned
        exercise_logs[date].append((log.exercise.name, calories_burned))

    workout_summary.append(f"{'=' * 20} Workout Summary {'=' * 20}")
    workout_summary.append(f"User Info:")
    workout_summary.append(f"Name: {user.name}")
    workout_summary.append(f"Age: {user.age}")
    workout_summary.append(f"Weight: {user.weight} lbs")
    workout_summary.append(f"Height: {user.height} inches")
    workout_summary.append("")

    for date, logs in exercise_logs.items():
        workout_summary.append(f"Date: {date}")
        for exercise, calories in logs:
            workout_summary.append(f"Exercise '{exercise}' burned {calories} calories")
        workout_summary.append("")  # Empty line for formatting

    workout_summary.append(f"Total calories burned: {total_calories}")

    # Create a simple bar chart for calories burned per exercise
    exercises = [log[0] for logs in exercise_logs.values() for log in logs]
    calories_burned = [log[1] for logs in exercise_logs.values() for log in logs]

    plt.figure(figsize=(10, 6))
    plt.bar(exercises, calories_burned, color='blue')
    plt.xlabel('Exercise')
    plt.ylabel('Calories Burned')
    plt.title('Calories Burned per Exercise')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the plot as an image and append the filename to the workout summary
    image_path = f'{user.name}_workout_summary.png'
    plt.savefig(image_path)
    plt.close()

    workout_summary.append(f"\nWorkout Summary Graph: {image_path}")
    workout_summary.append(f"{'=' * 50}")

    return "\n".join(workout_summary)

def get_user_info():
    name = input("Enter your name: ")
    age = int(input("Enter your age: "))
    weight = float(input("Enter your weight (lbs): "))
    height = float(input("Enter your height (inches): "))
    return User(name, age, weight, height)

def main():
    user = None

    while True:
        if not user:
            user = get_user_info()
        print("\n1. Log Exercise\n2. View Workout Summary\n3. Save and Exit\nEnter your choice: ")

        choice = input()

        if choice == '1':
            name = input("Enter exercise name: ")
            category = input("Enter exercise category (e.g., Cardio, Strength): ")
            duration = float(input("Enter duration in minutes: "))
            calories_burned = float(input("Enter calories burned per minute: "))
            exercise = Exercise(name, category, duration, calories_burned)
            log_exercise(user, exercise, duration)
            print("Exercise logged successfully!")

        elif choice == '2':
            workout_summary = generate_workout_summary(user)
            print(workout_summary)

        elif choice == '3':
            save_user_data(user, f'{user.name}_data.json')
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()