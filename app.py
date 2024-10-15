import os
import json
from enum import Enum

from flask import Flask, request, jsonify

from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

import bot.intent as intents
import bot.action as action

app = Flask(__name__)

# setup environment
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)

# define constants
BOT_NUMBER = os.getenv('LOGAN_BOT')

@app.route('/sms', methods=['POST'])
def sms_reply():
    # Get the message the user sent
    incoming_msg = request.form.get('Body')
    from_number = request.form.get('From')

    # Print the message to the console
    print(f"Received message from {from_number}: {incoming_msg}")
    intent_json = intents.classify_chat_intent(incoming_msg)

    # parse intent
    intent = json.loads(intent_json)['intent']
    explanation = json.loads(intent_json)['explanation']
    print(f"Intent received: {intent}")
    print(f"Explanation: {explanation}")

    # route to appropriate function
    message = ""
    try:
        message = intents.handle_intent(intent, incoming_msg)
        print(f"Message: {message}")
        
    except Exception as e:
        print(f"Error handling intent: {e}")
        message = "I'm sorry, I don't know how to help with that. Can you please rephrase?"

    message = client.messages.create(
        body=message,
        from_=BOT_NUMBER,
        to=from_number
    )
    return message.sid


if __name__ == '__main__':
    app.run(debug=True)
