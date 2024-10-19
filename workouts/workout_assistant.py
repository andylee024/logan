import dotenv
import openai
import os
import traceback
import json

from workout_bot_tools import get_most_likely_workout, get_workouts_for_week
from tool_descriptors import WORKOUT_TOOLS

dotenv.load_dotenv()
client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

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

# Setup for bot 
class WORKOUT_BOT_CONFIG:
    def __init__(self):
        self.description = """
        You are a workout assistant.
        Your job is to help the user find a workout, log exercises, and track progress.
        """

    @property
    def tools(self):
        return [WORKOUT_TOOLS.get_most_likely_workout, WORKOUT_TOOLS.get_workouts_for_week]
    
    @property
    def model(self):
        return "gpt-4o"


def chat_with_workout_bot():
    # setup assistant
    config = WORKOUT_BOT_CONFIG()
    assistant = client.beta.assistants.create(
        instructions="You are a workout assistant. Use the provided functions to answer questions.",
        model="gpt-4o",
        tools=[get_most_likely_workout_tool, get_workouts_for_week_tool]
    )

    thread = client.beta.threads.create()

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
            messages = client.beta.threads.messages.list(thread_id=thread.id)

            for idx, message in enumerate(messages):
                for content_block in message.content:
                    if content_block.type == "text":
                        print(f"Bot {idx}:", content_block.text.value)

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

                    if tool.function.name == "get_most_likely_workout":
                        print("AI requested get_most_likely_workout()")
                        print("AI generated arguments:", tool.function.arguments)
                        
                        # Parse the arguments from JSON string to dictionary
                        arguments = json.loads(tool.function.arguments)
                        
                        tool_outputs.append({
                            "tool_call_id": tool.id,
                            "output": get_most_likely_workout(arguments)
                        })

                        print("TOOL OUTPUTS:", tool_outputs)

                    elif tool.function.name == "get_workouts_for_week":
                        # Parse the arguments from JSON string to dictionary
                        arguments = json.loads(tool.function.arguments)
                        
                        tool_outputs.append({
                            "tool_call_id": tool.id,
                            "output": get_workouts_for_week(arguments)
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
                messages = client.beta.threads.messages.list(
                    thread_id=thread.id
                )
                print(messages)

            else:
                print(run.status)



if __name__ == "__main__":
    chat_with_workout_bot()


"""
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
}"""
