import dotenv
import openai
import os

from enum import Enum

from bot import action
from prompts import INTENT_PROMPT, INTENT_SCHEMA
from utils import llm_utils

dotenv.load_dotenv()
client = openai.Client(api_key=os.getenv('OPENAI_API_KEY'))


class Intent(Enum):
    LOG = "log"
    WORKOUT = "workout"
    HELP = "help"


def classify_chat_intent(message):
    """Classify the user's message into an intent"""
    instructions = INTENT_PROMPT 
    schema = f"Use the following schema \n {INTENT_SCHEMA}"
    user_message = f"User message: \n {message}"

    prompt = [
        {
            "role": "system",
            "content": instructions
        },
        {
            "role": "user",
            "content": user_message + "\n" + schema
        }
    ]
    return llm_utils.run_llm(prompt, "gpt-4o", json_format=True)


def route_intent(intent, message):

    if intent == Intent.WORKOUT.value:
        print("Matched WORKOUT intent")
        workout = action.handle_workout()
        message = f"Here's today's workout: \n {workout}. \n Does this look right?"
        return message

    elif intent == Intent.LOG.value:
        print("Matched LOG intent")
        return action.handle_log(message)

    elif intent == Intent.HELP.value:
        print("Matched HELP intent")
        message = "I'm sorry, I don't know how to help with that. Can you please rephrase?"
        return message

    else:
        print("No matching intent found")
        message = "I'm sorry, I don't know how to help with that. Can you please rephrase?"
        return message