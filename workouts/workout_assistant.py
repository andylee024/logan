import datetime
import dotenv
import openai
import os
import traceback
import json

from workout_bot_tools import get_most_likely_workout, get_this_weeks_workouts, log_exercise_set
import tool_descriptors 

dotenv.load_dotenv()
client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Setup for bot 

WORKOUT_BOT_INSTRUCTIONS = """
You are an AI workout assistant.
Your job is to access information about the user and help the user do 1 of 2 workflows.

Start a workout workflow:
If a user wants to start a workout, you will pick the most likely workout for them based on their timing 
If a user confirms the workout or logs an exercise, the workout is confirmed. 
If a user says it's not the right workout, you will show them workouts in the near past and future and ask them to choose the right workout.
You must confirm a workout before logging an exercise set (i.e. have a workout_id)

Log an exercise workflow:
If a user wants to log an exercise, you will provide the workout id and log the exercise 
Users will often respond with workout sets, reps, weights and exercise names when they want to log an exercise.
"""

class WORKOUT_BOT_CONFIG:
    def __init__(self):
        self.instructions = WORKOUT_BOT_INSTRUCTIONS
    
    @property
    def model(self):
        return "gpt-4o"


def chat_with_workout_bot():
    # setup assistant
    config = WORKOUT_BOT_CONFIG()

    assistant = client.beta.assistants.create(
        instructions=config.instructions,
        model=config.model,
        tools=[
            tool_descriptors.get_this_weeks_workouts_tool_descriptor,
            tool_descriptors.get_most_likely_workout_tool_descriptor,
            tool_descriptors.log_exercise_set_tool_descriptor
        ]
    )

    user_session_info = {
        "user_id": "+18577021834",
        "date": datetime.datetime.today()
    }

    thread = client.beta.threads.create()

    # initialize session
    initialization_message = f"The user has started a session : user_id : {user_session_info['user_id']} date : {user_session_info['date']}"
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=initialization_message,
    )

    while True:

        # ask user for input 
        # create message to add to thread
        user_input = input("You: ")
        if user_input.lower() == "done":
            print("Exiting chat.")
            break

        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_input,
        )

        # trigger run of assistant
        run = client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=assistant.id,
        )

        # check if run is completed
        if run.status == "completed":
            bot_response = _retrieve_bot_response(thread.id, client)
            print(f"\n Bot: {bot_response} \n ")

        else:
            print("RUN STATUS:", run.status)
            print("RUN REQUIRED ACTION:", run.required_action)

            # Handle required tool actions
            tool_outputs = []

            if run.required_action and run.required_action.submit_tool_outputs:

                for tool in run.required_action.submit_tool_outputs.tool_calls:

                    print("TOOL FUNCTION:", tool.function)
                    print("TOOL FUNCTION NAME:", tool.function.name)
                    print("TOOL FUNCTION PARAMETERS:", tool.function.arguments)

                    arguments = json.loads(tool.function.arguments)
                    response = ""

                    if tool.function.name == "get_most_likely_workout":
                        response = str(get_most_likely_workout(arguments))

                    elif tool.function.name == "get_this_weeks_workouts":
                        response = str(get_this_weeks_workouts(arguments))

                    elif tool.function.name == "log_exercise_set":
                        response = str(log_exercise_set(arguments))

                    else:
                        raise ValueError(f"no tool implemented for {tool.function.name}")

                    tool_outputs.append({
                        "tool_call_id": tool.id,
                        "output": response
                    })

                    print("TOOL OUTPUTS:", tool_outputs)

            if tool_outputs:
                print("Submitting tool outputs")
                try:
                    run = client.beta.threads.runs.submit_tool_outputs_and_poll(
                        thread_id=thread.id,
                        run_id=run.id,
                        tool_outputs=tool_outputs
                    )
                    print("Tool outputs submitted successfully.")

                except Exception as e:
                    print("Failed to submit tool outputs:", e)
                    traceback.print_exc()
            else:
                print("No tool outputs to submit.")

            if run.status == 'completed':
                bot_response = _retrieve_bot_response(thread.id, client)
                print(f"\n Bot: {bot_response} \n")

            else:
                print(run.status)



def _retrieve_bot_response(thread_id, client):
    messages = client.beta.threads.messages.list(thread_id, limit=1)
    messages_iter = iter(messages)
    most_recent_message = next(messages_iter, None)

    if not most_recent_message:
        return None

    for content_block in most_recent_message.content:
        if content_block.type == "text":
            return content_block.text.value
    


if __name__ == "__main__":
    chat_with_workout_bot()
