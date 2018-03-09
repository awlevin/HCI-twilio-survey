from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from datetime import datetime
from threading import Timer
import os, csv
import json

# Load environment configurations
PORT = os.environ["PORT"]
SECRET_KEY = os.environ["TWILIO_AUTH_TOKEN"]
TWILIO_ACCOUNT_SID = os.environ["TWILIO_ACCOUNT_SID"]

# Load participant details from config file (names and phone numbers)
with open('participants.json') as f:
    participants = json.load(f)

# Configure Flask app
app = Flask(__name__)
app.config.from_object(__name__)

"""
Set up survey times
"""
def setup_survey_times():
    now = datetime.now()
    exec_dates = [datetime(2018, 3, day, hour=9) for day in range(10,15)]
    delays = [(exec_date - now).seconds for exec_date in exec_dates]
    timers = [Timer(delay, inquire_participants) for delay in delays]
    [t.start() for t in timers]

"""
Texts the survey to all of the participants
"""
@app.route("/")
def inquire_participants():
    for cell_number, name in participants.items():
        resp = MessagingResponse()
        client = Client(TWILIO_ACCOUNT_SID, SECRET_KEY)
        client.api.account.messages.create(
        to=str(cell_number),
        from_="+12242231260",
        body="Hey " + name + "! How many times do you think you'll use the bus today? Please respond with 0-10. \n\nThanks again for helping out!")
    return "Hello World!"

"""
Handles all of the user's responses to the survey via webhook configured on Twilio
"""
@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """ RESPOND TO USER TEXT MESSAGES TO THE TWILIO NUMBER"""
    body = request.values.get('Body', None)
    
    date = datetime.now().isoformat()

    from_number = request.values.get('From')
    if from_number in participants:
        name = participants[from_number]
    else:
        name = "Unknown"

    resp = MessagingResponse()
    
    if body.isdigit():
        if (int(body) > 10 or int(body) < 0):
            log(date, body, name)
            resp.message("Please enter a valid number between 0-10")
        else:
            resp.message("Thank you!")
            save_data(name, int(body), date)
    else:
        log(date, body, name)
        resp.message("Please enter a number between 0-10")

    return str(resp)

"""
Save the user's responses to a CSV file
"""
def save_data(name, value, timestamp):
    with open('data.csv', 'a') as csvfile:
        wr = csv.writer(csvfile, dialect='excel')
        wr.writerow([name, value, timestamp])

"""
If a response was invalid, this method will log what the user tried to input in their SMS
"""
def log(date, body, name):
    with open('error_logs.txt', 'a') as logfile:
        logfile.write(date + " --- " + name + " --- " + body + "\n")
        



if __name__ == "__main__":
    setup_survey_times()
    app.run(debug=True, port=int(PORT))
    
