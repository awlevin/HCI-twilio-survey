# Run with python3
from twilio.rest import Client
import os

TWILIO_ACCOUNT_SID = os.environ["TWILIO_ACCOUNT_SID"]
TWILIO_AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]
TWILIO_NUMBER = os.environ["TWILIO_NUMBER"]

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

message = client.messages.create(
    to="+<country_code><phone_number>",
    from_=TWILIO_NUMBER,
    body="This is a test!")

print(message.sid)

