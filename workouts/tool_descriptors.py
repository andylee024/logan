
get_all_workouts_tool_descriptor = {
    "type": "function",
    "function": {
        "name": "get_all_workouts",
        "description": "Get all workouts for a user based on session info",
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