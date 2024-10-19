
class WORKOUT_TOOLS:
    @property
    def get_most_likely_workout(self):
        return get_most_likely_workout_tool

    @property
    def get_workouts_for_week(self):
        return get_workouts_for_week_tool

get_most_likely_workout_tool = {
    "type": "function",
    "function": {
        "name": "get_most_likely_workout",
        "description": "Get the most likely workout for a user based on session info",
        "parameters": {
            "type": "object",
            "properties": {
                "user_session_info": {
                    "type": "object",
                    "description": "Information about the user's session, including user_uuid and date",
                    "properties": {
                        "user_uuid": {"type": "string"},
                        "date": {"type": "string", "format": "date"}
                    },
                    "required": ["user_uuid", "date"]
                }
            },
            "required": ["user_session_info"]
        }
    }
}

get_workouts_for_week_tool = {
    "type": "function",
    "function": {
        "name": "get_workouts_for_week",
        "description": "Get the workouts for a user for the week based on session info",
        "parameters": {
            "type": "object",
            "properties": {
                "user_session_info": {
                    "type": "object",
                    "description": "Information about the user's session, including user_uuid and date",
                    "properties": {
                        "user_uuid": {"type": "string"},
                        "date": {"type": "string", "format": "date"}
                    },
                    "required": ["user_uuid", "date"]
                }
            },
            "required": ["user_session_info"]
        }
    }
}

