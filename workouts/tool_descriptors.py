

get_most_likely_workout_tool_descriptor = {
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

get_workouts_for_week_tool_descriptor = {
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

