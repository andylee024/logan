import dotenv
import os

from twilio.rest import Client                                                                                      


dotenv.load_dotenv()
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)

BOT_NUMBER = os.getenv('LOGAN_BOT')


def send_sms_message(user, message):
    message = client.messages.create(
        body=message,
        from_=BOT_NUMBER,
        to=user['phone_number']
    )
    return message.sid

def send_whatsapp_message():
    # Twilio credentials

    # Message details
    # from_whatsapp_number = 'whatsapp:+16262635386'
    from_whatsapp_number = 'whatsapp:+14155238886'
    to_whatsapp_number = 'whatsapp:+16263102445'
    message_body = 'Hello from your Twilio WhatsApp bot!'

    # Send message
    message = client.messages.create(
        body=message_body,
        from_=from_whatsapp_number,
        to=to_whatsapp_number
    )

if __name__ == '__main__':
    user = {'phone_number': '+18577021834'}
    send_sms_message(user, 'Hello from the Logan Bot')
    # sandbox()
    # send_whatsapp_message()