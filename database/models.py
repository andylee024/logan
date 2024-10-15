from sqlalchemy import create_engine, Column, String, Integer, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    uuid = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    email = Column(String)


class ExerciseSet(Base):
    __tablename__ = 'exercise_sets'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    sets = Column(Integer, nullable=False)
    reps = Column(Integer, nullable=False)
    weight_kg = Column(Float, default=0.0)
    rest_min = Column(Float)
    duration_min = Column(Float)
    intensity = Column(String)
    notes = Column(String)
    
    # workout_id = Column(Integer, ForeignKey('workouts.id'), nullable=False)
    # workout = relationship("Workout", back_populates="exercise_sets")


class Workout(Base):
    __tablename__ = 'workouts'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    date = Column(String, nullable=False)
    status = Column(String, nullable=False)
    notes = Column(String)
    
    exercise_sets = relationship("ExerciseSet", back_populates="workout")
    user_uuid = Column(String, ForeignKey('users.uuid'), nullable=False)
    user = relationship("User")
