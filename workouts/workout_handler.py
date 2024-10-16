import dotenv
import openai
import os

import database.db_operations as db_ops
import workout_schema


dotenv.load_dotenv()
client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def _convert_message_to_exercise_schema(user_message):
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
    e1 = _convert_message_to_exercise_schema("I did 3 sets of 10 reps of bench press with 100lbs")
    print(e1)
    db_ops.add_exercise_set(e1, workout_id=1)

    # e2 = convert_message_to_exercise_schema("Bulgarian split squat 3x12 25kg")
    # db_ops.add_exercise_set(workout_id=1, exercise_set_id=1, exercise_id=1, reps=10, weight=100)
    


if __name__ == "__main__":
    test()
