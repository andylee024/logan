import dotenv
import openai
import os

import database.db_operations as db_ops
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

    workout = Workout(date=date, 
                      user_uuid=user_uuid, 
                      status="not_started", 
                      notes="")
    
    return str(workout)

def get_workouts_for_week(user_session_info):
    """Gets the workouts for the user by week."""
    workouts = []
    return workouts

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
    # db_ops.add_user(uuid="+18577021834", 
    #                 name="Andy", phone_number="+18577021834", email="drifter24@gmail.com")

    # add workout
    # workout = workout_schema.Workout(date="2024-08-01", 
    #                                  user_uuid="+18577021834", 
    #                                  status="completed", 
    #                                  notes="")

    # db_ops.add_workout(workout)

    # add exercise set
    e1 = convert_message_to_exercise_schema("I did 3 sets of 10 reps of bench press with 100lbs")
    print(e1)
    db_ops.add_exercise_set(e1, workout_id=1)

    # e2 = convert_message_to_exercise_schema("Bulgarian split squat 3x12 25kg")
    # db_ops.add_exercise_set(workout_id=1, exercise_set_id=1, exercise_id=1, reps=10, weight=100)
    


if __name__ == "__main__":
    test()
