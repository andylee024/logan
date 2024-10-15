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
