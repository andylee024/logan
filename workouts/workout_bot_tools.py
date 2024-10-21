import dotenv
import openai
import os

from datetime import datetime, timedelta

import database.db_operations as db_ops
import workout_schema

dotenv.load_dotenv()
client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# 
# workout getters
#
def _get_week_start_and_end_dates(date):
    """Gets the start and end dates for the current week."""
    reference_date = datetime.strptime(date, "%Y-%m-%d")
    start_date = reference_date - timedelta(days=reference_date.weekday())
    end_date = start_date + timedelta(days=6)
    return start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")


def get_this_weeks_workouts(user_session_info):
    """Gets all workouts for a user in the current week."""
    user_id = user_session_info.get("user_id")
    user_workouts = db_ops.get_workouts_for_user(user_id)

    user_date = user_session_info.get("date")
    start_date, end_date = _get_week_start_and_end_dates(user_date)
    start_date_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_date_dt = datetime.strptime(end_date, "%Y-%m-%d")

    filtered_workouts = [
        w for w in user_workouts
        if start_date_dt <= datetime.strptime(w['date'], "%Y-%m-%d") <= end_date_dt
    ]
    return filtered_workouts

def get_most_likely_workout(user_session_info):
    """Gets the most likely workout for a user."""
    workouts = get_this_weeks_workouts(user_session_info)
    workouts = [w for w in workouts if w['status'] == 'not_started']

    user_date = datetime.strptime(user_session_info['date'], "%Y-%m-%d")
    workouts.sort(key=lambda w: abs(datetime.strptime(w['date'], "%Y-%m-%d") - user_date))
    return workouts[0]


def log_exercise_set(data):
    """Log a set for a workout."""
    exercise_set = convert_message_to_exercise_schema(data['user_message'])
    print(f"logging exercise set for workout id:  {data['workout_id']}")
    print(f"exercise_set: {exercise_set}")
    # db_ops.add_exercise_set(exercise_set, data['workout_id'])

# 
# converters
#  
def convert_message_to_exercise_schema(user_message):
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": "Extract the workout information from the user's message."},
            {"role": "user", "content": user_message},
        ],
        response_format=workout_schema.ExerciseSet,
    )
    return completion.choices[0].message.parsed


def test():
    user_session_info = {'user_id': "+18577021834", 'date':"2024-10-21"}
    workouts = get_most_likely_workout(user_session_info)
    print(workouts)


if __name__ == "__main__":
    test()
