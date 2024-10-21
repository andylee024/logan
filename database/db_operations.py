from sqlalchemy.orm import sessionmaker
from workouts.workout_schema import ExerciseSet, Workout
from database.models import ExerciseSet as SQLExerciseSet, Workout as SQLWorkout, User as SQLUser

from database.db_setup import init_db, Session, engine  # Import Session and engine
init_db()

def _row_to_dict(row):
    """Converts a SQLAlchemy row to a dictionary."""
    return {column.name: getattr(row, column.name) for column in row.__table__.columns}

# 
# Add operations
# 
def add_user(user_id, name, phone_number, email=None):
    session = Session()
    try:
        new_user = SQLUser(uuid=user_id, name=name, phone_number=phone_number, email=email)
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
def get_workouts_for_user(user_id: str):
    session = Session()
    try:
        workouts = session.query(SQLWorkout).filter(SQLWorkout.user_id == user_id).all()
        return [_row_to_dict(w) for w in workouts]
    except Exception as e:
        print(f"Error getting workouts for user: {e}")
    finally:
        session.close()


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

def convert_exercise_set(pydantic_exercise_set: ExerciseSet, workout_id: int) -> SQLExerciseSet:
    return SQLExerciseSet(
        workout_id=workout_id,
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
        user_id=workout.user_id,
        date=workout.date,
        status=workout.status.value,
        notes=workout.notes,
    )
    
    # Add exercise sets to the workout
    exercise_sets = [convert_exercise_set(ex, sqlalchemy_workout.id) for ex in workout.exercises]
    sqlalchemy_workout.exercises = exercise_sets
    
    return sqlalchemy_workout

def test():
    workouts = get_workouts_for_user("+18577021834")
    print(workouts)

if __name__ == "__main__":
    test()
