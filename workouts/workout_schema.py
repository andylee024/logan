from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum


class Status(Enum):
    not_started = "not_started"
    in_progress = "in_progress"
    completed = "completed"
    completed_partial = "completed_partial"
    missed = "missed"


class ExerciseSet(BaseModel):
    name: str
    sets: int
    reps: int
    weight_kg: float = Field(default=None, description="Weight used in the exercise. Output 0.0 if not applicable")

    notes: Optional[str] = Field(default=None, description="Additional notes about the exercise")
    rest_min: Optional[float] = Field(default=None, description="Rest time in minutes")
    duration_min: Optional[float] = Field(default=None, description="Duration of the exercise in minutes")
    intensity_float: Optional[str] = Field(default=None, description="Intensity level, e.g., 'low', 'medium', 'high'")


class Workout(BaseModel):
    user_uuid: str
    date: str
    status: Status = Field(default=Status.not_started, description="Status of the workout")

    exercises: List[ExerciseSet] = Field(default_factory=list, description="List of exercises in the workout") 
    notes: Optional[str] = Field(default=None, description="Additional notes about the workout")
