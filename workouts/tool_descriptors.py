
get_this_weeks_workouts_tool_descriptor = {
    "type": "function",
    "function": {
        "name": "get_this_weeks_workouts",
        "description": "Get all workouts for a user for this upcoming week",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {"type": "string", "description": "The ID of the user"},
                "date": {"type": "string", "format": "date", "description": "The date for which to retrieve workouts"},
            },
            "required": ["user_id", "date"]
        }
    }
}

get_most_likely_workout_tool_descriptor = {
    "type": "function",
    "function": {
        "name": "get_most_likely_workout",
        "description": "Gets the most likely workout for the user based on timing",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {"type": "string", "description": "The ID of the user"},
                "date": {"type": "string", "format": "date", "description": "The date for which to retrieve workouts"}
            },
            "required": ["user_id", "date"]
        }
    }
}

log_exercise_set_tool_descriptor = {
    "type": "function",
    "function": {
        "name": "log_exercise_set",
        "description": "Log a user's exercise set to the database",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {"type": "string", "description": "The ID of the user"},
                "date": {"type": "string", "format": "date", "description": "The date for which to retrieve workouts"},
                "user_message": {"type": "string", "description": "The user's message containing exercise info to be logged"},
                "workout_id": {"type": "string", "description": "The ID of the workout to log the exercise set to"}
            },
            "required": ["user_id", "date", "user_message", "workout_id"]
        }
    }
}