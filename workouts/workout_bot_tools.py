import dotenv
import openai
import os

import database.db_operations as db_ops
import workout_schema
from workout_schema import ExerciseSet, Workout

dotenv.load_dotenv()
client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


# 
# workout getters
#
def get_most_likely_workout(user_session_info):
    """Gets the most likely workout based on the user session info."""
    user_uuid = user_session_info.get("user_uuid", "+16263102445")
    date = user_session_info.get("date", "2024-08-01")
    workouts = db_ops.get_workouts_for_user(user_uuid)
    return workouts


def get_all_workouts(user_session_info):
    """Gets all workouts for a user."""

    def _convert_workouts_to_json(workout):
        return {"user_id": workout.user_id,
         "workout_id": workout.id,
         "date": workout.date,
         "status": workout.status,
         "notes": workout.notes}
    
    try:
        user_id = user_session_info.get("user_id")
        workouts = db_ops.get_workouts_for_user(user_id)
        return str([_convert_workouts_to_json(w) for w in workouts])

    except Exception as e:
        print(f"Cannot retrieve workouts for user: {e}")
        return []

# 
# handle workout state
# 
def handle_workout_start(user_session_info, workout_id):
    """Start workout and handle all required flows"""
    pass

def handle_workout_end(user_session_info, workout_id):
    """End workout and handle all required flows."""
    pass

def log_exercise_set(user_message, workout_id):
    """Log a set for a workout."""
    exercise_set = convert_message_to_exercise_schema(user_message)
    db_ops.add_exercise_set(exercise_set, workout_id)
    pass

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

    # add user
    # db_ops.add_user(user_id="+447470774593", 
    #                 name="Andy", 
    #                 phone_number="+447470774593", 
    #                 email="drifter24@gmail.com")

    # get workout 
    user_session_info = {'user_id': "+18577021834", 'date':"2024-08-01"}
    workouts = get_all_workouts(user_session_info)
    print(workouts)

    # add exercise set
    # e1 = convert_message_to_exercise_schema("I did 3 sets of 10 reps of bench press with 100lbs")
    # db_ops.add_exercise_set(e1, workout_id=1)


if __name__ == "__main__":
    test()
