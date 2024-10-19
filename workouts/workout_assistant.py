import dotenv
import openai
import os
import traceback
import json

from workout_bot_tools import get_all_workouts
import tool_descriptors 

dotenv.load_dotenv()
client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Setup for bot 
class WORKOUT_BOT_CONFIG:
    def __init__(self):
        self.description = """
        You are a workout assistant.
        Your job is to help the user find a workout, log exercises, and track progress.
        """

    @property
    def tools(self):
        return 
    
    @property
    def model(self):
        return "gpt-4o"


def chat_with_workout_bot():
    # setup assistant
    config = WORKOUT_BOT_CONFIG()
    assistant = client.beta.assistants.create(
        instructions=config.description,
        model=config.model,
        tools=[tool_descriptors.get_all_workouts_tool_descriptor]
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

                    if tool.function.name == "get_most_likely_workout":
                        print("AI requested get_most_likely_workout()")
                        print("AI generated arguments:", tool.function.arguments)
                        
                        # Parse the arguments from JSON string to dictionary
                        arguments = json.loads(tool.function.arguments)
                        

                    elif tool.function.name == "get_all_workouts":
                        print("AI requested get_most_likely_workout()")
                        print("AI generated arguments:", tool.function.arguments)

                        # Parse the arguments from JSON string to dictionary
                        arguments = json.loads(tool.function.arguments)
                        
                        tool_outputs.append({
                            "tool_call_id": tool.id,
                            "output": get_all_workouts(arguments)
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
