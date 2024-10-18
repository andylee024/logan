import dotenv
import openai
import os
import time

import database.db_operations as db_ops

dotenv.load_dotenv()
client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

WORKOUT_BOT_DESCRIPTION = """
You are a workout assistant.
Your job is to help the user find a workout, log exercises, and track progress.
"""

def main():
    assistant = client.beta.assistants.create(
        name="Workout Assistant",
        description=WORKOUT_BOT_DESCRIPTION,
        model="gpt-4o",
        tools=[],
        tool_resources={}
    )

    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": "Give me a legs workout focused on explosiveness.",
            }
        ]
    )
    print(f"Thread ID: {thread.id}")
    print(f"Assistant ID: {assistant.id}")
    print("Starting run...")

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
        model="gpt-4o",
        instructions="Please address the user as Jane Doe. The user has a premium account."
    )

    # Wait for the run to complete
    while True:
        if run.status == 'completed':
            messages = client.beta.threads.messages.list(
                thread_id=thread.id
            )
            print(messages)
            break

        if run.status != 'completed':
            print(run.status)
            time.sleep(1)

def main2():
    # assistant
    assistant = client.beta.assistants.create(
        name="GC_Bot",
        instructions="You are a workout personal trainer. I will ask you some questions about fitness.",
        tools=[{"type": "code_interpreter"}],
        model="gpt-4o",
    )

    chat_with_bot(assistant)


def chat_with_bot(assistant):
    thread = client.beta.threads.create()

    while True:
        user_input = input("You: ")
        if user_input.lower() == "done":
            print("Exiting chat.")
            break

        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_input,
        )

        run = client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=assistant.id,
        )

        if run.status == "completed":
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            print(messages)

            print("OUTPUT \n \n \n")
            for message in messages:
                for content_block in message.content:
                    if content_block.type == "text":
                        print("Bot:", content_block.text.value)
        else:
            print("Error:", run.status)


if __name__ == "__main__":
    main2()
