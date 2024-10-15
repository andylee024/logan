from sqlalchemy.orm import sessionmaker
from .db_setup import engine
from workouts.workout_schema import ExerciseSet, Workout
from database.models import ExerciseSet as SQLExerciseSet, Workout as SQLWorkout, User as SQLUser

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# 
# Add operations
# 
def add_user(uuid, name, phone_number, email=None):
    session = Session()
    try:
        new_user = SQLUser(uuid=uuid, name=name, phone_number=phone_number, email=email)
        session.add(new_user)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error adding user: {e}")
    finally:
        session.close()


def add_workout(pydantic_workout: Workout):
    session = Session()
    try:
        new_workout = convert_workout(pydantic_workout)
        session.add(new_workout)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error adding workout: {e}")
    finally:
        session.close()


def add_exercise_set(pydantic_exercise_set: ExerciseSet):
    session = Session()
    try:
        new_exercise_set = convert_exercise_set(pydantic_exercise_set)
        session.add(new_exercise_set)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error adding exercise set: {e}")
    finally:
        session.close()

#
# Get operations
# 

def get_all_users():
    session = Session()
    try:
        users = session.query(SQLUser).all()
        return users
    finally:
        session.close()


#
# Convert operations
# 

def convert_exercise_set(pydantic_exercise_set: ExerciseSet) -> SQLExerciseSet:
    return SQLExerciseSet(
        name=pydantic_exercise_set.name,
        sets=pydantic_exercise_set.sets,
        reps=pydantic_exercise_set.reps,
        weight_kg=pydantic_exercise_set.weight_kg,
        rest_min=pydantic_exercise_set.rest_min,
        duration_min=pydantic_exercise_set.duration_min,
        intensity=pydantic_exercise_set.intensity_float,
        notes=pydantic_exercise_set.notes,
    )

def convert_workout(workout: Workout) -> SQLWorkout:
    
    # Create the SQLAlchemy Workout
    sqlalchemy_workout = SQLWorkout(
        user_uuid=workout.user_uuid,
        date=workout.date,
        status=workout.status.value,
        notes=workout.notes,
    )
    
    # Add exercise sets to the workout
    exercise_sets = [convert_exercise_set(ex) for ex in workout.exercises]
    sqlalchemy_workout.exercises = exercise_sets
    
    return sqlalchemy_workout
