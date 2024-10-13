from enum import Enum



INTENT_PROMPT = """
You are a helpful workout assistant.
Your job is to interpret the user's message and determine their intent. 
Options for intent are:

1. log: Log a lift 
2. workout: Provide a workout   
3. help : unclear intent

Return your answer as a JSON object with the following format:
{
    "intent": <intent>,
    "explanation": 1-line explanation for your choice
}
"""

INTENT_SCHEMA = {
    "type": "object",
    "properties": {
        "intent": {"type": "string"},
        "explanation": {"type": "string"}
    },
    "required": ["intent", "explanation"]
}

WORKOUT_LOG_PROMPT = """
You are a helpful workout assistant.
Your job is to structure the user's message into a loggable format.
The user may provide a single lift or list of lifts
The user will provide a list of lifts they did, along with the sets, reps, and weight.

Return a JSON object with the following format:
{'all_lifts':[{
    "lift": <lift>,
    "sets": <sets>,
    "reps": <reps>,
    "weight": <weight>,
    "unit": kg or lbs
}]}

<lift> is the name of the lift
<sets> is the number of sets
<reps> is the number of reps
"""