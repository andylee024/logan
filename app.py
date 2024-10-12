import os
from flask import Flask, request, jsonify
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

app = Flask(__name__)

# ... existing code ...
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)

BOT_NUMBER = os.getenv('LOGAN_BOT')

@app.route('/handle_incoming_whatsapp_message', methods=['POST'])
def handle_incoming_whatsapp_message():
    # Parse incoming message
    incoming_msg = request.form.get('Body')
    from_number = request.form.get('From')

    # Calculate calories (stubbed function)
    calories = calculate_calories(incoming_msg)

    # Log to Google Sheets
    # log_to_google_sheets(from_number, incoming_msg, calories)

    # Respond to the user
    response = MessagingResponse()
    response.message(f"Your meal has been logged with {calories} calories!")
    return str(response)

# ... existing code ...

def calculate_calories(message):
    # Stubbed function to calculate calories
    # Replace with actual logic or API call
    return 100  # Example static value

def log_to_google_sheets(from_number, message, calories):
    # Google Sheets API setup
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SERVICE_ACCOUNT_FILE = 'path/to/credentials.json'

    credentials = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials)

    # The ID and range of the spreadsheet
    SPREADSHEET_ID = 'your-spreadsheet-id'
    RANGE_NAME = 'Sheet1!A1:C1'

    # Prepare data to append
    values = [[from_number, message, calories]]
    body = {'values': values}

    # Append data to the sheet
    sheet = service.spreadsheets()
    sheet.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME,
        valueInputOption='RAW',
        body=body
    ).execute()

# ... existing code ...

@app.route('/sms', methods=['POST'])
def sms_reply():
    # Get the message the user sent
    incoming_msg = request.form.get('Body')
    from_number = request.form.get('From')

    # Print the message to the console
    print(f"Received message from {from_number}: {incoming_msg}")

    # Respond to the message (optional)
    # response = MessagingResponse()
    # response.message("Thank you for your message!")
    # return str(response)

    message = client.messages.create(
        body="r u sure bro i got it",
        from_=BOT_NUMBER,
        to=from_number
    )
    return message.sid


if __name__ == '__main__':
    app.run(debug=True)
